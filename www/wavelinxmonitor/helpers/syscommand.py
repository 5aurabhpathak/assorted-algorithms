# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/syscommand
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import logging
# import shlex
import subprocess as sub
import threading

class SynCommand(object):
	'''
	Class to synchronously fire off a system command with timeout

	:string cmd: shell command

	:tuple rtnvalue: value from stdout, stderr as a tuple
	'''

	_logger = logging.getLogger(__name__)

	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout=None):
		'''
		:int timeout: command timeout in seconds
		'''
		def target():
			self._logger.debug('Command started: ' + self.cmd)
			self._logger.debug('Timing out in ' + str(timeout) + 's')
			# May want/need to skip the shlex.split() when using shell=True
			# See Popen() constructor docs on 'shell' argument for more detail.
			# args = shlex.split(self.cmd)
			self.process = sub.Popen(self.cmd.split(), shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
			self.timer.start()
			cmd_output = self.process.communicate()
			self.timer.cancel()
			self._logger.debug('Getting process output')
			self.output = cmd_output

		def timer_callback():
			self._logger.debug('Terminating command (timed out)')
			self.process.kill()
			self._logger.debug('Terminated.')

		thread = threading.Thread(target=target)
		self.timer = threading.Timer(timeout, timer_callback)
		thread.start()
		thread.join()

		return self.output


class AsynCommand(object):
	'''
	Class to asynchronously fire off a system command with timeout

	:string cmd: shell command
	'''

	_logger = logging.getLogger(__name__)

	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout=None):
		def target():
			self._logger.debug('Command started: ' + self.cmd)
			self._logger.debug('Timing out in ' + str(timeout) + 's')
			# May want/need to skip the shlex.split() when using shell=True
			# See Popen() constructor docs on 'shell' argument for more detail.
			# args = shlex.split(self.cmd)
			self.process = sub.Popen(self.cmd.split(), shell=False, stdout=sub.PIPE, stderr=sub.PIPE)
			self.timer.start()
			cmd_output = self.process.communicate()
			self.timer.cancel()

		def timer_callback():
			self._logger.debug('Terminating command (timed out)')
			self.process.kill()
			self._logger.debug('Terminated.')

		thread = threading.Thread(target=target)
		self.timer = threading.Timer(timeout, timer_callback)
		thread.start()
