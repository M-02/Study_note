## 思路说明:

反编译提取URL或抓包获取URL，进行WEB应用测试，如不存在或走其他协议的情况下，需采用网络接口抓包进行数据获取，转至其他协议安全测试!
#APP->WEB APP->其他APB->逆向
#WEB抓包，其他协议抓包演示及说明

burp抓包

Charles抓包

修改数据包访问如何做到漏洞扫描
利用扫描工具设置里面修改扫描的http头部

### burp联动xray：

burp打开User options选项，选择Upstream Proxy Servers，添加如下图

![image-20210908093833201](D:\BaiduNetdiskDownload\安全\漏洞发现\APP应用.assets\image-20210908093833201.png)

xray启动监听

```
xray webscan --listen 127.0.0.1:6666
```



#未逆向层面进行抓包区分各协议测试
#逆向层面进行提取APK代码层面数据

