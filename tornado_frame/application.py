#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
import logging

import tornado.web
from configs.settings import SETTINGS,RUNING_CONFIG
from libs.config import Config
from libs.logger import init_logger_handler
from utils.helpers import get_root_path



class Application(tornado.web.Application):
	default_config = dict(debug=False)

	def __init__(self, service="all", env="default"):
		self.import_name = env
		self.root_path = get_root_path(self.import_name)
		from urls.main_url import main_patterns
		handlers = main_patterns
		configs = self.load_config()
		super(Application, self).__init__(handlers=handlers,log_request=self.log_request, **configs)
		self.init_log()
		self.init_db()

	def load_config(self):
		"""
		加载配置
		:return:
		"""
		config = Config(self.root_path, self.default_config)
		config.from_object(SETTINGS[RUNING_CONFIG])
		return config

	def init_log(self):
		"""
		初始化日志
		:return:
		"""
		logs_path = self.settings.get("logs_path")
		# Orders
		order_logger = logging.getLogger('orders.log')
		order_logger.setLevel(logging.INFO)
		order_logger.addHandler(init_logger_handler(logs_path,'orders.log'))

		# Account Requests && Account
		account_logger = logging.getLogger('account.log')
		account_logger.setLevel(logging.INFO)
		account_logger.addHandler(init_logger_handler(logs_path,'account.log'))

		#Assets
		assets_logger = logging.getLogger('assets.log')
		assets_logger.setLevel(logging.INFO)
		assets_logger.addHandler(init_logger_handler(logs_path,'assets.log'))

		# Messages
		assets_logger = logging.getLogger('messages.log')
		assets_logger.setLevel(logging.INFO)
		assets_logger.addHandler(init_logger_handler(logs_path,'messages.log'))



	def log_request(self,handler):
		"""
		请求日志
		"""
		logs_path = self.settings.get("logs_path")
		apicall_logger = logging.getLogger('apicall.log')
		apicall_logger.setLevel(logging.INFO)
		apicall_logger.addHandler(init_logger_handler(logs_path,'apicall.log'))
		if handler.get_status() < 400:
			log_method = apicall_logger.info
		elif handler.get_status() < 500:
			log_method = apicall_logger.warning
		else:
			log_method = apicall_logger.error
		req = handler.request
		log_method('"%s %s" %d %s %.6f',
		           req.method, req.uri, handler.get_status(),
		           req.remote_ip, req.request_time() )


