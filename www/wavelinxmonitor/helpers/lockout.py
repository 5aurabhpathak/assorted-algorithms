# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/lockout
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

class Lockout(object):
	'''
	Class which implements basic account lockout.
	
	:param attempts: Number of attempts before lockout.
	:param expires: Expiration time before login is allowed.  (default: 5 minutes)
	:param lockout_dir: Directory that account information is stored in.
			(default: ``'/tmp'``).
	'''
	def __init__(self, attempts=5, expires=60*5, lockout_dir='/tmp'):
		self.attempts = attempts
		self.expires = expires
		self.lockout_dir = lockout_dir

	def load(self, account):
		filename = os.path.join(self.lockout_dir, 'account-%s' % account)
		if not os.path.exists(filename):
			return None
		with open(filename, 'r') as fp:
			account = pickle.load(fp)
		return account

	def save(self, data):
		account = data['account']
		fileName = os.path.join(self.lockout_dir, 'account-%s' % account)
		tmpName = fileName + '.' + str(uuid.uuid4())
		with open(tmpName, 'w') as fp:
			self.account = pickle.dump(data, fp)
		os.rename(tmpName, fileName)

	def check(self, account=None):
		data = self.load(account)
		now = int(time.time())
		lockout = False

		if not data:
			return lockout

		attempts = data['failedAttempts']
		lockout = data['lockout']
		exp_time = now - data['time']

		if exp_time > self.expires:
			lockout = False

		return lockout

	def failed(self, account=None):
		data = self.load(account)
		now = int(time.time())

		if not data:
			data = {
				'account': account,
				'time': 0,
				'failedAttempts': 0,
				'lockout': False
			}

		attempts = data['failedAttempts'] + 1
		data['failedAttempts'] = attempts
		data['time'] = int(time.time())

		if attempts >= self.attempts:
			if now - data['time'] > self.expires:
				data['lockout'] = False
				data['failedAttempts'] = 1
			else:
				data['lockout'] = True

		self.save(data)

		return data

	def success(self, account=None):
		data = {
			'account': account,
			'time': int(time.time()),
			'failedAttempts': 0,
			'lockout': False
		}

		self.save(data)
