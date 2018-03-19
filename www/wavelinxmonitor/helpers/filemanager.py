# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/filemanager
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import logging
import os
import shutil
import tarfile
from threading import Timer
import time

from helpers import darkcapi
from helpers.subproc import make_args, make_sub, do_sync
from helpers import flex

logger = logging.getLogger(__name__)
logger.debug('Loading module: %s', __name__)


def delayed_delete(filename='', delay_sec=30.0):
	def delete_file():
		logger.debug('Removing file: ' + str(filename))
		if os.path.exists(filename):
			os.remove(filename)

	logger.debug('Set ' + str(filename) + ' to delete in ' + str(delay_sec) + 's')
	timer = Timer(delay_sec, delete_file)
	timer.start()

def update_values_json(update_file):
	'''
	Return dictionary of contents of text file or file object structured as:
	key_1=value_1
	key_2=value_2
		...
	key_n=value_n
	'''
	if type(update_file) is tarfile.ExFileObject:
		logger.debug('Reading tarfile object contents...')
		update_content = update_file.readlines()

	elif type(update_file) is str:
		with open(update_file, 'r') as update_values:
			logger.debug('Opening update_values.txt file...')
			update_content = update_values.readlines()
	else:
		raise ValueError('Unrecognized update_file location or object supplied')

	update_data = [s.strip().split('=') for s in update_content]

	update_object = {}
	for element in update_data:
		if len(element) > 1:
			update_object[element[0]] = element[1]

	return update_object

def process_wac_archive(archive=''):
	'''
	Return update info from update_values.txt
	- takes a file name (with path) as an argument
	'''
	logger.debug('Attempting to get update_values.txt from first tarfile object')
	tar = tarfile.open(archive, 'r|gz')
	first_item = tar.next()

	if first_item.name == 'update_values.txt':
		try:
			update_file_obj = tar.extractfile(first_item)
			logger.debug('Extracting json data from tarfile object')
			return update_values_json(update_file_obj)

		except Exception as err:
			logger.exception('Problem in process_wac_archive with tarfile object')
			logger.warning(repr(err))

	logger.debug('Fallback to extracting %s to get update_values.txt',archive)
	if not os.path.isfile('/tmp/update_values.txt'):
		try:
			logger.debug('No update_values.txt file in /tmp, extracting archive...')
			tar = tarfile.open(archive, 'r|gz')
			tar.extractall('/tmp') #12s
			os.remove('/tmp/rootfs.tgz')
			os.remove('/tmp/uImage')
		except Exception as err:
			logger.exception('Problem getting update values')
			logger.warning(repr(err))
			raise

	try:
		logger.debug('Extracting json data from update_values.txt')
		return update_values_json('/tmp/update_values.txt')
	except Exception as err:
		logger.exception('Problem in process_wac_archive')
		logger.warning(repr(err))
		logger.debug('Removing /tmp/update_values.txt')
		os.remove('/tmp/update_values.txt')
		raise

def process_archive(archive='', extract_dir='/tmp/'):
	'''
	Send ota files to /storage/ota-files/zigbee/
	- takes a file name (with path) as an argument
	'''
	logger.debug('Extracting ' + str(archive) + ' to ' + str(extract_dir))
	try:
		logger.debug('Opening archive file')
		tar = tarfile.open(archive, 'r|gz')
		logger.debug('Extracting archive contents')
		tar.extractall(extract_dir)
		logger.debug('Cleaning up (removing) archive file')
		os.remove(archive)

	except Exception as err:
		logging.exception('Problem in process_archive')
		logger.warning(repr(err))
		raise

def restore_from_backup():
	'''
	Restore gateway from /storage/restore/
	1. Remove /storage/openldap-data/
	1. Move /storage/restore/openldap-data/ to /storage/
	1. /etc/init.d/ldap restart
	1. Restore hostname from backup
	1. ZigBee info
	1. monit stop wavelinx
	1. Remove /storage/wavelinx/
	1. Move /storage/restore/wavelinx/ to /storage/
	'''

	# Update LDAP and Avahi
	try:
		logger.debug('Removing hostname file')
		if os.path.exists('/storage/hostname'):
			os.remove('/storage/hostname')
		logger.debug('Removing openldap-data directory')
		shutil.rmtree('/storage/openldap-data')
		do_sync()

		logger.debug('Stopping ldap...')
		ldap_stop = make_sub(make_args('/etc/init.d/ldap stop'))
		ldap_stop.communicate()
		logger.debug('Copying ldap files')
		shutil.move('/storage/restore/openldap-data','/storage/')
		do_sync()

		logger.debug('Restarting ldap...')
		ldap_start = make_sub(make_args('/etc/init.d/ldap start'))
		ldap_start.communicate()

		logger.debug('Getting backed up hostname')
		with open('/storage/restore/hostname') as f:
			name = f.readlines()

		backup_hostname = name[0].strip('\n')
		logger.debug('Restoring hostname to: %s' % backup_hostname)
		flex.update_avahi_name(backup_hostname)

	except Exception as err:
		logger.exception('Problem restoring system files')
		logger.warning(repr(err))
		raise

	try:
		logger.debug('Restoring wifi-config file')
		shutil.copy('/storage/restore/wifi-config', '/storage/')
	except:
		logger.debug('No wifi-config file')

	# Trigger ZigBee network reload in wavelinx
	try:
		logger.debug('Copy network-backup.bin to network-restore.bin and trigger network restore')
		shutil.move('/storage/restore/wavelinx/network-backup.bin',
					'/storage/wavelinx/network-restore.bin')
		darkcapi.get_oid_list()
		zigbee_nw_manager = darkcapi.find_oid('NetworkManager')
		logger.debug('Found NetworkManager oid: ' + str(zigbee_nw_manager))
		req_body = {'~restoreZigBeeNetwork': 1}
		logger.debug('Sending ZigBee network restore command: ' + str(req_body))
		darkcapi.update_oid(zigbee_nw_manager, req_body)
		logger.debug('ZigBee restore request successful')
		time.sleep(2)

	except Exception as err:
		logger.exception('Problem with network restore request')
		logger.warning(repr(err))
		raise

	# Verify status of network restore
	nw_restored_status = 'ZigBee network restore error'
	nw_mgr_status = darkcapi.get_oid(zigbee_nw_manager)

	if 'zigBeeRestoreStatus' in nw_mgr_status:
		for i in range(5):
			logger.debug('Checking ZigBee network restore status, attempt %s' % i)
			nw_mgr_status = darkcapi.get_oid(zigbee_nw_manager)
			if nw_mgr_status['zigBeeRestoreStatus'] != 'Default':
				logger.debug('Status changed, zigBeeRestoreStatus: %s' % nw_mgr_status['zigBeeRestoreStatus'])
				nw_restored_status = ''.join(['ZigBee network ',nw_mgr_status['zigBeeRestoreStatus']])
				break
			logger.debug('No change yet, zigBeeRestoreStatus: %s' % nw_mgr_status['zigBeeRestoreStatus'])
			time.sleep(1)
	else:
		logger.debug('Missing zigBeeRestoreStatus attribute')


	# Update WaveLinx database
	try:
		logger.debug('Stopping wavelinx from monit')
		flex.stop_wavelinx()
		logger.debug('Removing wavelinx user data from /storage/wavelinx/')
		shutil.rmtree('/storage/wavelinx')
		do_sync()
		logger.debug('Copying wavelinx restore data')
		shutil.move('/storage/restore/wavelinx', '/storage/')
		do_sync()
		time.sleep(2)
		# start_wavelinx() only if we're not also doing an update

	except Exception as err:
		logger.exception('Problem restoring wavelinx')
		logger.warning(repr(err))
		raise

	return nw_restored_status

def create_backup_archive(filename='backup_wac.tgz'):
	'''
	Create a backup of the system to be used for
	system restore purposes, including:
	- /storage/wavelinx/
	- /storage/openldap-data/
	- /storage/hostname
	- /storage/wifi-config
	- /storage/.backup/otaUpdate.tgz
	- /etc/passwd ???
	- /etc/config/network ???
	- /etc/wireless/mt7620/mt7620.dat ???
	'''
	# Trigger ZigBee network backup in wavelinx
	try:
		logger.debug('Initiating ZigBee network backup')
		darkcapi.get_oid_list()
		zigbee_nw_manager = darkcapi.find_oid('NetworkManager')
		logger.debug('Found NetworkManager oid: ' + str(zigbee_nw_manager))
		req_body = {'~backupZigBeeNetwork': 1}
		logger.debug('Sending ZigBee network backup command: ' + str(req_body))
		darkcapi.update_oid(zigbee_nw_manager, req_body)
		logger.debug('ZigBee backup request successful')

	except Exception as err:
		logger.exception('Problem backing up network')
		logger.warning(repr(err))
		raise

	try:
		backup_tmp_path = os.path.join('/tmp/', filename)

		with tarfile.open(backup_tmp_path, 'w:gz') as backup_file:
			logger.debug('Adding /storage/wavelinx/ to archive...')
			backup_file.add('/storage/wavelinx', arcname='/wavelinx')
			logger.debug('Adding /storage/openldap-data/ to archive...')
			backup_file.add('/storage/openldap-data', arcname='/openldap-data')
			logger.debug('Adding /storage/hostname to archive...')
			backup_file.add('/storage/hostname', arcname='hostname')

			try:
				logger.debug('Trying to add /storage/wifi-config to archive...')
				backup_file.add('/storage/wifi-config', arcname='wifi-config')
			except:
				logger.debug('Adding wifi-config failed')
			try:
				logger.debug('Trying to add /storage/.backup/otaUpdate.tgz to archive...')
				backup_file.add('/storage/.backup/otaUpdate.tgz', arcname='/backup/otaUpdate.tgz')
			except:
				logger.debug('Adding .backup failed')

			logger.debug('Finishing creating backup tgz')
			backup_file.close()
		return

	except Exception as err:
		logger.exception('Problem backing up wavelinx')
		logger.warning(repr(err))
		raise
