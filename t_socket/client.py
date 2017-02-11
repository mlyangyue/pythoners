#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

import socket
import time
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8001))
while True:
	try:
		second = random.randint(1,8)
		time.sleep(1)
		print "send msg"
		sock.send('I send msg is {second}'.format(second=second))
		print sock.recv(1024)
	except Exception as E:
		time.sleep(0.01)

sock.close()