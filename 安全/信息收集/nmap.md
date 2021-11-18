简要回顾Nmap简单的扫描方式：

- 1 全面扫描：nmap-T4 -A target ip   
- 2 主机发现：nmap-T4 -sn target ip   
- 3 端口扫描：nmap-T4 target ip   
- 4 服务扫描：nmap-T4 -sV target ip   
- 5 操作系统扫描：nmap-T4 -O targetip
  上述的扫描方式能满足一般的信息搜集需求。而若想利用Nmap探索出特定的场景中更详细的信息，则需仔细地设计Nmap命令行参数，以便精确地控制Nmap的扫描行为。

# 端口扫描

```bash
nmap -F -sT -V nmap.org
nmap -iF 1.txt
nmap -iF 1.txt --exculde host1,host2
nmap -iF 1.txt --exculdefile 2.txt
nmap -iR 随机扫描
nmap -PS TCP发送一个SYN包
nmap -PA TCP发送一个ACK包
nmap -PU 发送一个UDP包
nmap -PR 使用ARP扫描
nmap -n  不对发现的主机进行反向域名解析

-F: 扫描100个最有可能开放的端口-V获取扫描的信息-sT:采用的是TCP扫描不写也是可以的，默认采用的就是TCP扫描
-p:指定要扫描的端口

```

![image-20210524103241424](D:\BaiduNetdiskDownload\安全\信息收集\nmap.assets\image-20210524103241424.png)



# TCP扫描(-sT)

这是一种最为普通的扫描方法，这种扫描方法的特点是:
	扫描的速度快，准确性高，对操作者没有权限上的要求，
	但是容易被防火墙和IDS(防入侵系统)发现
运行的原理:通过建立TCP的三次握手连接来进行信息的传递
	Client端发送SYN;
	Server端返回SYN/ACK，表明端口开放;
	Client端返回ACK,表明连接已建立;
	Client端主动断开连接。

# SYN扫描( -sS)

这是一种秘密的扫描方式之一，因为在SYN扫描中Client端和Server端没有形成3次握手，所以没有建立一个正常的TCP连接，因此不被防火墙和日志所记录，一般不会再目标主机上留下任何的痕迹，但是这种扫描是需要root权限(对于windows用户来说，是没有root权限这个概念的，root权限是linux的最高权限，对应windows的管理员权限)

# 端口扫描

使用UDP ping探测主机:

```bash
nmap -PU 192.168.1.0/24
```

服务版本探测

```bash
nmap -sV 192.168.1.1
```

精准地确认端口上运行的服务

```bash
nmap -sV --script unusual-port 192.168.1.1
```

syn扫描器
扫描外国主机网段
对应端口爆破工具
提供访向木马服务端下载的工具
ftp、http nfs
一个远控

# 探测目标主机的操作系统

```bash
nmap -0 192.168.1.19
nmap -A 192.168.1.19

nmap -A 192.168.1.19 -oN /1.txt 导出扫描结果
nmap -A 192.168.1.19 -oX /1.xml 导出扫描结果xml格式
```

# 防火墙躲避绕过

-f分片绕过
-D使用透饵隐蔽扫描

```bash
NMAP -D 1.1.1.1,222.222.222.222 www.cracer.com
```

 --source-port 源端口欺骗

```
Nmap --script=vuln    默认nse插件
Nmap vulscan vulners   调用第三方库探针
脚本存放路径：/usr/share/nmap/scripts/
```

