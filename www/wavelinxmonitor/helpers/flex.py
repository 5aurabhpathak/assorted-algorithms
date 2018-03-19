# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/flex
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import json
import logging
import os
import re
from shutil import move
import subprocess as sub
from tempfile import mkstemp
import urllib2

import delegator

from helpers.subproc import make_args, make_sub

logger = logging.getLogger(__name__)

AP_CONFIG_FILE = '/etc/wireless/mt7620/mt7620.dat'


def set_config_mode(counter):
	logger.info('Setting configMode counter to: ' + str(counter))
	try:
		with open('/var/configMode', 'w') as config_file:
			config_file.write(str(counter) + '\n')
	except Exception as err:
		logger.warning(repr(err))


def shell_access_enabled():
	'''
	Check if shell access enabled and listening on port 22
	'''
	proc_netstat = sub.Popen(['netstat', '-atn'], stdout=sub.PIPE, shell=False)
	proc_grep1 = sub.Popen(
		['grep', 'LISTEN'], stdin=proc_netstat.stdout, stdout=sub.PIPE, shell=False)
	proc_grep2 = sub.Popen(
		['grep', '22'], stdin=proc_grep1.stdout, stdout=sub.PIPE, shell=False)
	proc_netstat.stdout.close()
	proc_grep1.stdout.close()
	output, errors = proc_grep2.communicate()

	if output.strip('\n'):
		return True
	else:
		return False


def get_avahi_name():
	'''
	Return the string value of the <name> tag in the avahi service file
	'''
	get_hostname = make_sub(make_args('cat /proc/sys/kernel/hostname'))
	name = get_hostname.communicate()

	if name[0]:
		return name[0].strip('\n')
	else:
		raise


def update_avahi_name(new_name='EatonWAC'):
	try:
		logger.debug('Setting hostname with wac-set-hostname to %s' % new_name)
		set_hostname = make_sub(
			make_args('/usr/sbin/wac-set-hostname %s' % new_name.strip('\n')))
		set_hostname.communicate()
	except Exception as e:
		logger.warning('Problem updating hostname')
		logger.warning(repr(e))
		raise


def get_fw_version():
	'''
	Return contents of /database/otaValue text file
	'''
	try:
		with open('/database/otaValue', 'r') as ota_value:
			fw_version = ota_value.read().replace('\n', '')

	except IOError:
		fw_version = ''

	return fw_version


def get_wac_version():
	'''
	Return gateway version from CAPI
	'''
	try:
		response = urllib2.urlopen(
			'http://127.0.0.1:52825/v1/version', timeout=2)
		fw_build = json.load(response)
		return fw_build['firmwareVersion']

	except:
		return get_fw_version()


def get_zigbee_info():
	try:
		response = urllib2.urlopen('http://127.0.0.1:52825/v1/network')
		fw_build = json.load(response)
		return fw_build['firmwareVersion']

	except:
		raise


def ntp_enabled():
	'''
	Return T/F if NTP is enabled or not
	'''
	try:
		p = sub.Popen(['uci', 'get', 'system.ntp.enabled'],
					  stdout=sub.PIPE, stderr=sub.PIPE)
		ntp_enabled, errors = p.communicate()
		if '1' in ntp_enabled:
			return True
		else:
			return False
	except:
		return False


def ntp_servers():
	'''
	Return array of ntp servers from uci system.ntp.server
	'''
	try:
		proc_uci = sub.Popen(
			['uci', 'get', 'system.ntp.server'], stdout=sub.PIPE, shell=False)
		output, errors = proc_uci.communicate()
		if output:
			return output.strip('\n').split(' ')
		else:
			return []
	except:
		return []


def start_wavelinx():
	'''
	monit start wavelinx
	'''
	sub1 = make_sub(make_args('monit start wavelinx'))
	return sub1.communicate()


def stop_wavelinx():
	'''
	monit stop wavelinx
	'''
	sub1 = make_sub(make_args('monit stop wavelinx'))
	return sub1.communicate()


def restart_wavelinx():
	'''
	monit stop wavelinx
	'''
	sub1 = make_sub(make_args('monit restart wavelinx'))
	return sub1.communicate()


def wac_updating():
	'''
	Return whether or not applyOta.sh is currently running
	- the grep -q flag returns a 0 for found and 1 for not found
	'''
	cmd = delegator.run('ps').pipe('grep -q applyOta.sh')
	return not bool(cmd.return_code)


# def get_ap_ssid():
# 	SSID_KEY = 'SSID1'
# 	regex = re.compile(r"^%s=.*" % SSID_KEY)
# 	with open(AP_CONFIG_FILE, 'r') as ap_file:
# 		for line in ap_file:
# 			if line.startswith(SSID_KEY):
# 				return regex.sub(line)


# def ap_is_enabled():
#     return


def update_ap_key(new_key='wclAdmin'):
	'''
	Update the Wi-FI AP key
	'''
	logger.debug('Updating Wi-Fi AP key to %s', new_key)
	regex = re.compile(r"^WPAPSK1=.*")
	fh, abs_path = mkstemp()

	with os.fdopen(fh, 'w') as new_file:
		with open(AP_CONFIG_FILE, 'r') as old_file:
			for line in old_file:
				new_line = regex.sub("WPAPSK1=%s" % new_key, line)
				new_file.write(new_line)

	logger.debug('Removing old %s', AP_CONFIG_FILE)
	os.remove(AP_CONFIG_FILE)
	logger.debug('Renaming new file to %s', AP_CONFIG_FILE)
	move(abs_path, AP_CONFIG_FILE)

	return
