#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
import redis
import datetime
import csv
import json

path1 = './2015年/discount15old.csv'
path2 = './2015年/beforediscount15.csv'
path3 = './2016年/disount16old.csv'
path4 = './2016年/beforediscount16.csv'
path5 = './2017年/17discountold.csv'
path6 = './2017年/17before.csv'

nick = 3  # 买家昵称
order_time = 4  # 下单时间
pay_time = 5  # 付款时间
ordermoney = 10# 实付金额

old = {}
before = {}
oldmoney = {}


rd = redis.Redis()


def deal():
	with open(path5, 'rb') as fd:
		reader = csv.reader(fd)
		for row in reader:
			if reader.line_num == 1:
				continue
			nickname = row[3].decode('gbk')
			if nickname not in old:
				old[nickname] = row[4]
			else:
				old[nickname] = min(old[nickname], row[4])
		rd.hmset('17old',old)
		print 'end'

def dealmoney():
	with open(path5, 'rb') as fd:
		reader = csv.reader(fd)
		moneycount=0
		for row in reader:
			if reader.line_num == 1:
				continue
			nickname = row[3].decode('gbk')
			moneytime = row[4]
			moneyamount = float(row[10])
			moneycount += moneyamount
			if nickname not in oldmoney:
				oldmoney[nickname]={}
				oldmoney[nickname]['ordertime'] = moneytime
			else:
				oldmoney[nickname] = min(oldmoney[nickname], row[4])
			oldmoney[nickname]["money"] = oldmoney[nickname].get('money',0)+float(row[10])
		rd.hmset('17money',oldmoney)
		print 'end',moneycount

def deal500():
	before = {}
	count = 0
	with open(path6, 'rb') as fd:
		reader = csv.reader(fd)
		for row in reader:
			if reader.line_num == 1:
				continue
			try:
				nickname = row[3].decode('gbk')
			except Exception as e:
				print e, count
				continue
			if nickname in old:
				if nickname not in before:
					before[nickname] = row[5]
				else:
					before[nickname] = max(before[nickname], row[5])
		rd.hmset("17before", before)
		print 'end'


def deal3():
	beforeinfo = rd.hgetall("17before")
	oldinfo = rd.hgetall("17old")
	tempdict = {'0-30': 0,
	            '31-60': 0,
	            '61-90': 0,
	            '91-120': 0,
	            '121-150': 0,
	            '151-180': 0,
	            '181-270': 0,
	            '271-360': 0,
	            '361-450': 0,
	            '451-540': 0,
	            '541-630': 0,
	            '631-720': 0,
	            '721-900': 0,
	            '901-1080': 0,
	            '1081-1440': 0,
	            '>1440': 0,

	            }

	tdict = {'0-30': {},
	         '31-60': {},
	         '61-90': {},
	         '91-120': {},
	         '121-150': {},
	         '151-180': {},
	         '181-270': {},
	         '271-360': {},
	         '361-450': {},
	         '451-540': {},
	         '541-630': {},
	         '631-720': {},
	         '721-900': {},
	         '901-1080': {},
	         '1081-1440': {},
	         '>1440': {},

	         }
	for key, val in beforeinfo.iteritems():
		o = oldinfo[key]
		d1 = (int(val[0:4]), int(val[5:7]), int(val[8:10]))
		d2 = (int(o[0:4]), int(o[5:7]), int(o[8:10]))
		t1 = datetime.date(d1[0], d1[1], d1[2])
		t2 = datetime.date(d2[0], d2[1], d2[2])
		days = (t2 - t1).days
		if days <= 30:
			tempdict['0-30'] += 1
			tdict['0-30'][days] = tdict['0-30'].get(days, 0) + 1

		elif days >= 31 and days <= 60:
			tempdict['31-60'] += 1
			tdict['31-60'][days] = tdict['31-60'].get(days, 0) + 1
		elif days >= 61 and days <= 90:
			tempdict['61-90'] += 1
			tdict['61-90'][days] = tdict['61-90'].get(days, 0) + 1
		elif days >= 91 and days <= 120:
			tempdict['91-120'] += 1
			tdict['91-120'][days] = tdict['91-120'].get(days, 0) + 1
		elif days >= 121 and days <= 150:
			tempdict['121-150'] += 1
			tdict['121-150'][days] = tdict['121-150'].get(days, 0) + 1
		elif days >= 151 and days <= 180:
			tempdict['151-180'] += 1
			tdict['151-180'][days] = tdict['151-180'].get(days, 0) + 1
		elif days >= 181 and days <= 270:
			tempdict['181-270'] += 1
			tdict['181-270'][days] = tdict['181-270'].get(days, 0) + 1
		elif days >= 271 and days <= 360:
			tempdict['271-360'] += 1
			tdict['271-360'][days] = tdict['271-360'].get(days, 0) + 1
		elif days >= 361 and days <= 450:
			tempdict['361-450'] += 1
			tdict['361-450'][days] = tdict['361-450'].get(days, 0) + 1
		elif days >= 451 and days <= 540:
			tempdict['451-540'] += 1
			tdict['451-540'][days] = tdict['451-540'].get(days, 0) + 1
		elif days >= 541 and days <= 630:
			tempdict['541-630'] += 1
			tdict['541-630'][days] = tdict['541-630'].get(days, 0) + 1
		elif days >= 631 and days <= 720:
			tempdict['631-720'] += 1
			tdict['631-720'][days] = tdict['631-720'].get(days, 0) + 1
		elif days >= 721 and days <= 900:
			tempdict['721-900'] += 1
			tdict['721-900'][days] = tdict['721-900'].get(days, 0) + 1
		elif days >= 901 and days <= 1080:
			tempdict['901-1080'] += 1
			tdict['901-1080'][days] = tdict['901-1080'].get(days, 0) + 1
		elif days >= 1081 and days <= 1440:
			tempdict['1081-1440'] += 1
			tdict['1081-1440'][days] = tdict['1081-1440'].get(days, 0) + 1
		elif days > 1440:
			tempdict['>1440'] += 1
			tdict['>1440'][days] = tdict['>1440'].get(days, 0) + 1
		else:
			print 'err', days
	# 人数
	t = 0
	for key,val in tempdict.iteritems():
		print key,val
		t += val
	print t
	# 重点天数
	# temp = {}
	# for key,val in tdict.iteritems():
	# 	d = max(val.values())
	# 	for k, v in val.iteritems():
	# 		if v==d:
	# 			temp[key]=k
	# 			break
	# for k,v in temp.iteritems():
	# 	print k,v

def moneyrate():
	moneyinfo = rd.hgetall("17money")
	beforeinfo = rd.hgetall("17before")
	tempdict = {'0-30': 0,
	            '31-60': 0,
	            '61-90': 0,
	            '91-120': 0,
	            '121-150': 0,
	            '151-180': 0,
	            '181-270': 0,
	            '271-360': 0,
	            '361-450': 0,
	            '451-540': 0,
	            '541-630': 0,
	            '631-720': 0,
	            '721-900': 0,
	            '901-1080': 0,
	            '1081-1440': 0,
	            '>1440': 0,

	            }
	for key, val in beforeinfo.iteritems():
		data = eval(moneyinfo[key])
		o = data['ordertime']
		d1 = (int(val[0:4]), int(val[5:7]), int(val[8:10]))
		d2 = (int(o[0:4]), int(o[5:7]), int(o[8:10]))
		t1 = datetime.date(d1[0], d1[1], d1[2])
		t2 = datetime.date(d2[0], d2[1], d2[2])
		days = (t2 - t1).days
		if days <= 30:
			tempdict['0-30'] += float(data['money'])
		elif days >= 31 and days <= 60:
			tempdict['31-60'] += float(data['money'])
		elif days >= 61 and days <= 90:
			tempdict['61-90'] += float(data['money'])
		elif days >= 91 and days <= 120:
			tempdict['91-120'] += float(data['money'])
		elif days >= 121 and days <= 150:
			tempdict['121-150'] += float(data['money'])
		elif days >= 151 and days <= 180:
			tempdict['151-180'] += float(data['money'])
		elif days >= 181 and days <= 270:
			tempdict['181-270'] += float(data['money'])
		elif days >= 271 and days <= 360:
			tempdict['271-360'] += float(data['money'])
		elif days >= 361 and days <= 450:
			tempdict['361-450'] += float(data['money'])
		elif days >= 451 and days <= 540:
			tempdict['451-540'] += float(data['money'])
		elif days >= 541 and days <= 630:
			tempdict['541-630'] += float(data['money'])
		elif days >= 631 and days <= 720:
			tempdict['631-720'] += float(data['money'])
		elif days >= 721 and days <= 900:
			tempdict['721-900'] += float(data['money'])
		elif days >= 901 and days <= 1080:
			tempdict['901-1080'] += float(data['money'])
		elif days >= 1081 and days <= 1440:
			tempdict['1081-1440'] += float(data['money'])
		elif days > 1440:
			tempdict['>1440'] += float(data['money'])
		else:
			print 'err', days
	tem = 0
	for key,val in tempdict.iteritems():
		tem +=val
		print key, val
	print tem




	pass
if __name__ == "__main__":
	# deal()
	# deal500()

	# deal3()
	# dealmoney()
	# moneyrate()
	pass
