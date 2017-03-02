#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'


import os
import signal
import multiprocessing
import time
"""
主进程开启多个子进程,并守护子进程,当子进程退出时,自动拉起子进程
"""
process = {}

def random_sleep(seconds):
	time.sleep(seconds)

def created_subprocess(func,params=None):
	global process
	if params==None:
		f = multiprocessing.Process(target=func)
	else:
		f = multiprocessing.Process(target=func, args=params)
	f.start()
	process[f.pid]=(func,params)
	print process

def main():
	for i in range(3):
		created_subprocess(random_sleep,(100,)) # 开3个子进程
	def child_handler(sig, frame):
		global process
		pid, status = os.wait()#等待进程死掉
		if pid in process:
			params = process[pid]
			created_subprocess(params[0],params[1]) # 重新打开死掉的进程
		del process[pid]
	signal.signal(signal.SIGCHLD, child_handler)

if __name__=='__main__':
	main()