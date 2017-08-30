#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from application import Application
from libs.Manager import Manager,Command
app = Application()
manager = Manager(app)

class Prints(Command):
	def run(self):
		import  time
		time.sleep(100)
		print "hello"

manager.add_command('prints',Prints())
route = {}



if __name__ == '__main__':
	manager.run()