# -*- coding: utf-8 -*-
"""
darkcapi
~~~~~~~~~~
A DarkCAPI interface helper class


Features:
	- 

Usage:
    >>> from darkcapi import DarkCapi

	>>> dark_capi = DarkCapi()

	# Get object list, find an object, and update that object
	>>> dark_capi.get_oid_list()
	>>> zigbee_nw_manager = dark_capi.oidref['NetworkManager'][0]
	>>> req_body = {
			'~restoreZigBeeNetwork': 1
		}
	>>> dark_capi.update_oid(zigbee_nw_manager, req_body)

"""
from datetime import datetime, timedelta
import json
import logging
import threading
import timeit

import requests
import websocket

logger = logging.getLogger(__name__)


class DarkCapi(object):
	'''
	Class which opens a Dark CAPI session and handles requests
	'''
	def __init__(self, ip_address='127.0.0.1:52825/'):
		# URL Structures
		self.version = 'v1'
		self.self_ipaddr = ip_address
		self.base_api_url = ''.join(['http://',self.self_ipaddr,self.version])
		self.base_ws_url = ''.join(['ws://',self.self_ipaddr])

		# Configuration
		self.request_timeout = 10 # seconds
		self.session_timeout = 30 # minutes

		# Initialize properties
		self.oidref = {}
		self.cred = {}
		self.last_request_time = None
		self.logged_in = False
		self.login()


	#########################
	# DarkCAPI API Helpers
	#########################
	def handleRequest(self, url, opts):
		try:
			# Form and send request
			if opts['method'] == 'post':
				req = requests.post(
					url,
					headers = opts['header'],
					data = json.dumps(opts['data']),
					timeout = self.request_timeout
					)
			elif opts['method'] == 'put':
				req = requests.put(
					url,
					headers = opts['header'],
					data = json.dumps(opts['data']),
					timeout = self.request_timeout
					)
			elif opts['method'] == 'patch':
				req = requests.patch(url,
				headers = opts['header'],
				data = json.dumps(opts['data']),
				timeout = self.request_timeout
				)
			elif opts['method'] == 'delete':
				req = requests.delete(url,
				headers = opts['header'],
				data = json.dumps(opts['data']),
				timeout = self.request_timeout
				)
			else:
				req = requests.get(
					url,
					headers = opts['header'],
					timeout = self.request_timeout
					)

			# Handle response
			if str(req) == '<Response [200]>':
				logger.debug('Request good %s',req)
				try:
					response = req.json()
					logger.debug('JSON response')
					return response
				except:
					logger.debug('no json object')
					return ''
				
			elif str(req) == '<Response [404]>':
				logger.debug('Request error %s',req)

				try:
					response = req.json()
					if response['errorCode'] == 'WCL.AUTH.E.0201':
						logger.debug('Auth error, logged_in state to False')
						self.logged_in = False
						self.cred={}
						self.ws.close()

						if self.current_api_request:
							logger.debug('Session was invalid, log in and try again')
							return self.api(self.current_api_request)

					logger.debug('JSON response')
					return response

				except:
					logger.debug('no json object')
					return ''
			else:
				logger.debug('Unknown response %s',req)
				return req

		except requests.exceptions.Timeout:
			logger.info('request failed: timeout')

		except requests.exceptions.TooManyRedirects:
			logger.info('request failed: too many redirects')

		except requests.exceptions.RequestException as e:
			logger.info('request failed %r',e)


	def login(self, user='DarkCAPI', pw='IamBatmanCunningham!'):
		logger.debug('Logging into CAPI as %s' % user)
		opts = {}
		opts['header'] = None
		opts['method'] = 'post'
		opts['data'] = {
			'userName': user,
			'password': pw
		}
		currentUrl = ''.join([self.base_api_url,'/authentication/login'])

		try:
			r = self.handleRequest(currentUrl, opts)
			responseObj = r
			self.cred['token'] = responseObj['token']
			self.cred['userType'] = responseObj['userType']
			logger.info('Logged into CAPI as: %s',user)
			self.logged_in = True

		except:
			logger.info('CAPI Login failed')
			self.logged_in = False

	def logout(self):
		opts = {}
		opts['header'] = {}
		opts['header']['token'] = self.cred['token']
		opts['method'] = 'post'
		opts['data'] = {}
		current_url = ''.join([self.base_api_url,'/authentication/logout'])

		try:
			r = self.handleRequest(current_url, opts)
			responseObj = r
			logger.debug(repr(responseObj))
			self.logged_in = False

		except:
			logger.info('CAPI logout failed')

	def api(self, opts):
		if not self.logged_in:
			self.login()

		if 'header' not in opts: opts['header'] = {}
		opts['header']['token'] = self.cred['token']
		if 'url' not in opts: opts['url'] = '/'
		currentUrl = ''.join([self.base_api_url,opts['url']])

		logger.info('Request to: %s',opts['url'])
		logger.debug('API request, opts: %s',json.dumps(opts, indent=4))
		start_time = timeit.default_timer()

		try:
			r = self.handleRequest(currentUrl, opts)
			elapsed = timeit.default_timer() - start_time
			logger.info('Response from: %s|%s',opts['url'],json.dumps(r, indent=4))
			logger.info('Request time: %ss',elapsed)
			logger.debug('Clear current API request')
			self.current_api_request={}
			return r

		except:
			elapsed = timeit.default_timer() - start_time
			logger.info('Request to %s failed',opts['url'])
			logger.info('Request time: %ss',elapsed)
			logger.debug('Clear current API request')
			self.current_api_request={}


	#########################
	# Websocket core methods
	#########################
	def ws_on_open(self, ws):
		ws_login = {
			"id":"cloud_manager",
			"method":"authenticate",
			"params":{
				"data":{
					"token": self.cred['token']
				}
			},
			"jsonrpc":"2.0"
		}
		ws.send(json.dumps(ws_login))

		return None


	def ws_init(self, ws_on_message, ws_on_error, ws_on_close):
		'''
		ex:
		def on_message(ws, message):
			logger.info(message)

		def on_error(ws, error):
			logger.info(error)

		def on_close(ws):
			logger.info("### closed ###")
		'''
		try:
			self.ws = websocket.WebSocketApp(self.base_ws_url,
										on_message = ws_on_message,
										on_error = ws_on_error,
										on_close = ws_on_close)
			self.ws.on_open = self.ws_on_open
			wst = threading.Thread(target = self.ws.run_forever)
			wst.daemon = True
			wst.start()
			logger.info('Websocket connection successful')

			return None
		except:
			logger.info('Websocket connection failed')


	def ws_subscribe_objects(self, class_names=[], update_oids=False):
		'''
		class_names is a list of DarkCAPI object "Names"
		'''
		oid_array = []
		if not self.oidref or update_oids:
			self.get_oid_list()

		for class_name in class_names:
			oid_array.extend(self.oidref[class_name])

		sub_body = {
			"actions" : {
				"actions" : [
					{
						"action" : {
							"subscribe" : {
								"objects": oid_array
							}
						},
						"sequenceNumber" : 1
					}
				]
			},
			"event" : "EXECUTE",
			"isManual" : True
		}

		opts = {}
		opts['method'] = 'post'
		opts['url'] = '/exec'
		opts['data'] = sub_body

		logger.info('Subscribing to objects: %s',oid_array)
		return self.api(opts)


	#########################
	# DarkCAPI Core Methods
	#########################
	def get_oid_list(self):
		opts = {}
		opts['method'] = 'get'
		opts['url'] = '/oidlist'
		self.current_api_request = opts

		oidlist = self.api(opts)

		self.oidref = {}
		for k,v in oidlist.items():
			self.oidref.setdefault(str(v),list()).append(int(k))

		return oidlist


	def get_oid(self, oid):
		opts = {}
		opts['method'] = 'get'
		opts['url'] = ''.join(['/oid/',str(oid)])
		self.current_api_request = opts

		return self.api(opts)


	def update_oid(self, oid, body):
		opts = {}
		opts['method'] = 'patch'
		opts['url'] = ''.join(['/oid/',str(oid)])
		opts['data'] = body
		self.current_api_request = opts

		return self.api(opts)


	def get_object(self, name):
		oid = self.oidref[name][0]
		opts = {}
		opts['method'] = 'get'
		opts['url'] = ''.join(['/oid/',str(oid)])
		self.current_api_request = opts

		return self.api(opts)


	def update_object(self, name, body):
		oid = self.oidref[name][0]
		opts = {}
		opts['method'] = 'patch'
		opts['url'] = ''.join(['/oid/',str(oid)])
		opts['data'] = body
		self.current_api_request = opts

		return self.api(opts)


def ws_handle_callback(ws, message):
	logger.debug('Received websocket message: %s' % message)
	logger.debug('From websocket: %r' % ws)

def ws_handle_error(ws, error):
	logger.debug('Websocket ERROR: %s' % error)
	logger.debug('From websocket: %r' % ws)

def ws_handle_close(ws):
	logger.debug('Websocket closed: %r' % ws)


# Create default DarkCAPI class so we don't have to instantiate a bunch of them...
logger.debug('Creating default DarkCAPI instance')
default_dc = DarkCapi()

try:
	logger.debug('Initiating websocket connection to keep session active')
	default_dc.ws_init(ws_handle_callback, ws_handle_error, ws_handle_close)
except:
	logger.debug('Unable to initiate websocket connection')


# Expose all webservice methods
def get_oid_list():
	return default_dc.get_oid_list()

def get_oid(oid):
	return default_dc.get_oid(oid)

def update_oid(oid, body):
	return default_dc.update_oid(oid, body)

def get_object(name):
	return default_dc.get_object(name)

def update_object(name, body):
	return default_dc.update_object(name, body)

def find_oid(name):
	if not default_dc.oidref:
		default_dc.get_oid_list()
	return default_dc.oidref[name][0]

def find_oids(name):
	if not default_dc.oidref:
		default_dc.get_oid_list()
	return default_dc.oidref[name]
