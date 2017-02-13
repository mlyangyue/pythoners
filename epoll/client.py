#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

import socket,time
def sim_client(name,i):
	connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	connFd.connect(("127.0.0.1", 8080))
	connFd.send("Process-%s start subscibe\n\n" % name)
	while True:
		try:
			readData = connFd.recv(1024)
			if readData:
				print "*"*40 + "\n" + readData.decode()
		except:
			time.sleep(0.2)


if __name__=="__main__":
	sim_client("progressage",1)
