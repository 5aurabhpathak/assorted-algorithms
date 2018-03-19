# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/system
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
from datetime import datetime
import logging
import os
import shutil
import string
import subprocess as sub
import time

import bottle
from bottle import request, HTTPError
import paho.mqtt.publish as mqtt_publish

from helpers.auth import auth_token, validate_token, touch_token, csrf_check
from helpers import flex
from helpers import ldap
from helpers.subproc import make_args, make_sub
from helpers.syscommand import SynCommand

app = application = bottle.default_app()
logger = logging.getLogger(__name__)

# Load Configuration Constants
API_VERSION = app.config['wlm.api_version']
CERTIFICATE_BASE = app.config['certificate.default']
CERTIFICATE_DIR = app.config['certificate.dir']
CERTIFICATE_FILE = app.config['certificate.file']
CUSTOM_CERT_FLAG = app.config['certificate.flag']
DATETIME_FORMAT = app.config['date.datetime_format']
LINUX_DATE_FORMAT = app.config['date.linux_format']

# Derived Constants
BASE_URL = '/' + API_VERSION + '/system'
PLATFORM_BROKER = '127.0.0.1'
VALID_CHARS = "-%s%s" % (string.ascii_letters, string.digits)

##### System #####
@app.get(BASE_URL)
@auth_token(validate_token)
def get_system():
	'''
	Return current system status (time, networks)
	'''

	return {
		'build': flex.get_fw_version(),
		'customCertificate': get_certificate_status(),
		'shellAccess': flex.shell_access_enabled(),
		'time': get_system_time(),
		'users': ldap.get_allowed_users(),
		'version': flex.get_wac_version(),
		'wacName': flex.get_avahi_name()
	}


##### System - Get Time #####
@app.get(BASE_URL + '/time')
@auth_token(validate_token)
def get_system_time():
	'''
	Return current system time
	'''
	now = datetime.now()
	nowfmt = now.strftime(DATETIME_FORMAT)

	p = sub.Popen(['uci','get','system.@system[0].timezone'], stdout=sub.PIPE, stderr=sub.PIPE)
	timezone, errors = p.communicate()

	return {
		'time': nowfmt,
		'timeZone': timezone.strip('\n'),
		'useNtp': flex.ntp_enabled(),
		'ntpServers': flex.ntp_servers()
	}


##### System - Update Time #####
@app.post(BASE_URL + '/time')
@csrf_check()
@auth_token(validate_token)
def update_system_time():
	'''
	Manually set system time
	'''
	data = ''
	try:
		data = request.json
		useNtp = data.get('useNtp',False)

	except ValueError:
		return HTTPError(404, 'Missing data')

	if useNtp:

		try:
			ntp_array = data['ntpServers']

		except:
			return HTTPError(404, 'Missing NTP servers')

		p = sub.Popen(['uci','delete','system.ntp.server'], stdout=sub.PIPE, stderr=sub.PIPE)
		result, errors = p.communicate()

		for i in range(len(ntp_array)):
			logger.info('attempting to use ntpd for address: ' + ntp_array[i])
			ntpd_command = SynCommand('ntpd -dnq -p ' + ntp_array[i])
			output, errors = ntpd_command.run(5)
			logger.debug('Did we get a response?')
			logger.debug('output: ' + str(output))
			logger.debug('errors: ' + str(errors))
			
			if 'offset:' in str(errors):
				logger.info('Success! Starting up daemon and moving on')
				ntp_daemon = SynCommand('ntpd -p ' + ntp_array[i])
				output, errors = ntp_daemon.run(5)
				break
			elif i < (len(ntp_array) - 1):
				ntp_array.pop(i)
				logger.info('Failed. Trying the next from the list, i=' + str(i))
				continue

			# Fallback case
			logger.warning('Unable to sync with NTP servers')
			p = sub.Popen(['uci','set','system.ntp.enabled=0'], stdout=sub.PIPE, stderr=sub.PIPE)
			result, errors = p.communicate()
			return HTTPError(404, 'Error using NTP sync for all given addresses')


		for ntp_server in ntp_array:
			p = sub.Popen(['uci','add_list','system.ntp.server=' + ntp_server], stdout=sub.PIPE, stderr=sub.PIPE)
			result, errors = p.communicate()

		p = sub.Popen(['uci','set','system.ntp.enabled=1'], stdout=sub.PIPE, stderr=sub.PIPE)
		result, errors = p.communicate()

		p = sub.Popen(['uci','commit'], stdout=sub.PIPE, stderr=sub.PIPE)
		result, errors = p.communicate()

	else:
		# If 'time' ends in 'Z', use UTC. Otherwise, use whatever is in 'timeZone'
		if data['time'].endswith('Z'):
			time_zone = 'UTC'
		else:
			try:
				time_zone = data['timeZone']

			except KeyError:
				return HTTPError(404, 'Missing time zone')

		sub.Popen(['killall','-9','ntpd'])

		# Set Time Zone
		p = sub.Popen(['uci','set','system.@system[0].timezone=' + time_zone], stdout=sub.PIPE, stderr=sub.PIPE)
		timezone, errors = p.communicate()
		sub.Popen(['uci','commit'])

		# Format time for manual update
		if len(data['time']) < 19:
			new_date = data['time'] + ':00'
		else:
			new_date = data['time']

		linux_date = datetime.strptime(data['time'], DATETIME_FORMAT).strftime(LINUX_DATE_FORMAT)

		# Set system time
		p = sub.Popen(['date',linux_date], stdout=sub.PIPE, stderr=sub.PIPE)
		date, errors = p.communicate()

		p = sub.Popen(['uci','set','system.ntp.enabled=0'], stdout=sub.PIPE, stderr=sub.PIPE)
		result, errors = p.communicate()

	# Set hwclock to system time
	logger.info('Updating hwclock')
	p = sub.Popen(['hwclock','-w'], stdout=sub.PIPE, stderr=sub.PIPE)
	output, errors = p.communicate()

	try:
		token = request.get_header('token', None)
		touch_token(token)
	except:
		HTTPError(404, 'Unable to update session time')

	return get_system_time()


##### System - Enable/Disable SSH Access #####
@app.post(BASE_URL + '/shellAccess')
@csrf_check()
@auth_token(validate_token)
def update_shell_access():
	'''
	Update shell access
	'''
	data = ''
	try:
		data = request.json
		new_access = data['shellAccess']

	except ValueError:
		return HTTPError(404, 'Missing data')

	if new_access == True:
		dropbear_update = 'start'
	elif new_access == False:
		dropbear_update = 'stop'
	else:
		return HTTPError(404, 'Problem with request data')

	try:
		p = sub.Popen(['/etc/init.d/dropbear',dropbear_update], stdout=sub.PIPE, stderr=sub.PIPE)
		output, errors = p.communicate()
		time.sleep(0.2)
	except:
		return HTTPError(404, 'Unable to update SSH access')

	return {'shellAccess': flex.shell_access_enabled()}


##### System - Update WAC Name #####
@app.post(BASE_URL + '/wacName')
@csrf_check()
@auth_token(validate_token)
def update_wac_name():
	'''
	Update WAC name in avahi service file
	'''
	data = ''
	try:
		data = request.json
		if 'wacName' in data:
			new_wac_name = data['wacName']
		elif 'newWACName' in data:
			new_wac_name = data['newWACName']

	except ValueError:
		return HTTPError(404, 'Missing data')

	logger.info('Attempting to set hostname to: %s' % new_wac_name)

	if any(char not in VALID_CHARS for char in new_wac_name):
		return HTTPError(404, 'That hostname is not valid. Please use only letters, numbers, and hyphens.')

	logger.info('Valid hostname is: %s' % new_wac_name)

	try:
		logger.info('Setting hostname...')
		flex.update_avahi_name(new_wac_name.strip('-'))

	except:
		return HTTPError(404, 'Failed to update WAC name')

	return {
		'wacName': flex.get_avahi_name()
	}


##### System - Get Users #####
@app.get(BASE_URL + '/users')
@auth_token(validate_token)
def get_users():
	'''
	Return list of users
	'''

	return {
		'users': ldap.get_allowed_users()
	}


##### System - Update User Data #####
@app.post(BASE_URL + '/users')
@csrf_check()
@auth_token(validate_token)
def update_user():
	'''
	Update a single user password
	'''
	data = ''
	try:
		data = request.json
		user_name = data['userName']
		old_password = data['oldPassword']
		new_password = data['newPassword']

	except KeyError:
		return HTTPError(404, 'Missing data')

	if len(new_password) <= 6:
		return HTTPError(404, 'New password is too short')

	errors = ldap.change_user_password(user_name, old_password, new_password)

	if errors:
		return HTTPError(404, 'user update failed, ' + errors)
	else:

		return {
			'updated': True,
		}


##### System - Get Certificate Status #####
@app.get(BASE_URL + '/certificate')
@auth_token(validate_token)
def get_certificate_status():
	'''
	Return whether or not we're using a custom SSL certificate
	'''
	if os.path.exists(CUSTOM_CERT_FLAG):
		return True
	else:
		return False


##### System - Disable Custom Certificate #####
@app.post(BASE_URL + '/certificate')
@csrf_check()
@auth_token(validate_token)
def update_certificate_status():
	'''
	Enable/disable custom certificate
	- currently only available to disable the custom certificate
	'''
	data = ''
	try:
		data = request.json
		enable_custom_cert = data['enabled']

	except ValueError:
		return HTTPError(404, 'Missing data')

	if not enable_custom_cert:
		os.remove(CERTIFICATE_FILE)
		os.remove(CUSTOM_CERT_FLAG)
		shutil.copy(CERTIFICATE_BASE,CERTIFICATE_FILE)

		try:
			flex.restart_wavelinx()
		except:
			return HTTPError(404, 'Error restarting wavelinx')

	else:
		return HTTPError(404, 'Not allowing user-enabling of custom certificates')

	return {'customCertificate': False}


##### System - Upload and Enable Custom Certificate File #####
@app.post(BASE_URL + '/certificate/upload')
@csrf_check()
@auth_token(validate_token)
def upload_certificate_file():
	'''
	Upload custom certificate file
	'''
	if 'file' not in request.files:
		return HTTPError(404, 'No certificate uploaded')

	try:
		if not os.path.exists(CERTIFICATE_DIR):
			os.makedirs(CERTIFICATE_DIR)

		user_certificate = request.files.get('file')
		user_certificate.save(CERTIFICATE_FILE,overwrite=True)

	except:
		return HTTPError(404, 'Unable to save certificate file')

	try:
		flex.restart_wavelinx()
	except:
		return HTTPError(404, 'Error restarting wavelinx')

	if not os.path.exists(CUSTOM_CERT_FLAG):
		with open(CUSTOM_CERT_FLAG, 'w') as f:
			f.write(user_certificate.filename)

	return {'customCertificate': True}


##### System - Reboot the WAC #####
@app.post(BASE_URL + '/reboot')
@csrf_check()
@auth_token(validate_token)
def post_reboot_request():
	'''
	Reboot the WAC
	'''
	data = {}
	try:
		data = request.json
		do_reboot = data.get('reboot', False)

	except KeyError:
		return HTTPError(404, 'Missing data')

	if not do_reboot:
		return HTTPError(404, 'No reboot requested.')

	if flex.wac_updating():
		return HTTPError(404, 'WAC currently updating, reboot pending...')

	logger.info('Requesting reboot from platform manager')
	mqtt_publish.single('/platform/requests', 'reboot-wac', hostname=PLATFORM_BROKER)

	return {'rebooting': True}
