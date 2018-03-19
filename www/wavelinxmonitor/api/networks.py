# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/networks
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import json
import logging
import os
import socket
import subprocess as sub
import time

import bottle
from bottle import request, HTTPError

from helpers.auth import auth_token, validate_token, csrf_check
from helpers import filemanager
from helpers.flex import set_config_mode, update_ap_key

app = application = bottle.default_app()
logger = logging.getLogger(__name__)

# Load Configuration Constants
API_VERSION = app.config['wlm.api_version']
WIFI_CONFIG_FILE = '/storage/wifi-config'
WIFI_AP_CONFIG = '/etc/wireless/mt7620/mt7620.dat'
CONFIG_MODE_TIME = 1

# Derived Constants
BASE_URL = '/' + API_VERSION + '/networks'
BASH_ESC_CHARS = ('$', '`')
INVALID_SSID_CHARS = ('+', ']', '/', '"', '\t', '\n', '\v', '\r')
INVALID_SSID_START = ('!', '#', ';')


class WifiException(Exception):
	pass


def check_wifi_ssid(user_ssid=''):
	'''
	Validate wifi data based on
	- doesn\'t start with !, #, ;
	- doesn\'t end with a space
	- doesn\'t contain +, ], /, ", TAB, LF, VT, CR
	- up to 32 characters
	'''	
	if any(char in user_ssid for char in INVALID_SSID_CHARS):
		raise WifiException('Wi-Fi SSID invalid character(s)')

	if any(user_ssid.startswith(char) for char in INVALID_SSID_START):
		raise WifiException('Wi-Fi SSID cannot start with with !, #, or ;')

	if user_ssid.endswith(' '):
		raise WifiException('Wi-Fi SSID cannot end with a space')

	return


def check_wifi_auth(auth, encryp):
	'''
	Validate wifi auth/encryption
	'''

	try:
		if auth == 'OPEN':
			assert encryp in ('NONE', 'WEP')
		elif auth == 'SHARED':
			assert encryp in ('WEP')
		elif auth in ('WPAPSK', 'WPA2PSK'):
			assert encryp in ('TKIP', 'AES')
	
	except AssertionError as err:
		logger.exception(err)
		raise WifiException('Invalid Authentication/Encryption combination')

	return


def escape_bash(dangerous_string):
	'''
	Escape bash characters: $, `
	'''
	try:
		new_string = dangerous_string.replace('$', '\\$')
		good_string = new_string.replace('`', '\\`')
		return good_string

	except:
		raise


def set_wifi_config(ssid='',password='',channel='',authentication='', encryption=''):

	try:
		wifi_file = open(WIFI_CONFIG_FILE, 'w')
		logger.info('Writing wifi-config file...')

		logger.info('SSID=' + str(ssid))
		wifi_file.write('SSID="' + str(ssid) + '"\n')

		logger.info('WIFIKEY=' + str(password))
		wifi_file.write('WIFIKEY="' + str(password) + '"\n')

		logger.info('CHANNEL=' + str(channel))
		wifi_file.write('CHANNEL="' + str(channel) + '"\n')

		logger.info('AUTHENTICATION=' + str(authentication))
		wifi_file.write('AUTHENTICATION="' + str(authentication) + '"\n')

		logger.info('ENCRYPTION=' + str(encryption))
		wifi_file.write('ENCRYPTION="' + str(encryption) + '"\n')

		wifi_file.close()
		return

	except IOError as err:
		logger.exception(err)
		return

def get_wifi_config():
	logger.info('Reading wifi-config data...')
	if os.path.exists(WIFI_CONFIG_FILE):
		try:
			with open(WIFI_CONFIG_FILE, 'r') as wifi_config:
				wifi_content = wifi_config.readlines()
				if wifi_content:
					wifi_data = [s.strip().split('=') for s in wifi_content]
					wifi_object = {}
					for element in wifi_data:
						wifi_object[element[0]] = element[1].strip('"')

					logger.info('Found wifi-config data: ' + json.dumps(wifi_object, indent=4))
					return wifi_object

				else:
					logger.info('Nothing there')
					return {}
		except IOError:
			logger.info('IOError')
			return {}
	else:
		logger.info('No wifi-config file')
		return {}

##### Networks - Get Networks #####
@app.get(BASE_URL)
@auth_token(validate_token)
def get_networks():
	'''
	Return all network info
	'''
	logger.info('Retrieving all network data')
	return {
		'current': get_current_network(),
		'ethernet': get_ethernet_network(),
		'wifi': get_wifi_network(),
		'wifiAp': get_wifi_ap()
	}


##### Networks - Current Network #####
@app.get(BASE_URL + '/current')
@auth_token(validate_token)
def get_current_network():
	'''
	Return current network being used
	'''
	logger.info('Retrieving current network being used (nothing, currently)')
	return ''


##### Networks - Get Ethernet Network #####
@app.get(BASE_URL + '/ethernet')
@auth_token(validate_token)
def get_ethernet_network():
	'''
	Return current Ethernet network configuration
	'''
	logger.info('Getting current ethernet network settings')

	p = sub.Popen(['uci','get','network.wan.proto'], stdout=sub.PIPE, stderr=sub.PIPE)
	ethernet_dhcp, errors = p.communicate()
	logger.debug('eth0.2 proto: %s', ethernet_dhcp.strip('\n'))

	p = sub.Popen(['bash','-c','. /usr/sbin/nwFunctions.sh; get_ip eth0.2'], stdout=sub.PIPE, stderr=sub.PIPE)
	ethernet_ip, errors = p.communicate()
	logger.debug('eth0.2 IP: %s', ethernet_ip.strip('\n'))

	p = sub.Popen(['bash','-c','. /usr/sbin/nwFunctions.sh; get_netmask eth0.2'], stdout=sub.PIPE, stderr=sub.PIPE)
	ethernet_nm, errors = p.communicate()
	logger.debug('eth0.2 netmask: %s', ethernet_nm.strip('\n'))
	
	p = sub.Popen(['bash','-c','. /usr/sbin/nwFunctions.sh; get_gateway eth0.2'], stdout=sub.PIPE, stderr=sub.PIPE)
	ethernet_gw, errors = p.communicate()
	logger.debug('eth0.2 gateway: %s', ethernet_gw.strip('\n'))

	isDhcp = True if ethernet_dhcp.strip('\n') == 'dhcp' else False

	return {
		'isDhcp': isDhcp,
		'ipAddress': ethernet_ip.strip('\n'),
		'netMask': ethernet_nm.strip('\n'),
		'gateway': ethernet_gw.strip('\n')
	}


##### Networks - Update Ethernet Network #####
@app.post(BASE_URL + '/ethernet')
@csrf_check()
@auth_token(validate_token)
def update_ethernet_network():
	'''
	Set Ethernet network configuration
	'''
	data = ''
	try:
		data = request.json
		isDhcp = data.pop('isDhcp')

		logger.info('Ethernet configuration data: ' + json.dumps(data, indent=4))

		if not isDhcp:
			ipaddr = data['ipAddress']
			netmask = data['netMask']
			gateway = ''
			if data['gateway'] != '0.0.0.0':
				gateway = data['gateway']

	except KeyError:
		return HTTPError(404, 'Missing data')

	try:
		os.remove('/tmp/resolv.conf')
	except OSError:
		pass

	try:
		if isDhcp:
			logger.info('Configuring DHCP network settings, set config mode flag to %s',CONFIG_MODE_TIME)
			set_config_mode(CONFIG_MODE_TIME)
			p = sub.Popen(['ifconfig','eth0.2','up'])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.proto=dhcp'])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.ipaddr='])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.netmask='])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.gateway='])
			result, errors = p.communicate()
			p = sub.Popen(['uci','commit'])
			result, errors = p.communicate()
			# TODO: fork this to handle failed DHCP-getting
			p = sub.Popen(['udhcpc','-i','eth0.2','-t','5','-n'], stdout=sub.PIPE, stderr=sub.PIPE)
			result, errors = p.communicate()

		else:
			for name, maybe_ip in data.iteritems():
				logger.debug('Checking if %s is a valid IPv4 address', name)
				try:
					socket.inet_aton(maybe_ip)
					logger.debug('Valid IP address: %s', maybe_ip)
				except socket.error as err:
					logger.exception(err)
					logger.warning('Invalid IP address: %s', maybe_ip)
					return HTTPError(404, 'Invalid IPv4 address given for %s' % name)

			if ipaddr.startswith('192.168.100.'):
				return HTTPError(404, 'Setting IP to 192.168.100.1/24 subnet is not allowed.')

			logger.info('Configuring static network settings, set config mode flag to %s',CONFIG_MODE_TIME)
			set_config_mode(CONFIG_MODE_TIME)
			p = sub.Popen(['ifconfig','eth0.2','up'])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.proto=static'])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.ipaddr=' + ipaddr])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.netmask=' + netmask])
			result, errors = p.communicate()
			p = sub.Popen(['uci','set','network.wan.gateway=' + gateway])
			result, errors = p.communicate()
			p = sub.Popen(['uci','commit'])
			result, errors = p.communicate()
			logger.info('Reloading network settings')
			p = sub.Popen(['/etc/init.d/network','reload'], stdout=sub.PIPE, stderr=sub.PIPE)
			result, errors = p.communicate()

		logger.info('Restarting avahi...')
		p = sub.Popen(['/etc/init.d/avahi-daemon','reload'], stdout=sub.PIPE, stderr=sub.PIPE)
		result, errors = p.communicate()

	except Exception as err:
		logger.warning(repr(err))
		return HTTPError(404, 'Unable to connect')

	remove_wifi_network()
	
	return get_ethernet_network()


##### Networks - Get Wi-Fi Network #####
@app.get(BASE_URL + '/wifi')
@auth_token(validate_token)
def get_wifi_network():
	'''
	Return current Wi-Fi network configuration
	'''
	logger.info('Getting current Wi-Fi network settings')

	p = sub.Popen(['bash','-c','. /usr/sbin/nwFunctions.sh; get_ip apcli0'], stdout=sub.PIPE, stderr=sub.PIPE)
	wifi_ip, errors = p.communicate()
	logger.debug('apcli0 IP: %s', wifi_ip.strip('\n'))

	p = sub.Popen(['bash','-c','. /usr/sbin/nwFunctions.sh; get_netmask apcli0'], stdout=sub.PIPE, stderr=sub.PIPE)
	wifi_nm, errors = p.communicate()
	logger.debug('apcli0 netmask: %s', wifi_nm.strip('\n'))
	
	p = sub.Popen(['bash','-c','. /usr/sbin/nwFunctions.sh; get_gateway apcli0'], stdout=sub.PIPE, stderr=sub.PIPE)
	wifi_gw, errors = p.communicate()
	logger.debug('apcli0 gateway: %s', wifi_gw.strip('\n'))

	isDhcp = True # if ethernet_dhcp.strip('\n') == 'dhcp' else False # some other time, maybe

	wifi_config = get_wifi_config()

	return {
		'isDhcp': isDhcp,
		'ipAddress': wifi_ip.strip('\n'),
		'netMask': wifi_nm.strip('\n'),
		'gateway': wifi_gw.strip('\n'),
		'ssid': wifi_config.get('SSID',''),
		'authentication': wifi_config.get('AUTHENTICATION',''),
		'encryption': wifi_config.get('ENCRYPTION',''),
		'channel': wifi_config.get('CHANNEL','')
	}


##### Networks - Update Wi-Fi Network #####
@app.post(BASE_URL + '/wifi')
@csrf_check()
@auth_token(validate_token)
def update_wifi_network():
	'''
	Set Wi-Fi network configuration
	'''
	data = ''
	try:
		data = request.json

		logger.info('Wi-Fi configuration data: ' + json.dumps(data, indent=4))

		ssid = data['ssid']
		password = data.get('password', '')
		channel = data.get('channel', '')
		authentication = data.get('authentication', '')
		encryption = data.get('encryption', '')

	except KeyError:
		return HTTPError(404, 'Missing data')

	try:
		check_wifi_ssid(ssid)
		check_wifi_auth(authentication, encryption)

		# Escape bash chars
		escaped_ssid = escape_bash(ssid)
		escaped_pw = escape_bash(password)

	except WifiException as err:
		logger.exception('Wi-Fi cred exception: %s', err)
		return HTTPError(404, err.message)
	
	except Exception as err:
		logger.exception(err)
		return HTTPError(404, 'Wi-Fi setup failed')

	try:
		set_config_mode(CONFIG_MODE_TIME)
		set_wifi_config(
			ssid=escaped_ssid,
			password=escaped_pw,
			channel=channel,
			authentication=authentication,
			encryption=encryption
		)
		time.sleep(0.1)
		logger.info('Turn on apcli0 for Wi-Fi client')
		sub.Popen(['ifconfig','apcli0','up'])
		logger.info('Running wifi init script to try Wi-Fi connection')
		p = sub.Popen(['/etc/init.d/wifi','start'], stdout=sub.PIPE, stderr=sub.PIPE)
		wifi_connection, errors = p.communicate()

		if "Failed to Connect to the given WiFi SSID" not in wifi_connection:
			logger.info('Looks like we connected to ssid: ' + str(ssid))
			sub.Popen(['/root/wifi/udhcpc.sh'])
			sub.Popen(['/etc/init.d/avahi-daemon','reload'])
		else:
			logger.info('Failed to connect to Wi-Fi network, removing wifi-config file')
			os.remove(WIFI_CONFIG_FILE)
			return HTTPError(404, 'Unable to connect to Wi-Fi network: ' + ssid)

	except RuntimeError:
		return HTTPError(404, 'Wi-Fi connection failed')

	return get_wifi_network()


##### Networks - Remove Wi-Fi Network Configuration #####
@app.delete(BASE_URL + '/wifi')
@csrf_check()
@auth_token(validate_token)
def remove_wifi_network():
	'''
	Remove Wi-Fi network configuration
	'''
	if os.path.exists(WIFI_CONFIG_FILE):
		set_config_mode(CONFIG_MODE_TIME)
		logger.info('ConfigMode set to  %i, removing wifi-config file', CONFIG_MODE_TIME)
		os.remove(WIFI_CONFIG_FILE)
		try:
			os.remove('/tmp/resolv.conf')
		except OSError:
			pass
	
	return {}


##### Networks - Get Wi-Fi AP Info #####
@app.get(BASE_URL + '/wifiAp')
@auth_token(validate_token)
def get_wifi_ap():
	'''
	Return current Wi-Fi AP configuration
	'''
	logger.info('Getting current Wi-Fi network settings')

	ap_config = filemanager.update_values_json(WIFI_AP_CONFIG)
	ap_ssid = ap_config['SSID1']
	# ap_enabled = flex.ap_is_enabled()

	return {
		'enabled': True,
		'ssid': ap_ssid
	}

##### Networks - Update Wi-Fi Network #####
@app.post(BASE_URL + '/wifiAp')
@csrf_check()
@auth_token(validate_token)
def update_wifi_ap():
	'''
	Set Wi-Fi network configuration
	'''
	data = ''
	try:
		data = request.json
		nwk_key = data.get('networkKey', 'wclAdmin')

	except KeyError:
		return HTTPError(404, 'Missing data')

	try:
		# set the network key
		update_ap_key(nwk_key)
		# reload network???
		return

	except Exception as err:
		logger.exception(err)
		return HTTPError(404, 'Error updating Wi-Fi AP info')
