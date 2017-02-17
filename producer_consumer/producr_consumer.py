#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
'''生产者消费者模式'''
import thread
import threading
import time
import random
import Queue

share_queue = Queue.Queue()  # 共享队列
my_lock = thread.allocate_lock() # 队列共享变量,放进锁里防止竞争

class Producer(threading.Thread):
   def run(self):
       products = range(5)
       global share_queue
       while True:
           num = random.choice(products)
           my_lock.acquire()  # 加锁
           share_queue.put(num) # 放入队列
           print "Produce : ", num
           my_lock.release()  # 释放锁 给其他人
           time.sleep(random.random())  # 用睡眠不好

class Consumer(threading.Thread):
   def run(self):
       global share_queue
       while True:
           my_lock.acquire() # 加锁
           if share_queue.empty():
               print "Queue is Empty..."
               my_lock.release()
               time.sleep(random.random())
               continue
           num = share_queue.get() # 从队列取
           print "Consumer : ", num
           my_lock.release() # 释放锁 给其他人
           time.sleep(random.random()) # 用睡眠不好 信号比较好

if __name__ == '__main__':
   Producer().start() # 启动生产者
   Consumer().start() # 启动消费者