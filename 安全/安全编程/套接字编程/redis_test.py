import os
import subprocess
import time


f= open("D:\\BaiduNetdiskDownload\\笔记\\安全\\安全编程\\redis_ip.txt",'r',encoding="utf-8")
for ip in f:
    exec="D:\\BaiduNetdiskDownload\\工具\\Redis-x64-3.0.504\\redis-cli.exe -h " + ip + " -c ping"
    # re=os.system(exec)
    # print(re)
    # with os.popen(exec, "r") as cmd:
    #     r=cmd.read()
    #     print(r)
    p =subprocess.Popen(exec, shell=True, stdout=subprocess.PIPE)
    r = p.stdout.read( )
    print(r)
