#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
'''生产者消费者模式v2版本'''
import threading
import random, time, Queue

MAX_SIZE = 5
SHARE_Q = Queue.Queue(5)  # 模拟共享队列
CONDITION = threading.Condition()

class Producer(threading.Thread):
   def run(self):
       products = range(5)
       global SHARE_Q
       while True:
           CONDITION.acquire()
           if SHARE_Q.full(): # 队列满了释放锁,通知消费者
               print "Queue is full.."
               CONDITION.wait() #进入wait状态,生产者主动释放锁
               print "Consumer have comsumed something"
           product = random.choice(products)
           SHARE_Q.put(product)
           print "Producer : ", product
           CONDITION.notify() # 通知消费者醒来,lock还在
           CONDITION.release() # 主动释放锁
           time.sleep(random.random())

class Consumer(threading.Thread):
   def run(self):
       global SHARE_Q
       while True:
           CONDITION.acquire()
           if SHARE_Q.empty(): # 队列空了,释放锁通知生产者
               print "Queue is Empty..."
               CONDITION.wait() #释放锁
               print "Producer have producted something"
           product = SHARE_Q.get()
           print "Consumer :", product
           CONDITION.notify()
           CONDITION.release()
           time.sleep(random.random())

if __name__ == '__main__':
   Producer().start()
   Consumer().start()