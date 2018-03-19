# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/auth
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import base64
import functools
import hashlib
import logging
import os
import subprocess as sub

import bottle
from bottle import request, HTTPError

from helpers import ldap
from helpers.session import Session

app = application = bottle.default_app()
logger = logging.getLogger(__name__)
session_manager = Session()

# Load Configuration Constants
CSRF_CHECK = app.config['wlm.csrf_check']
LOGIN_USER_LEVEL = int(app.config['wlm.login_user_level'])

def user_level(user):
	user_level = 0

	if user == 'WclUser':
		user_level = 1
	elif user == 'WclAdmin':
		user_level = 2
	elif user in ('DarkCAPI', 'WclWeb'):
		user_level = 3
	else:
		user_level = 0

	return user_level

def csrf_check(text="Not allowed"):
	'''
	Decorator to enable CSRF-checking for incoming API POST requests
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*a, **ka):
			request_ref = request.get_header('Referer') or None
			request_host = request.get_header('Host')

			logger.debug('csrf_check value: %s',CSRF_CHECK)

			if str(request_host) not in str(request_ref) and CSRF_CHECK.lower() == 'true':
				return HTTPError(403, text)
			return func(*a, **ka)
		return wrapper
	return decorator

def auth_token(check, realm="private", text="Access denied"):
	'''
	Decorator to enable token-checking for incoming API requests
	- Takes a function "check" that should return True or False
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*a, **ka):
			token = request.get_header('token', None)
			if token is None or not check(token):
				err = HTTPError(401, text)
				return err
			return func(*a, **ka)
		return wrapper
	return decorator

def get_token(user):
	'''
	Creates a token for a new session
	'''	
	level = user_level(user)
	logger.info('Starting new session for user: ' + user)
	return (session_manager.new_session(level), level)

def validate_token(token):
	'''
	Checks if the token is for a valid session
	'''
	try:
		session = session_manager.get_session(token)
		usr_level = session['userLevel']

		if usr_level >= LOGIN_USER_LEVEL:
			return session['valid']
		else:
			return False

	except:
		return False

def touch_token(token):
	'''
	Update time for a valid session
	'''
	try:
		session = session_manager.touch_session(token)
		usr_level = session['userLevel']
		logger.debug('Updating session for token: ' + token)

		if usr_level >= LOGIN_USER_LEVEL:
			logger.debug('Success updating session')
			return session['valid']
		else:
			logger.debug('User level not appropriate')
			return False

	except:
		logger.debug('Exception while getting session info')
		return False

def invalidate_token():
	'''
	Makes a session invalid
	'''
	token = request.get_header('token', None)
	session = session_manager.end_session(token)
	logger.info('Marking session invalid, token: ' + token)
	return session


def validate_login(user_name, password, level=LOGIN_USER_LEVEL):
	'''
	Verifies login of the WclAdmin user only (for now)
	'''
	try:
		logger.info('Validating user...')
		login_is_validated = ldap.validate_login(user_name, password)
		logger.info('Checking user level...')
		usr_level = user_level(user_name)

		if login_is_validated and (usr_level >= level):
			logger.info('User: ' + str(user_name) + ' login validated')
			return True
		else:
			logger.info('User: ' + user_name + ' login not validated')
			logger.debug('User level: ' + str(usr_level))
			logger.debug('Login validated: ' + str(login_is_validated))
			return False

	except:
		logger.debug('Exception while validating user: ' + user_name)
		return False
