#!/usr/bin/python3

import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host=socket.gethostname()
udp_port=12345

sock.bind((udp_host,udp_port))

while True:
    print("Waiting for client.....")
#从客户端返回数据
    data,addr=sock.recvfrom(1024)
#对传输的数据进行解码
    print("Received Messages:",data.decode('utf-8'),"from",addr)