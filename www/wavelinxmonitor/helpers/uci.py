# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/uci
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import logging
import subprocess as sub
import threading

from helpers.syscommand import SynCommand

class UciHandler(object):
	def get(self, config=''):
		result = SynCommand('uci get ' + config)
		return result


uci_handler = UciHandler()

def get(config=''):
	uci_handler.get()