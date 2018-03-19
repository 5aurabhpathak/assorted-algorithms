# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/subproc
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import subprocess as sub


def make_grep(search_string, option=None):
	if option:
		return ['grep',option,search_string]
	else:
		return ['grep',search_string]

def make_cut(delimiter, field):
	return ['cut','-d' + delimiter, '-f' + field]

def make_args(args_string):
	return args_string.split()

def make_sub(arguments,pipe_input=None):
	if pipe_input:
		return sub.Popen(arguments,stdin=pipe_input.stdout,stdout=sub.PIPE,shell=False)
	else:
		return sub.Popen(arguments,stdout=sub.PIPE,shell=False)

def do_sync():
	bash_sync = make_sub(make_args('sync'))
	bash_sync.communicate()
