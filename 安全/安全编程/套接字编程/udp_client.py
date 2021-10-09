#!/usr/bin/python3

import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host=socket.gethostname()
udp_port=12345

msg="Hello Python"
print("UDP taget IP and port is:",udp_host,udp_port)

sock.sendto(msg.encode('utf-8'),(udp_host,udp_port))