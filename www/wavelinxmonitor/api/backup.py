# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/backup
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
from datetime import datetime
import hashlib
from itertools import product
import logging
import os
import random
import shutil
import string
import subprocess as sub

import bottle
from bottle import request, static_file, HTTPError

from helpers.auth import auth_token, validate_token, csrf_check
from helpers.filemanager import (create_backup_archive, delayed_delete, process_archive,
								 process_wac_archive, restore_from_backup)
from helpers import flex
from helpers import enc_dec

app = application = bottle.default_app()
logger = logging.getLogger(__name__)

# Load Configuration Constants
API_VERSION = app.config['wlm.api_version']
BACKUP_FILE = app.config['backup.file']
BACKUP_FILENAME_BASE = app.config['backup.filename_base']
DATE_FORMAT = app.config['date.date_format']
ENC_KEY = app.config['wlm.enc_key']
OTA_TMP_FILE = app.config['ota.update_file']
RESTORE_DIR = app.config['restore.dir']
RESTORE_BACKUP = app.config['restore.backup']
TMP_DIR = app.config['wlm.tmp_dir']
UPDATE_FILE = app.config['ota.update_file']

# Derived Constants
BASE_URL = '/' + API_VERSION + '/backup'
VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)

##### GET Backup URL #####


@app.get(BASE_URL)
@auth_token(validate_token)
def get_backup():
	'''
	Return backup file
	'''
	now = datetime.now()
	nowfmt = now.strftime(DATE_FORMAT)
	wac_name = flex.get_avahi_name()
	randomize = ''.join(random.choice(VALID_CHARS) for _ in range(4))
	backup_filename = '_'.join(
		[BACKUP_FILENAME_BASE, wac_name, nowfmt, randomize]) + '.tgz'
	backup_filename_valid = ''.join(
		c for c in backup_filename if c in VALID_CHARS)

	logger.info('Backup filename: ' + backup_filename_valid)

	for root, dirs, filenames in os.walk('/tmp'):
		for f in filenames:
			if f.startswith(BACKUP_FILENAME_BASE):
				logger.debug('Deleting old backup file ' + str(f))
				os.remove(os.path.join(root, f))
			elif f.startswith('del_'):
				logger.debug('Deleting old backup file ' + str(f))
				os.remove(os.path.join(root, f))
	try:
		logger.info('Creating backup file...')
		create_backup_archive(backup_filename_valid)
		backup_tmp_path = os.path.join('/tmp/', backup_filename_valid)
		try:
			logger.debug('Reading key value...')
			with open(ENC_KEY, 'r') as _file:
				key = _file.read()
		except IOError:
			logger.debug('Unable to read key ...')
		try:
			backup_filename_valid = enc_dec.encrypt_file(key, backup_tmp_path)
			backup_filename_valid = os.path.basename(backup_filename_valid)
			logger.debug('Finishing encrypted backup .enc')
		except Exception as err:
			logger.exception(err)
			logger.debug('Encryption failed ...')
	except Exception as err:
		logger.exception(err)
		logger.warning('Problem creating backup file')
		return HTTPError(404, 'Unable to create backup file.')

	token = request.get_header('token', None)
	secure_link_content = backup_filename_valid + ':' + token
	dynamic_url = hashlib.md5(secure_link_content).hexdigest()
	logger.info('Generating secure URL: ' + dynamic_url)

	logger.info('Set backup file to be deleted after 60s')
	delayed_delete('/tmp/' + backup_filename_valid, 60.0)

	return {
		'downloadLink': dynamic_url
	}


##### GET Backup File #####
@app.get(BASE_URL + '/<secure_url>')
def get_backup_file(secure_url):
	'''
	Verify secure_url matches a hash of a backup file and a valid token and
	return the file.
	'''
	logger.info('Gathering available backups and sessions')
	backups = []
	sessions = []
	for root, dirs, filenames in os.walk('/tmp'):
		for f in filenames:
			if f.startswith(BACKUP_FILENAME_BASE):
				logger.debug('Found backup %s' % f)
				backups.append(f)
			elif f.startswith('session-'):
				logger.debug('Found session %s' % f)
				sessions.append(f)

	if len(backups) == 0:
		logger.info('Didn\'t find any available backup file')
		return HTTPError(404, 'No backup file available')

	test_list = list(product(backups, sessions))

	for item in test_list:
		token = item[1][8:]
		item_digest = hashlib.md5(item[0] + ':' + token).hexdigest()
		if item_digest == secure_url:
			backup_file = item[0]
			new_filename = 'del_' + hashlib.md5(backup_file).hexdigest()

			if validate_token(token):
				logger.info('Token valid, backup file available')
				logger.info('Renaming backup so no more downloads can happen')
				os.rename('/tmp/' + backup_file, '/tmp/' + new_filename)
				logger.info('Deleting the file in 30s')
				delayed_delete('/tmp/' + new_filename, 30.0)
				logger.info('Sending the backup file')
				return static_file(new_filename,
								   root='/tmp',
								   download=backup_file,
								   mimetype='application/octet-stream')
			else:
				logger.info('Backup available, but no valid session to match')
				return HTTPError(404, 'Your link is now invalid')

	logger.info('Somehow we ended up here...?')
	return HTTPError(404, 'No valid backup file available')


##### GET Restore #####
@app.get(BASE_URL + '/restore')
@auth_token(validate_token)
def get_restore():
	'''
	Return available restore info
	'''
	if os.path.isfile(BACKUP_FILE):
		logger.info('Backup file available')

		if os.path.exists(RESTORE_DIR):
			logger.info(
				'Removing existing restore directory /storage/restore/')
			shutil.rmtree(RESTORE_DIR)

		logger.info('Creating restore directory /storage/restore/')
		os.makedirs(RESTORE_DIR)

		try:
			logger.info('Extracting backup into restore directory')
			process_archive(BACKUP_FILE, RESTORE_DIR)
		except:
			return HTTPError(404, 'Failed to extract restore data')
	else:
		logger.info('No backup file available')

	if os.path.exists(RESTORE_DIR):
		logger.info('Restore directory ready')
		run_apply_ota = False
		current_ver = flex.get_fw_version()
		restore_ver = ''

		if os.path.isfile(RESTORE_BACKUP):
			logger.info('Restore data has an update archive')
			shutil.move(RESTORE_BACKUP, UPDATE_FILE)

		try:
			update_info = process_wac_archive(OTA_TMP_FILE)
			restore_ver = update_info.get('fw_version', '')

			if restore_ver != current_ver:
				logger.info('Current version: ' + str(current_ver))
				logger.info('Restore version: ' + str(restore_ver))
				logger.info('Need to do an update!')
				run_apply_ota = True

		except:
			logger.info('No update available')
			update_info = {}

		return {
			'restoreAvailable': True,
			'restoreWithUpdate': run_apply_ota,
			'currentVersion': current_ver,
			'restoreVersion': restore_ver
		}

	else:
		logger.info('Restore directory not available')

	return HTTPError(404, 'No restore available')


##### POST Start WAC Restore #####
@app.post(BASE_URL + '/restore')
@csrf_check()
@auth_token(validate_token)
def start_gateway_restore():
	'''
	Restore gateway from wacBackup.tgz file
	'''
	data = ''
	try:
		data = request.json
		start_restore = data['startWacRestore']

	except ValueError:
		return HTTPError(404, 'Missing data')

	restore_info = get_restore()

	if type(restore_info) is HTTPError:
		return restore_info

	restore_available = restore_info.get('restoreAvailable', False)
	restore_and_update = restore_info.get('restoreWithUpdate', False)

	if restore_available and start_restore:
		try:
			logger.info('Restoring from backup')
			network_restored_status = restore_from_backup()
			logger.info('Cleanup, removing /storage/restore/ directory')
			shutil.rmtree('/storage/restore')

		except Exception as e:
			return HTTPError(404, 'Failed to restore gateway')

		if restore_and_update:
			logger.info(
				'Update required, removing monit state file so it will restart after update')
			os.remove('/storage/.monit.state')
			logger.info('Running applyOta...')
			p = sub.Popen(['/root/applyOta.sh'],
						  stdout=sub.PIPE, stderr=sub.PIPE)
			output, errors = p.communicate()

			result = output.strip('\n').split('\n')[-1]

			if 'Error' in result:
				return HTTPError(404, 'Update not available or failed')

			else:
				logger.info('applyOta succeeded, going down for reboot in 2s')
				update_info = process_wac_archive(OTA_TMP_FILE)
				sub.Popen(['reboot', '-d', '2'])

				return {
					'networkRestore': network_restored_status,
					'wacRestore': True,
					'reboot': True,
					'restoreInfo': restore_info
				}

		else:
			logger.info(
				'No update required, so we\'re going to try and restart wavelinx')
			try:
				logger.info(
					'Attempting to restart wavelinx (removing .monit.state as a fallback)')
				os.remove('/storage/.monit.state')
				test1 = flex.start_wavelinx()
				logger.debug('Started wavelinx? test1=' + str(test1[0]))

				return {
					'networkRestore': network_restored_status,
					'wacRestore': True,
					'reboot': False,
					'restoreInfo': restore_info
				}

			except:
				logger.info(
					'Failed to restart wavelinx, clearing .monit.state and rebooting...')
				os.remove('/storage/.monit.state')
				sub.Popen(['reboot', '-d', '2'])
				return {
					'networkRestore': network_restored_status,
					'wacRestore': True,
					'reboot': True,
					'restoreInfo': restore_info
				}

	else:
		return {
			'networkRestore': network_restored_status,
			'wacRestore': False,
			'reboot': False,
			'restoreInfo': restore_info
		}


##### POST Upload Backup File #####
@app.post(BASE_URL + '/upload')
@csrf_check()
@auth_token(validate_token)
def upload_backup_file():
	'''
	Upload file
	'''
	if 'file' not in request.files:
		logger.info('No backup file in the request')
		return HTTPError(404, 'No backup file found')

	try:
		archive = request.files.get('file')
		logger.info('Filename: ' + str(archive.filename))

		if archive.filename.startswith('bak_') and archive.filename.endswith('.tgz.enc'):
			logger.info('Backup file starts with bak_ and ends with .tgz.enc')

			if os.path.exists(BACKUP_FILE):
				logger.info('Removing existing restore file')
				os.remove(BACKUP_FILE)

			archive.save(TMP_DIR, overwrite=True)
			logger.info('Saved file to ' + str(TMP_DIR))
			enc_file_path = os.path.join(TMP_DIR, archive.filename)

			try:
				logger.debug('Reading key value...')
				with open(ENC_KEY, 'r') as _file:
					key = _file.read()
			except IOError:
				logger.debug('Unable to read key ...')
			try:
				file_path = enc_dec.decrypt_file(key, enc_file_path)
				logger.debug('Finishing decryption of backup .tgz')
			except Exception as err:
				logger.exception(err)
				logger.debug('Decryption failed ...')

		elif archive.filename.startswith('bak_') and archive.filename.endswith('.tgz'):
			logger.info('Backup file starts with bak_ and ends with .tgz')

			if os.path.exists(BACKUP_FILE):
				logger.info('Removing existing restore file')
				os.remove(BACKUP_FILE)

			archive.save(TMP_DIR, overwrite=True)
			logger.info('Saved file to ' + str(TMP_DIR))
			file_path = os.path.join(TMP_DIR, archive.filename)

		else:
			logger.info('Dunno what this is...')
			return HTTPError(404, 'Unrecognized backup file')

		os.rename(file_path, BACKUP_FILE)
		logger.info('Renamed file to ' + str(BACKUP_FILE))

	except Exception as err:
		logger.exception(err)
		logger.warning('Error saving backup file')
		return HTTPError(404, 'Saving file unsuccessful')

	return get_restore()
