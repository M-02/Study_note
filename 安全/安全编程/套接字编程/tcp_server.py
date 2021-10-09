#!/usr/bin/python3
#This is tcp_server.py

import socket

#创建套接字
s=socket.socket()
#获取ip+port
host=socket.gethostname()
port=9999
#监听地址
s.bind((host,port))
print("Waiting for connection......")
#监听连接
s.listen(5)
#与客户端建立连接
while True:
    conn,addr=s.accept()
    print("Got connection from",addr)
    conn.send('Server Say Hiaiaiai'.encode())
#关闭套接字
conn.close()