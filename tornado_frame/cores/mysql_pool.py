#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
from gevent import monkey

monkey.patch_all()

import pymysql
from Queue import Queue


class Exec_db:
	__v = None

	def __init__(self, host='localhost', port=3306, user=None, passwd=None, db=None, charset='utf-8', maxconn=5):
		self.host, self.port, self.user, self.passwd, self.db, self.charset = host, port, user, passwd, db, charset
		self.maxconn = maxconn
		self.pool = Queue(maxconn)
		for i in range(maxconn):
			try:
				conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
				                       charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
				conn.autocommit(False)
				# self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
				self.pool.put(conn)
			except Exception as e:
				raise IOError(e)

	@classmethod
	def get_instance(cls, *args, **kwargs):
		if cls.__v:
			return cls.__v
		else:
			cls.__v = Exec_db(*args, **kwargs)
			return cls.__v

	def exec_sql(self, sql, operation=None):
		"""
			执行无返回结果集的sql，主要有insert update delete
		"""
		try:
			conn = self.pool.get()
			cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
			response = cursor.execute(sql, operation) if operation else cursor.execute(sql)
		except Exception as e:
			print e
			cursor.close()
			self.pool.put(conn)
			return None
		else:
			cursor.close()
			self.pool.put(conn)
			return response

	def exec_sql_feach(self, sql, operation=None):
		"""
			执行有返回结果集的sql,主要是select
		"""
		try:
			conn = self.pool.get()
			cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
			response = cursor.execute(sql, operation) if operation else cursor.execute(sql)
		except Exception as e:
			print e
			cursor.close()
			self.pool.put(conn)
			return None, None
		else:
			data = cursor.fetchall()
			cursor.close()
			self.pool.put(conn)
			return response, data

	def exec_sql_many(self, sql, operation=None):
		"""
			执行多个sql，主要是insert into 多条数据的时候
		"""
		try:
			conn = self.pool.get()
			cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
			response = cursor.executemany(sql, operation) if operation else cursor.executemany(sql)
		except Exception as e:
			print e
			cursor.close()
			self.pool.put(conn)
		else:
			cursor.close()
			self.pool.put(conn)
			return response


	def close_conn(self):
		for i in range(self.maxconn):
			self.pool.get().close()


obj=Exec_db.get_instance(host='',db="sql_example",charset="utf8",maxconn=10)
