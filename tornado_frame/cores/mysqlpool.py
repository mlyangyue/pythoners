#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
import time
import pymysql
import threading
from configs.settings import RUNING_CONFIG, SETTINGS
from sqlalchemy.pool import QueuePool
"""
使用sqlalchemy的线程池QueuePool,实现mysql的连接池
使用时调用对应的get_read,get_wirte 获取连接,连接脱离作用域后自动回收,不用conn.close()
"""

_DB_POOL_ = {}

MUTEX = threading.Lock()


def createconn(host='localhost', port=3306, user=None, passwd=None, db=None, charset='utf-8'):
	conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,
	                       cursorclass=pymysql.cursors.DictCursor)
	return conn


def decorate_mutex(lock):
	def decoFunc(f):
		def callFunc(*args, **kwargs):
			lock.acquire()
			try:
				return f(*args, **kwargs)
			finally:
				lock.release()
		return callFunc
	return decoFunc

@decorate_mutex(MUTEX)
def ConnPool(index, suffix=None):
	"""
	初始化连接池
	:param index:数据库访问名
	:param suffix:连接方式 read,write
	"""

	index_suffix = str(index)
	if not suffix:
		index_suffix += str(suffix)
	if not index_suffix in _DB_POOL_:
		conf = SETTINGS[RUNING_CONFIG].dbconfig
		if not index in conf:
			index = 'bkwdb'
		dbconf = conf.get(index)
		# pool_size 最大连接数,max_overflow 超出最大连接数后缓存的连接数,timeout 超时返回连接时间
		_DB_POOL_[index_suffix] = QueuePool(lambda: createconn(**dbconf), pool_size=2, max_overflow=0, timeout=10)
	conn = None
	for i in range(_DB_POOL_[index_suffix].size() + 1):
		conn = _DB_POOL_[index_suffix].connect()
		try:
			conn.ping()
			break
		except pymysql.OperationalError:
			conn.invalidate()

	return conn


def get_read(index, suffix='read'):
	conn = ConnPool(index, suffix)
	return conn


def get_write(index, suffix='write'):
	conn = ConnPool(index, suffix)
	return conn



# def demo(start):
# 	conn = get_write('bkwdb')
# 	cur = conn.cursor()
# 	sql = """
# 		select * from new_table
# 		where name = 'andy{start}';
# 	""".format(start=start)
# 	cur.execute(sql)
# 	data = cur.fetchone()
# 	return data
#
#
# def threadrun(start):
# 	count = 10
# 	while count > 0:
# 		data = demo(start)
# 		print threading.current_thread().name,data
# 		count -= 1
# 		start += 1
# 		time.sleep(1)
#
#
# def main():
# 	t_list = []
# 	for i in range(5):
# 		t = threading.Thread(target=threadrun, args=(i * 1000,), name='thread_' + str(i))
# 		t_list.append(t)
# 	for t in t_list:
# 		t.setDaemon(True)
# 		t.start()
# 	t.join()
#
#
# if __name__ == '__main__':
# 	main()