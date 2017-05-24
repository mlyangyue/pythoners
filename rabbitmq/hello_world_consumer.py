#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""
rabbitmq 消费者 需要执行以下任务
1 连接到rabbitmq
2 获得信道
3 声明交换器
4 把队列和交换器绑定起来
5 消费消息
6 关闭信道
7 关闭连接
"""
import pika
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
"""声明队列"""
channel.queue_declare(queue="hello-queue")
"""绑定队列"""
channel.queue_bind(queue='hello-queue',
                   exchange="hello-exchange",
                   routing_key="hola")

"""处理消息的回调"""
def msg_consumer(channel,method,header,body):
	channel.basic_ack(delivery_tag=method.delivery_tag) # 消息确认
	if body == 'quit':
		channel.basic_cancel(consumer_tag="hello-consumer") #停止消费并退出
		channel.stop_consuming()
	else:
		print body
	return

channel.basic_consume(msg_consumer,
                      queue="hello-queue",
                      consumer_tag="hello-consumer")
channel.start_consuming()


