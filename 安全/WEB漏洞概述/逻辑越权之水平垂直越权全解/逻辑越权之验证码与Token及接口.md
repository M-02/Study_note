![image-20210824152808847](D:\BaiduNetdiskDownload\安全\逻辑越权之水平垂直越权全解\逻辑越权之验证码与Token及接口.assets\image-20210824152808847.png)

## 验证码安全

分类:图片，手机或邮箱，语音，视频，操作等
原理:验证生成或验证过程中的逻辑问题
危害:账户权限泄漏，短信轰炸，遍历，任意用户操作等
漏洞:客户端回显，验证码复用，验证码爆破，绕过等

## token安全

基本上述同理，主要是验证中可存在绕过可继续后续测试
token爆破，token客户端回显等

token爆破:

1.抓包，发送到intruder模块，

2.Payload Positions，Attack type选择Pitchfork模式

3.添加变量

4.payload选择Recursive grep

5.Resource Pool选择单线程

6.Options选项找到Grep - Extract，点击add，找到抓到的包，搜索关键字，选中token，确定，如果没有，点击Refetch response

7.点击Start attack进行攻击



## 验证码识别插件工具使用

captcha-killer, Pkav_Http_Fuzz, reCAPTCHA等

## 接口安全问题

调用，遍历，未授权，篡改等
调用案例:短信轰炸
遍历案列: UI D等遍历

callback回调JSON

