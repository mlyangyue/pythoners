#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'


import socket
'''创建socket对象 socket.socket( family, type )'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET家族包括Internet地址,SOCK_STREAM为流套接字
'''绑定到指定地址和端口 socket.bind(address)'''
sock.bind(('localhost', 8001))  # AF_INET创建的套接字address是元祖(host,port)
'''开始监听socket.listen(size)'''
sock.listen(5) # size表示最多允许连接的客户端数量,连接会进行排队,超出的拒绝连接
'''等待连接请求socket.accept()'''
while True:
    conn,address = sock.accept()
    try:
        conn.settimeout(5)
        while True:
            '''处理连接'''
            buf = conn.recv(1024)
            if len(buf)>0:
                conn.send("data recv success msg={buf}".format(buf=buf))
            else:
                print "data send over"
                conn.send("data send over")
    except socket.timeout:
        print "time out"
    conn.close()

