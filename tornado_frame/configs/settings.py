#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'


# 基础配置文件
class Config(object):
	debug = False
	dbconfig = {
		#后端读库
		'bkrdb': {
			"host": "localhost",
			"port": 3306,
			"user": "root",
			"passwd": "000000",
			"db":"blog",
			"charset": "utf-8",
		},
		#后端写库
		'bkwdb': {
			"host": "localhost",
			"port": 3306,
			"user": "root",
			"passwd": "000000",
			"db":"blog",
			"charset": "utf-8",
		}
	}
	pass


# 本地配置文件
class LocalConfig(Config):
	debug = False
	logs_path = "/Users/wangranming/log/"


# 生产配置文件
class Produce(Config):
	debug = False
	logs_path = "/data/logs/htg_usa_logs/"


SETTINGS = {
	'produce': Produce,
	'default': LocalConfig,
}

RUNING_CONFIG = 'default'