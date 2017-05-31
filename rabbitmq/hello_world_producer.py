#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""
rabbitmq 发布者 需要完成以下任务
1 连接到rabbitmq
2 获取信道
3 声明交换器
4 创建消息
5 发布消息
6 关闭信道
7 关闭连接
"""



import pika
import sys
from pika import spec
"""建立到代理服务器的链接"""
credentials = pika.PlainCredentials("guest","guest")
conn_params = pika.ConnectionParameters("127.0.0.1",credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
"""获得信道"""
channel = conn_broker.channel()
"""声明交换器"""
channel.exchange_declare(exchange="hello-exchange",
                         type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)


"""设置信道为confirm模式"""
# channel.confirm_delivery()
# channel.basic_consume()

msg_ids = []
"""创建纯文本消息"""
msg =sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

"""发布消息"""
ack = channel.basic_publish(body=msg,
                            exchange="hello-exchange",
                            properties=msg_props,
                            routing_key="hola")
if ack == True:
    print "put message to rabbitmq successed!"
else:
    print "put message to rabbitmq failed"
conn_broker.close()