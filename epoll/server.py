#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

'''
epoll是linux系统下高并发效率非常高的I/O多路复用模型
I/O多路复用的场合

1、当客户处理多个描述字时（通常是交互式输入和网络套接字），必须使用I/O复用

2、如果一个TCP服务器既要处理监听套接字，又要处理已连接套接字，一般也要用到I/O复用

3、如果一个服务器即要处理TCP，又要处理UDP，一般要使用I/O复用
'''


import socket, select, traceback, time
import threading
import Queue

gen = Queue.Queue()
connections = {}
requests = {}
responses = {}

def run():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 18080))
    serversocket.listen(5)
    serversocket.setblocking(0) #设定非阻塞模式
    epoll = select.epoll()  # 创建一个epoll对象
    epoll.register(serversocket.fileno(), select.EPOLLIN)  # 给新建的serversocket.fileno注册一个读event
    try:
        count = 0
        while True:
            events = epoll.poll()  # 激活的fileno举手
            count += 1
            for fileno, event in events:
                if fileno == serversocket.fileno():  # 当激活的fileno是新建的,给该fileno注册一个读event
                    connection, address = serversocket.accept()
                    connection.setblocking(0)
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    connections[connection.fileno()] = connection
                    requests[connection.fileno()] = b''
                    responses[connection.fileno()] = b""
                    print "new conn.fileno is %s" % connection.fileno()
                elif event & select.EPOLLIN:  # 如果fileno是读event,接收发送来消息,并修改该fileno为写event,下次循环时写数据
                    print "read event is happing"
                    requests[fileno] += connections[fileno].recv(1024)
                    epoll.modify(fileno, select.EPOLLOUT)
                    print('-' * 40 + '\n' + requests[fileno].decode()[:-2])
                elif event & select.EPOLLOUT:  # 如果fileno是写事件,写完后正常的为挂起
                    if responses[fileno]:
                        byteswritten = connections[fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            epoll.modify(fileno, select.EPOLLOUT)  # 需要向订阅者一直发消息,这里发完后仍为写event
                            print "change event to write"
                elif event & select.EPOLLHUP:
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
                    print "event is HUP ===%s" % fileno
        pass
    except Exception, err:
        print traceback.print_exc()
    finally:
        epoll.unregister(serversocket.fileno())
        epoll.close()
        serversocket.close()
        print "finally"

def create_data():
    count = 1
    while True:
        count += 1
        res = "Message-%s" % count
        gen.put_nowait(res)  # 把消息放入队列
        time.sleep(0.5)


def update_message():
    while True:
        message = gen.get()
        for res in responses:  # 遍历所有的活跃用户,更新消息
            responses[res] = message
        time.sleep(0.05)


if __name__ == "__main__":
    p = threading.Thread(target=create_data)  # 开个线程向队列里放数据
    p1 = threading.Thread(target=update_message)  # 从队列中取出数据
    p.start()
    p1.start()
    run()
    p.join()
    p1.join()
