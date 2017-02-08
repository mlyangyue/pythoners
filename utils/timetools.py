#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

# 时间处理工具

import time

"""时间戳转换成日期"""
def timestamp_to_datestr(timestamp=None,type=0):
	"""
	:func 时间戳转换日期字符串
	:param timestamp 时间戳  type: 时间格式类型
	"""
	if not timestamp:
		timestamp = int(time.time())
	_format = "%Y-%m-%d %H:%M:%S"
	if type == 1:
		_format = "%Y-%m-%d"
	elif type == 2:
		_format = "%Y/%m/%d"
	elif type == 3:
		_format = "%Y%m%d"
	elif type == 4:
		_format = "%Y%m%d%H%M%S"
	return time.strftime(_format, time.localtime(timestamp))


if __name__ == "__main__":
	timestamp_to_datestr()