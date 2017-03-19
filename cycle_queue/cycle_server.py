#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
'''
用环形队列执行定时任务

一个timer,每隔1s在环形队列里移动到下一个队列,用一个curr_index来标识当前检测的队列下标
环形队列是多个队列存放在一个列表中,当移动到列表的最后一个队列时,curr_index 指向列表中的第一个队列
每个队列里存放一个task set ,当 curr_index 指向该队列时,task set的所有任务num计数+1,计数加到tag_num时开始执行任务
执行完成后把task从taskset中丢弃
'''

import Queue
import time
import threading
import redis
import json
MAXSIZE = 5

exec_queue = Queue.Queue() #真实要执行的任务
subscribe_queue = Queue.Queue()
class Cycle_Queue(object):
	def __init__(self,count=3600,rhost='127.0.0.1'):
		self.cycle_queue = []
		self.curr_index = 0
		self.count = count
		self.rc=redis.Redis(host=rhost)
		pass


	def create_cycle_queue(self):
		"""创建环形队列"""
		self.cycle_queue = [Queue.Queue(maxsize=MAXSIZE) for i in xrange(self.count)]

	def is_full(self,queue):
		"""如果队列满了,返回Ture,否则返回False"""
		return queue.full()

	def get_curr_index(self):
		"""获取当前指针指向的环形队列下标"""
		return self.curr_index

	def get_qsize(self):
		return len(self.cycle_queue)

	def update_queue(self,queue):
		"""更新当前队列的状态,先从队列中取出消息,更新完成后放回队列中"""
		"""TODO,取出消息后会有其他消息占满队列,竞争问题,预期加锁"""
		msg_list = []
		global exec_queue
		while not queue.empty():
			msg_dict = queue.get()
			if 'num' not in msg_dict or  'tag_num' not in msg_dict:
				continue
			msg_dict['num']+=1
			print 'updata',msg_dict
			if msg_dict['num'] == msg_dict["tag_num"]: # 如果目标圈数和当前圈数相同时 执行任务
				del msg_dict['num']
				del msg_dict['tag_num']
				exec_queue.put(msg_dict) # 存放消息到执行队列里
			else:
				msg_list.append(msg_dict)
		"""重新放回队列里"""
		for item in msg_list:
			queue.put(item)

	def run(self):
		global subscribe_queue
		while True:
			time.sleep(1)
			if self.curr_index == self.count-1:
				self.curr_index = 0
			else:
				self.curr_index += 1
			if not subscribe_queue.empty():
				data = subscribe_queue.get()
				print 'recive',data
				if data:
					offset = int(data['offset'])
					if offset>self.count:
						print "大于queue max size"
						continue

					tag_num = offset/self.count+1
					tag_rema = offset%self.count
					tag_index = self.curr_index+tag_rema
					if tag_index>self.count-1:
						tag_index = tag_index-self.count-1
					data['tag_num']=tag_num
					data['num']=0
					queue = self.cycle_queue[tag_index]
					queue.put(data)
			self.update_queue(self.cycle_queue[self.curr_index])


def pubsub_task(exec_queue,rhost='127.0.0.1'):
	rc = redis.Redis(host=rhost)
	pt = rc.pubsub()
	while True:
		if exec_queue.empty():
			time.sleep(0.2)
			continue
		msg_dict = exec_queue.get()
		channel = msg_dict['channel']
		pt.subscribe([channel])
		data = dict(func=msg_dict['func'],
		            params=msg_dict['params'])
		rc.publish(channel, json.dumps(data))


def listen_pubsub(rhost='127.0.0.1'):
	rc = redis.Redis(host=rhost)
	rs = rc.pubsub()
	rs.subscribe(['task_queue'])
	global subscribe_queue
	for task in rs.listen():
		if task['type'] == 'message':
			data = json.loads(task['data'])
			print data
			subscribe_queue.put(data)



if __name__=='__main__':
	cycle_obj = Cycle_Queue(count=10)
	print 'start'
	cycle_obj.create_cycle_queue()
	work1 = threading.Thread(target=cycle_obj.run)
	work2 = threading.Thread(target=listen_pubsub)
	work3 = threading.Thread(target=pubsub_task,args=(exec_queue,))
	work1.start()
	work2.start()
	work3.start()


