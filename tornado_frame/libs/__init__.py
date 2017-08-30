#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

import os

def mkdirs(dir_path):
	"""
    生成日志目录
    :param dir_path:
    :return:
    """
	if not dir_path:
		dir_path = os.curdir + '/logs'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	return dir_path
