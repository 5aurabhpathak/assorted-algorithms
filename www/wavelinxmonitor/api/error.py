# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/error
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import json
import logging

import bottle
from bottle import response

app = application = bottle.default_app()
logger = logging.getLogger(__name__)

@app.error(500)
def custom_500(error):
	response.headers['Content-Type'] = 'application/json'
	logger.exception('Uncaught exception: %r' % error.exception)
	logger.debug(str(error.traceback))
	response.status = 404
	error_response = {
		'errorCode': 'WLM.EXC.000',
		'description': 'nada',
		'message': repr(error.exception),
		'severity': 'CRITICAL'		
	}
	return json.dumps(error_response)


@app.error(401)
@app.error(403)
@app.error(404)
@app.error(405)
def custom_error(error):
	response.headers['Content-Type'] = 'application/json'
	logger.exception('%s Error: %s' % (response.status, error.body))
	response.status = 404
	error_response = {
		'errorCode': 'WLM.GEN.000',
		'description': 'nada',
		'message': error.body,
		'severity': 'ERROR'		
	}
	return json.dumps(error_response)
