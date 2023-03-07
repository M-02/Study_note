# CSRF漏洞原理

CSRF全称：Cross-site request forgery，即，跨站请求伪造，也被称为 “One Click Attack” 或 “Session Riding”，通常缩写为CSRF或者XSRF，是一种对网站的恶意利用。举个生活中的例子：就是某个人点了个奇怪的链接，自己什么也没输，但自己的qq号或其他的号就被盗了。即该攻击可以在受害者不知情的情况下以受害者名义伪造请求，执行恶意操作，具有很大的危害性。

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
http://xxx.com/vulnerabilities/csrf/?password_new=123&password_conf=123&Change=Change
```

# CSRF 是如何工作的？

要使用CSRF 攻击，必须具备三个关键条件：

- **一个相关的动作。**应用程序中存在攻击者有理由诱导的操作。这可能是特权操作（例如修改其他用户的权限）或针对用户特定数据的任何操作（例如更改用户自己的密码）。
- **基于 cookie 的会话处理。**执行该操作涉及发出一个或多个 HTTP 请求，应用程序仅依赖会话 cookie 来识别发出请求的用户。没有其他机制来跟踪会话或验证用户请求。
- **没有不可预测的请求参数。**执行操作的请求不包含任何参数，其值攻击者无法确定或猜测。例如，当导致用户更改密码时，如果攻击者需要知道现有密码的值，则该函数不易受到攻击。

# CSRF检测方法

1、看验证来源不-修复

2、看凭据有无csrf_tokne

3、看关键操作有无验证

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
<script src="http://xxx.com/vulnerabilities/csrf/?password_new=password&password_conf=password&Change=Change"
</body>
</html>
```

# CSRF防御方法

1.不要使用get请求，建议所有的涉及到数据的地方都使用post请求。

2.加入csrf_tokne（令牌）验证或者验证码，令牌是由服务器端应用程序生成并与客户端共享的唯一、秘密且不可预测的值。当尝试执行敏感操作（例如提交表单）时，客户端必须在请求中包含正确的 CSRF 令牌。这使得攻击者很难代表受害者构造有效请求。

3.加入referer，使用 HTTP Referer 标头来尝试抵御 CSRF 攻击，通过验证请求是否来自应用程序自己的域。这通常不如 CSRF 令牌验证有效。

# CSRF绕过方法

令牌验证取决于请求方法：有的csrf token只验证post请求，利用burp将post请求转换为get请求

令牌验证取决于令牌存在：删除csrf token部分

令牌未绑定到用户会话：csrf token未绑定用户，使用其他用户生成的csrf token攻击

令牌绑定到非会话 cookie：伪造cookie攻击

Referer 验证取决于标头是否存在：删除referer表头

不严谨的Referer 验证：直接伪造referer来源

csrf token存在上下文

![image-20210615161659041](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161659041.png)

![image-20210615161802996](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161802996.png)

![image-20210615161855295](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161855295.png)

![image-20210615161933240](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615161933240.png)

![image-20210615162104224](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615162104224.png)

![image-20210615162212003](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\CSRF跨站请求伪造\CSRF跨站请求伪造.assets\image-20210615162212003.png)

