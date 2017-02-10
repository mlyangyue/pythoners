#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

# 时间处理工具

import time
import datetime

"""时间戳转换成格式化日期字符串"""
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



"""时间+-"""
def datetime_change(val=0,ptype="days",datestr=None):
    """
    :func   获取之前或之后的某个时间
    :param  val 正或负数,变动多少,  ptype 变动单位, days日,hours时,minutes分  start_time 时间字符串
    :return 变动后的时间datetime
    """
    if ptype not in ('days','hours','minutes'):
        print " invalid argument "
    today = datetime.datetime.now()
    if datestr:
        today = datetime.datetime.strptime(datestr,'%Y-%m-%d %H:%M:%S')
    if ptype=="days":
        return  today + datetime.timedelta(days=val)
    elif ptype=="hours":
        return  today + datetime.timedelta(hours=val)
    elif ptype=="minutes":
        return  today + datetime.timedelta(minutes=val)
    else:
        pass

"""格式化时间转换"""
def datestr_form(datestr=None,ptype=0):
    """
    :func  把格式化的时间字符串转换成其他类型的时间
    param   datestr 格式化的时间字符串  ptype  时间类型  0 时间戳,1 datetime
    """
    if ptype not in (0,1):
        print " invalid argument "
        return None
    now = datetime.datetime.now()
    if datestr:
        now = datetime.datetime.strptime(datestr,'%Y-%m-%d %H:%M:%S')
    if ptype == 1:
        return now
    if ptype == 0:
        return  int(time.mktime(now.timetuple()))






if __name__ == "__main__":
    # timestamp_to_datestr()
    # print datetime_change(val=1,ptype='minutes',datestr="2017-02-09 10:24:56")
    print datestr_form(datestr="2017-02-10 10:49:45",ptype=1)