import socket
import os
from whois import whois
import sys

#域名反查ip
# ip=socket.gethostbyname('daishen.ltd')
# print(ip)

#识别目标是否存在CDN，采用nslookup执行结果进行返回TP解析数具判断，利用Python调用系统指令
def CDN(url):
    # cdn_data=os.system('nslookup daishen.ltd')
    # print(cdn_data)
    cdn_data=os.popen('nslookup '+url)
    cdn_datas=cdn_data.read()
    x=cdn_datas.count('.')
    if x>10:
        print("CDN ON")
    else:
        print("CDN OFF")

#端口扫描
#1.原生自写socket协议tcpxudp扫描
#2.调用第三方masscan,nmap等扫描
#3.调用系统工具脚本执行
def PORT(url):
    ports=[21,22,1433,1521,3389,80,8080,135,445,3306,8888]
    ips=[url]
    for ip in ips:
        for port in ports:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #AF_INET ipv4 AF_INET6 ipv6 SOCK_STREAM执行面向流的tcp协议
            result=sock.connect_ex((ip,port))
            if result==0:
                print(ip+":%d is open" %port)
            else:
                print(ip+":%d is not open" %port)
    sock.close()

#whois查 询
#第方库进whois查询也可以利用网上接口查询
def whois(url):
    data=whois(url)
    print(data)

#子域名查询
#1.利用字典加载爆破进行查询
#2.利用bing或第三方接口进行查询
def SubDomain(url):
    urls=url.replace('www','')
    for sub_data in open('d:/BaiduNetdiskDownload/安全/安全编程/PasswordDic/SubDomain.dic'):
        sub_data=sub_data.replace('\n','')
        url=sub_data+urls
        try:
            ip=socket.gethostbyname(url)
            print(url+'-->'+ip)
        except Exception as e:
            # print(url+"子域名出错")
            pass

if __name__=='__main__':
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    check=sys.argv[1]
    url=sys.argv[2]
    if check=='-a':
        # whois(url)
        # PORT(url)
        CDN(url)
        SubDomain(url)
    elif check=='-c':
        CDN(url)
    elif check=='-s':
         SubDomain(url)