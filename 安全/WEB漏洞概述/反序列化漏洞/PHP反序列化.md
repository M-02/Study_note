![image-20210825102812677](D:\BaiduNetdiskDownload\安全\反序列化漏洞\PHP反序列化.assets\image-20210825102812677.png)

![image-20210825103111195](D:\BaiduNetdiskDownload\安全\反序列化漏洞\PHP反序列化.assets\image-20210825103111195.png)

## PHP反序列化

原理:未对用户输入的序列化字符串进行检测，导致攻击者可以控制反序列化过程，
从而导致代码执行，SQL注入，目录遍历等不可控后果。在反序列化的过程中自动触发
了某些魔术方法。 当进行反序列化的时候就有 可能会触发对象中的一些魔术方法。

```
serialize()		//将一个对象转换成一个字符串
unserialize()	//将字符串还原成一个对象
```

触发: unserialize函数的变量可控,文件中存在可利用的类，类中有魔术方法:

```
_construct () 	//创建对象时触发
_destruct() 	//对象被销毁时触发
_call () 		//在对象上下文中调用不可访问的方法时触发
_callStatic()	//在静态 上下文中调用不可访问的方法时触发
_get () 		//用于从不可访问的属性读取数据
_set() 			//用于将数据写入不可访问的属性
_isset() 		//在不可访问的属性上调用isset()或empty()触发
_unset () 		//在不可访问的属性上使用unset()时触发
_invoke() 		//当脚本尝试将对象调用为函数时触发

```

![image-20210825104117837](D:\BaiduNetdiskDownload\安全\反序列化漏洞\PHP反序列化.assets\image-20210825104117837.png)

