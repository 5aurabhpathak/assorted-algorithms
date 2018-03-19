#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

### Set up logging ###
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Formatting as: 2017-08-02 09:20:34,388|INFO|api.login:44|User logging in: WclAdmin
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s:%(lineno)s|%(message)s')
# Log to stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# Log to File
if not os.path.exists('/storage/logs'):
	os.makedirs('/storage/logs')
file_handler = logging.FileHandler('/storage/logs/webpage.log', 'a')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

### Import 3rd-party Dependencies ###
logger.debug('Loading bottle.py')
import bottle
logger.debug('Loading WSGIServer')
from flup.server.fcgi import WSGIServer

### Set up bottle default_app ###
logger.debug('Connecting to bottle default_app')
app = application = bottle.default_app()
app.config.load_config('/www/wavelinxmonitor/wavelinxmonitor.conf')

### Import our app ###
logger.debug('Loading wavelinxmonitor webapp')
import webapp


if __name__ == "__main__":
	# Change working directory so relative paths (and template lookup) work again
	os.chdir(os.path.dirname(__file__))
	logger.debug('Working directory: ' + str(os.path.dirname(__file__)))
	# start flup webserver
	logger.info('------------------------------------------------------')
	logger.info('-------      Starting up wavelinxmonitor...    -------')
	logger.info('------------------------------------------------------')
	WSGIServer(app).run()
