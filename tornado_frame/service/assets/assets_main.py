#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from tornado.web import RequestHandler
import logging
logger = logging.getLogger('assets.log')

class Assets(RequestHandler):
	def post(self, *args, **kwargs):
		logger.info("Assets start")
		self.write('hello orders!')