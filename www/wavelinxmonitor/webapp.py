#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	wavelinxmonitor - app
	~~~~~~~~~~
	A diagnostic and analytics application to manage, monitor, and
	report on the gateway application.

	:copyright: (c) 2017 by Eaton.
	:license: ???, see LICENSE for more details.
"""
import json
import logging
import sys

# Logging Setup
if len(sys.argv) == 2:
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# Formatting as: 2017-08-02 09:20:34,388|INFO|api.login:44|User logging in: WclAdmin
	formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s:%(lineno)s|%(message)s')
	# Log to stdout
	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(formatter)
	logger.addHandler(stream_handler)
	# Log to File
	file_handler = logging.FileHandler('/storage/logs/webpage.log', 'a')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.debug('Debug logger set up')
else:
	logger = logging.getLogger(__name__)

# Bottle configuration
import bottle
app = application = bottle.default_app()
app.config.load_config('/www/wavelinxmonitor/wavelinxmonitor.conf')
bottle.BaseRequest.MEMFILE_MAX = int(app.config['wlm.file_max_int'])

# Load webapps
logger.debug('Loading wavelinxmonitor webapp components')
from api import login, system, networks, update, backup, cors, error


if __name__ == "__main__":
	logger.info('-------------------------------------------------')
	logger.info('-----   Starting up wavelinxmonitor (dev)   -----')
	logger.info('-------------------------------------------------')
	logger.debug('Config info: ' + json.dumps(app.config, indent=4))
	logger.info('Running Config API ' + app.config['wlm.api_version'])
	app.run(host='0.0.0.0', port=8080)
