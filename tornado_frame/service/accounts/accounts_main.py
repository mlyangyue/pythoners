#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
from tornado.web import RequestHandler
import logging
logger = logging.getLogger('account.log')

class Accounts(RequestHandler):
	def post(self, *args, **kwargs):
		logger.info("Accounts start")
		self.write('hello Accounts!')