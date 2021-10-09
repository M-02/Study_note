# SSRF漏洞原理与危害

![image-20210615162750858](D:\BaiduNetdiskDownload\安全\SSRF漏洞原理与危害\SSRF漏洞原理与危害.assets\image-20210615162750858.png)

**SSRF(Server-Side Request Forgery:服务器端请求伪造)**

其形成的原因大都是由于服务端**提供了从其他服务器应用获取数据的功能**,但又没有对目标地址做严格过滤与限制

导致攻击者可以传入任意的地址来让后端服务器对其发起请求,并返回对该目标地址请求的数据

数据流:攻击者----->服务器---->目标地址

根据后台使用的函数的不同,对应的影响和利用方法又有不一样

```
PHP中下面函数的使用不当会导致SSRF:
file_get_contents()
fsockopen()
curl_exec()       
```

# SSRF漏洞检测与防御

```
http://daishen.ltd:1113/vul/ssrf/ssrf_curl.php?url=dict://127.0.0.1:3306/
http://daishen.ltd:1113/vul/ssrf/ssrf_curl.php?url=file:///etc/passwd
```

防御

禁止跳转

过滤所有的访问信息

禁用不需要应用的协议，如file://,dict://,ldap://,gopher://,sftp://

限制请求的端口

# SSRF漏洞绕过

127.0.0.1
8进制格式: 0300.0250.0.1
16进制格式: 0xC0.0xA8.0.1
10进制整数格式: 3232235521
16进制整数格式: 0xC0A80001

127.0.0.1.xip.io

短地址：http://dwz.cn/11SMa
127。0。0。1

