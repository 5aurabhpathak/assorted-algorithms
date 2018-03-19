# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - api/cors
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import bottle
from bottle import request, response

_allow_origin = '*'
_allow_methods = 'GET, POST, PUT, PATCH, DELETE, LINK, UNLINK'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With, token'

app = application = bottle.default_app()

@app.hook('after_request')
def enable_cors():

	if request.get_header('Origin'):				
		response.headers['Access-Control-Allow-Origin'] = request.get_header('Origin')

		return


@app.route('/', method = 'OPTIONS')
@app.route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):

	if request.get_header('Origin'):
		if request.get_header('Access-Control-Request-Method'):
			if request.get_header('Access-Control-Request-Method') != _allow_methods:
				response.headers['Access-Control-Allow-Methods'] = _allow_methods
				response.headers['Access-Control-Allow-Headers'] = _allow_headers
				
		response.headers['Access-Control-Allow-Origin'] = request.get_header('Origin')

		return
