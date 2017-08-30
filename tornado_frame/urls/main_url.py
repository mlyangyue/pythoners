#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
from tornado import gen
from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor
import tornado.web
import datetime


class Executor(ThreadPoolExecutor):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not getattr(cls, '_instance', None):
			cls._instance = ThreadPoolExecutor(max_workers=10)
		return cls._instance


class MainHandel(RequestHandler):
	executor = Executor()

	@gen.coroutine
	def post(self, *args, **kwargs):
		params = self.request.arguments
		uri = self.request.uri
		args = {}
		for arg in params:
			args[arg] = params[arg][-1]
		print uri, args
		from urls.api_urls import url_map
		if uri not in url_map:
			raise tornado.web.HTTPError(404)
		fun = url_map[uri]
		future = self.executor.submit(self.func, fun, args)
		response = yield tornado.gen.with_timeout(datetime.timedelta(seconds=20), future,
		                                          quiet_exceptions=tornado.gen.TimeoutError)
		data = self.std_return_info(response)
		self.write(data)
		self.finish()

	# @tornado.concurrent.run_on_executor
	def func(self, fun, args):
		response = fun(**args)
		return response

	def std_return_info(self, response):
		if isinstance(response, dict):
			_errcode = response.pop('_errcode', 0)
			_errmsg = response.pop('_errmsg', '')
			return dict(data=response,
			            _errcode=_errcode,
			            _errmsg=_errmsg)
		return dict(data=response,
		            _errcode=0,
		            _errmsg='')


main_patterns = [(r"^/(.*)", MainHandel)]
