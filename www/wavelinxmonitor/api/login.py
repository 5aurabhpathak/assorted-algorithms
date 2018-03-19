# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/login
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import logging

import bottle
from bottle import request, HTTPError

from helpers.auth import validate_login, invalidate_token, get_token, csrf_check
from helpers.lockout import Lockout

app = application = bottle.default_app()
lockout_mgr = Lockout()
logger = logging.getLogger(__name__)

# Load Configuration Constants
API_VERSION = app.config['wlm.api_version']

# Derived Constants
BASE_URL = '/' + API_VERSION + '/authentication'

##### Login #####
@app.post(BASE_URL + '/login')
def post_login():
	'''
	Receive and validate login
	'''
	data = ''
	try:
		data = request.json
		user_name = data['userName']
		password = data['password']

	except KeyError:
		return HTTPError(404, 'Missing login credentials')
	
	try:
		logger.info('User logging in: ' + user_name)
		login_is_validated = validate_login(user_name, password)
	except:
		logger.debug(user_name + ' login validation error')
		return HTTPError(404, 'Login failed')

	try:
		account_locked = lockout_mgr.check(user_name)
	except:
		logger.debug('Lockout manager error, account locked: ' + user_name)
		return HTTPError(404, 'Login failed')

	if account_locked:
		logger.info('Account locked: ' + user_name)
		return HTTPError(404, 'Too many failed logins, account locked')
	else:
		if login_is_validated:
			lockout_mgr.success(user_name)
			token, level = get_token(user_name)
			logger.info(user_name + ' login success')
			logger.info('Token: '+ token)
			return {
				'token': token,
				'userType': level
			}
		else:
			data = lockout_mgr.failed(user_name)
			logger.info('Invalid credentials for: ' + user_name)
			return HTTPError(404, 'Invalid credentials')


##### Logout #####
@app.post(BASE_URL + '/logout')
@csrf_check()
def post_logout():
	session = invalidate_token()
	logger.info('Logout success')

	return
