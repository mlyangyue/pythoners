#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

__author__ = 'Andy'

import logging
import pymysql
import time


logger = logging.getLogger('orders.log')

DBCONFIG = {
	'host': '127.0.0.1',
	'port': 3306,
	'user': 'root',
	'password': '000000',
	'db': 'blog',
	'cursorclass': pymysql.cursors.DictCursor
}
save_connect = pymysql.connect(**DBCONFIG)


class DB(object):
	def __init__(self, autocommit=False):
		self.save_connect = pymysql.connect(**DBCONFIG)
		if not autocommit:
			self.save_connect.autocommit(0)
		self.cursor = self.save_connect.cursor()


class Orders(object):
	@staticmethod
	def post(*args, **kwargs):
		logger.info("Orders start")
		time.sleep(10)

	@staticmethod
	def query(*args, **kwargs):
		logger.info("Orders query")
		time.sleep(10)


