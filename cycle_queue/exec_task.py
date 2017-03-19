#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'


import redis,json
rc = redis.Redis(host='127.0.0.1')
ps = rc.pubsub()
ps.subscribe(['order']) # 该类任务的订阅队列

def exec_work(**params):
	print 'start',params

dict_func = globals()
for item in ps.listen():
	print 'in'
	if item['type'] == 'message':
		data = json.loads(item['data'])
		dict_func[data['func']](**data['params'])