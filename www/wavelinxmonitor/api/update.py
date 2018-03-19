# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/update
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import logging
import os
import subprocess as sub

import bottle
from bottle import request, HTTPError

from helpers.auth import auth_token, validate_token, csrf_check
from helpers.filemanager import process_wac_archive, process_archive
from helpers.flex import get_fw_version

app = application = bottle.default_app()
logger = logging.getLogger(__name__)

# Load Configuration Constants
API_VERSION = app.config['wlm.api_version']
DEVICE_FILES_DIR = app.config['ota.device_files_dir']
DEVICE_OTA_DIR = app.config['ota.device_files_dir']
DEVICE_OTA_FILE = app.config['ota.device_file']
OTA_DIR = app.config['ota.update_dir']
OTA_TMP_FILE = app.config['ota.update_file']
OTA_TXT_FILE = app.config['ota.update_txt_file']

# Derived Constants
BASE_URL = '/' + API_VERSION + '/update'

##### Update #####
@app.get(BASE_URL)
@auth_token(validate_token)
def get_update():
	'''
	Return available update info
	'''
	update_info = ''

	logger.info('Looking for update file at %s' % OTA_TMP_FILE)
	wac_update = (os.path.exists(OTA_TMP_FILE))
	logger.info('Found wac_update status: %s' % wac_update)

	try:
		logger.info('Checking for device files directory at %s' % DEVICE_FILES_DIR)
		device_update = (os.listdir(DEVICE_FILES_DIR) != [])
		logger.info('Found directory, directory has files status: %s' % device_update)
	except:
		logger.info('No device files directory found')
		device_update = False

	if wac_update:
		try:
			logger.info('Getting update info from wac update archive')
			update_info = process_wac_archive(OTA_TMP_FILE)

		except:
			logger.info('Something went wrong, removing ota tmp file')
			os.remove(OTA_TMP_FILE)
			return HTTPError(404,
							'Unsuccessful getting update file info. \
							You need to re-upload the update file.')

	return {
		'currentWacVersion': get_fw_version(),
		'wacUpdateAvailable': wac_update,
		'deviceUpdateAvailable': device_update,
		'updateInfo': update_info
	}


##### Update - Get WAC Update #####
@app.get(BASE_URL + '/wac')
@auth_token(validate_token)
def get_wac_update():
	'''
	Return available update info (deprecated)
	'''
	logger.info('Why you callin\' this endpoint?!')
	return get_update()


##### Update - Start WAC Update #####
@app.post(BASE_URL + '/wac')
@csrf_check()
@auth_token(validate_token)
def start_gateway_update():
	'''
	Begin gateway update
	'''
	data = ''
	try:
		data = request.json
		start_update = data['startWacUpdate']

	except ValueError:
		return HTTPError(404, 'Missing data')

	logger.info('Should we run a WAC update?')

	if start_update and os.path.exists(OTA_TMP_FILE):
		logger.info('Apparently so.')
		update_info = process_wac_archive(OTA_TMP_FILE)
		# update_fw_int = int(update_info['fw_version'].split('-')[1])
		# current_fw = get_fw_version()
		# current_fw_int = int(current_fw.split('-')[1])

		# if update_fw_int < current_fw_int:
		# 	return HTTPError(404, 'To downgrade, restore from a previous backup')

		logger.info('Starting applyOta.sh...')
		p = sub.Popen(['/root/applyOta.sh'], stdout=sub.PIPE, stderr=sub.PIPE)
		output, errors = p.communicate()

		result = output.strip('\n').split('\n')[-1]
		logger.info('applyOta result: %s' % result)

		if 'Error' in result:
			logger.warning('Error occurred in applyOta script')
			return HTTPError(404, 'Update not available or failed')

		else:
			logger.warning('Going down for reboot')
			sub.Popen(['reboot','-d','2'])
			return {
				'wacUpdating': True,
				'updateInfo': update_info
			}

	else:
		logger.info('Guess not...')
		return {
			'wacUpdating': False,
			'updateInfo': ''
		}


##### WAC - Upload File #####
@app.post(BASE_URL + '/upload')
@csrf_check()
@auth_token(validate_token)
def upload_file():
	'''
	Upload update files
	'''
	if 'file' not in request.files:
		return HTTPError(404, 'No update file found')

	try:
		logger.info('File upload succeeded. Let\'s get it')
		ota_archive = request.files.get('file')

		if ota_archive.filename.startswith('otaUpdate') and ota_archive.filename.endswith('.tgz'):
			logger.info('Got an otaUpdate*.tgz file')
			ota_archive.save(OTA_TMP_FILE,overwrite=True)

			if os.path.exists(OTA_TXT_FILE):
				logger.info('Remove existing %s file' % OTA_TXT_FILE)
				os.remove(OTA_TXT_FILE)

		elif ota_archive.filename.startswith('deviceUpdate') and ota_archive.filename.endswith('.tgz'):
			logger.info('Got a deviceUpdate*.tgz file')
			if not os.path.exists(DEVICE_OTA_DIR):
				os.makedirs(DEVICE_OTA_DIR + '/')
			elif os.path.isfile(DEVICE_OTA_DIR):
				os.remove(DEVICE_OTA_DIR)
				os.makedirs(DEVICE_OTA_DIR + '/')

			if os.path.exists(DEVICE_FILES_DIR):
				for root,dirs,filenames in os.walk(DEVICE_FILES_DIR):
					for f in filenames:
						os.remove(os.path.join(root,f))
					for name in dirs:
						os.rmdir(os.path.join(root,name))

				os.rmdir(DEVICE_FILES_DIR)

			ota_archive.save(DEVICE_OTA_FILE,overwrite=True)
			process_archive(DEVICE_OTA_FILE,'/storage/ota-files/')

		elif ota_archive.filename.endswith('.ota'):
			logger.info('Got *.ota file')
			if not os.path.exists(DEVICE_OTA_DIR):
				logger.info('%s doesn\'t exist, so create it' % DEVICE_OTA_DIR)
				os.makedirs(DEVICE_OTA_DIR + '/zigbee/')
			elif os.path.isfile(DEVICE_OTA_DIR):
				logger.info('%s is a file for some reason, fix it' % DEVICE_OTA_DIR)
				os.remove(DEVICE_OTA_DIR)
				os.makedirs(DEVICE_OTA_DIR + '/zigbee/')
			elif not os.path.exists(DEVICE_OTA_DIR + '/zigbee/'):
				logger.info('%s/zigbee/ not there, so create it' % DEVICE_OTA_DIR)
				os.makedirs(DEVICE_OTA_DIR + '/zigbee/')

			# delete existing file that startswith same device name
			new_filename_split = ota_archive.filename.split('_')
			new_device = '_'.join(new_filename_split[:-1])
			logger.info('New file device: %s' % new_device)

			for root,dirs,filenames in os.walk(DEVICE_FILES_DIR):
				for f in filenames:
					old_filename_split = f.split('_')
					old_device = '_'.join(old_filename_split[:-1])
					logger.info('Existing ota file device: %s' % old_device)

					if old_device == new_device:
						logger.info('Found a match! Remove the old file.')
						old_file_path = os.path.join(DEVICE_FILES_DIR,'zigbee',f)
						logger.info('Deleting %s' % old_file_path)
						os.remove(old_file_path)
						break

			logger.info('Save the new .ota file')
			ota_archive.save(DEVICE_OTA_DIR + '/zigbee/', overwrite=True)

		else:
			return HTTPError(404, 'Unrecognized update file')

	except:
		return HTTPError(404, 'Saving file unsuccessful')

	return get_update()
