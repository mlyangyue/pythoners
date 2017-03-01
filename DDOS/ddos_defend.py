#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""
一个防护ddos的脚本
用netstat 查询ip的连接数,同一ip超过一定量的连接数就用iptables禁掉
查询命令用netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr
禁用访问命令:

"""

import os
import redis
import json
rd = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
MAX_LINK_QUANTITY = 50 # 最大连接次数阀值

ip_stat = json.loads(rd.get("ip_stat")) if rd.hgetall("ip_stat") else {}

output = os.popen("netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n").readlines()
new_ipstat={}
for item in output:
	ipseq = item.strip(" ").strip("\n").split(" ")
	count, ip = int(ipseq[0]), ipseq[1]
	if ip in ip_stat:
		new_ipstat[ip]=count+ip_stat[ip]
	new_ipstat[ip] = count

rd.set('ip_stat',json.dumps(new_ipstat),ex=10)
