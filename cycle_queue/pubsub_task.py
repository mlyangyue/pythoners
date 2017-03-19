#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
import redis,json
rc = redis.Redis('127.0.0.1')
ps = rc.pubsub()

'''发布任务时,需要传递 执行任务订阅的渠道channel,执行任务的func,传递给执行任务的参数params,延时执行的时间秒offset'''
task_data = dict(channel='order',
                 func='exec_work',
                 params={'order':11920170101,'uid':1},
                 offset=10)
rc.publish('task_queue', json.dumps(task_data))
