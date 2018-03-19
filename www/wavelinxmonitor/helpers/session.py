# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/session
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""

import time
import pickle
import os
import uuid

class Session(object):
	'''
	Class which implements some of the basic functionality required for
	session managers.

	:param expires: Expiration time of session ID token, either `None`
			if it is not to expire, a number of seconds in the future,
			or a datetime object.  (default: 30 minutes)
	:param session_dir: Directory that session information is stored in.
			(default: ``'/tmp'``).
	'''
	def __init__(self, expires=60*30, session_dir='/tmp'):
		self.expires = expires
		self.session_dir = session_dir

	def load(self, sessionid):
		filename = os.path.join(self.session_dir, 'session-%s' % sessionid)
		if not os.path.exists(filename):
			return None
		with open(filename, 'r') as fp:
			session = pickle.load(fp)
		return session

	def save(self, data):
		sessionid = data['sessionid']
		fileName = os.path.join(self.session_dir, 'session-%s' % sessionid)
		tmpName = fileName + '.' + str(uuid.uuid4().hex)
		with open(tmpName, 'w') as fp:
			self.session = pickle.dump(data, fp)
		os.rename(tmpName, fileName)

	def remove(self, sessionid):
		fileName = os.path.join(self.session_dir, 'session-%s' % sessionid)
		os.remove(fileName)

	def make_session_id(self):
		return str(uuid.uuid4().hex)

	def allocate_new_session_id(self):
		#  retry allocating a unique sessionid
		sessionid = self.make_session_id()
		for i in range(100):
			if not self.load(sessionid):
				return sessionid
		raise ValueError('Unable to allocate unique session')

	def new_session(self, user_level, sessionid=None):
		if not sessionid:
			sessionid = self.allocate_new_session_id()

		data = {
			'sessionid': sessionid,
			'time': int(time.time()),
			'userLevel': user_level,
			'valid': True
		}

		self.save(data)

		return sessionid

	def get_session(self, token=None):
		sessionid = token
		now = int(time.time())
		# get existing or create new session identifier
		if not token:
			sessionid = self.allocate_new_session_id()

		# load existing session
		data = self.load(sessionid)
		time_delta = now - data['time']

		# sessionid doesn't exist
		if not data:
			data = {
				'sessionid': sessionid,
				'time': int(time.time()),
				'userLevel': '',
				'valid': False
			}
			return data

		# expired session
		elif time_delta > self.expires:
			data['valid'] = False
			self.remove(sessionid)
			return data

		# not expired, update session
		data['time'] = int(time.time())
		self.save(data)
		return data

	def touch_session(self, token=None):
		sessionid = token
		now = int(time.time())
		# get existing or create new session identifier
		if not token:
			sessionid = self.allocate_new_session_id()

		# load existing session
		data = self.load(sessionid)

		# sessionid doesn't exist
		if not data:
			data = {
				'sessionid': sessionid,
				'time': int(time.time()),
				'userLevel': '',
				'valid': False
			}
			return data

		# update session
		data['time'] = int(time.time())
		self.save(data)
		return data

	def end_session(self, token=None):
		sessionid = token

		# load existing session
		data = self.load(sessionid)
		# expired session
		self.remove(sessionid)

		return data
