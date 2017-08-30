#!/usr/bin/env python
# coding: utf8
import os
import re
import time
import stat
import logging

from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

import libs

__author__ = 'Andy'


def init_logger_handler(logs_path,file_name):

    log_dir = libs.mkdirs(logs_path)
    filename = log_dir+file_name
    filehandler = TimedRotatingFileHandler(filename=filename, when='D', interval=1, backupCount=0,)
    """
    when 是一个字符串的定义如下：
    “S”: Seconds
    “M”: Minutes
    “H”: Hours
    “D”: Days
    “W”: Week day (0=Monday)
    “midnight”: Roll over at midnight

    interval 是指等待多少个单位when的时间后，Logger会自动重建文件，当然，这个文件的创建
    取决于filename+suffix，若这个文件跟之前的文件有重名，则会自动覆盖掉以前的文件，所以
    有些情况suffix要定义的不能因为when而重复。

    """
    filehandler.suffix = "%Y%m%d-%H%M.log"
    filehandler.setFormatter(Formatter(
        '[%(asctime)s] [%(filename)s:%(lineno)d] [tid:%(thread)d] %(levelname)s:  %(message)s '
    ))

    filehandler.setLevel(logging.INFO)
    return filehandler
