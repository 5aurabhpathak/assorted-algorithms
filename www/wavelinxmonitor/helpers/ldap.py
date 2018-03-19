# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - helpers/ldap
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import subprocess as sub

from helpers.subproc import make_grep, make_cut, make_args, make_sub


def change_user_password(user, old_password, new_password):
	args = make_args('ldappasswd -D cn=' + user + '+sn=' + user + ',dc=wavelinx -x -w ' + old_password + ' -a ' + old_password + ' -s ' + new_password)
	p = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE)
	try:
		invalid_change, errors = p.communicate()
		if errors:
			return errors.strip('\n')
		elif invalid_change:
			return invalid_change.strip('\n')
		else:
			return None

	except:
		return None

def get_allowed_users():
	sub1 = make_sub(make_args('ldapsearch -x -b dc=wavelinx'))
	sub2 = make_sub(make_grep('dn:'),sub1)
	sub3 = make_sub(make_cut('=','2'),sub2)
	sub4 = make_sub(make_grep('sn'),sub3)
	sub5 = make_sub(make_cut('+','1'),sub4)
	sub6 = make_sub(make_grep('DarkCAPI','-v'),sub5)
	sub6 = make_sub(make_grep('factory','-v'),sub6)
	user_list, errors = sub6.communicate()
	return user_list.strip('\n').split()

def validate_login(user, password):
	sub1 = make_sub(make_args('ldapwhoami -vvv -D cn=' + user + '+sn=' + user + ',dc=wavelinx -w ' + password))
	sub2 = make_sub(make_grep('Success'),sub1)
	try:
		valid_login, errors = sub2.communicate()
		if 'Success' in valid_login:
			return True
		else:
			return False
	except:
		return False
