## SQL Injection (mitigation)

防御sql注入，其实就是session,参数绑定，存储过程这样的注入。

```
//利用session防御，session内容正常情况下是用户无法修改的
select *from users where user = "'" + session.getAttribute ("UserID")+"'";
```

```
// 参数绑定方式， 利用了sql的预编译技术
String query = " SELECT * FROM users WHERE last_name = ?";
PreparedStatement statement = connection.prepareStatement(query) ;
statement.setString(1,accountName);
ResultSet results = statement.executeQuery();
```

使用PreparedStatement的参数化的查询可以阻止大部分的SQL注入。在使用参数化查询的情况下，数据库系统不会将参数的内容视为SQL指令的处理，而是在数据库完成SQL指令的编译后,才用参数运行，因此就算参数中含有破坏性的指令，也不会被数据库所运行。因为对于参数化查询来说,
SQL语句的格式是已经规定好了的，需要查的数据也设置好了缺的只是具体的那几个数据而已。所以用户能提供的只是数据,而且只能按需提供，无法做出影响数据库的其他举动来。

上面说的方式也不是能够绝对的进行sql注入防御，只是减轻。

如参数绑定方式可以使用下面方式绕过。
通过使用case when语句可以将order by后的orderExpression表达式中添加select语句。

## 什么是JWT?

JSON web Token (JSON web令牌)是种跨域验证身份的方案。JWT不加密传输的数据，但能够通过数字签名来验证数据未被篡改
JWT分为三部分，头部(Header) ，声明(Claima) ，签名(signature) ，三个部分以英文句号.隔开。JWT的内容以Base64URI进行了编码。

![image-20210901155025385](D:\BaiduNetdiskDownload\安全\JAVA安全\JAVA安全-JWT安全及预编译CASE注入等.assets\image-20210901155025385.png)

```
头部(Header)
{
"alg": "HS256", 
"typ": " JWT"
}
alg
是说明这个JWT的签名使用的算法的参数，常见值用HS256 (默认)，HS512等， 也可以为None。Hs256表示HMAC SHA256。
typ
说明这个token的类型为JWT


声明(claims)
"exp": 1416471934,
"user_ name": "user",
"scope": [
"read" ,
"write"
],
"authorities": [
"ROLE_ADMIN",
"ROLE_USER"
]，
"jti": "9bc92a44-0b1a-4c5e-be70-da52075b9a84",
"client_id": "my-client-with-secret"

Jwr固定参数有:
iss:发行人
exp:到期时间
sub:主题
aud:用户
nbf:在此之前不可用
iat:发布时间
jti: JWT ID用于标识该JWT


签名(Signature)
服务器有一个不会发送给客户端的密码(secret)用头部中指定的算法对头部和声明的内容用此密码进行加密，生成的字符串就是JWT的签名。
下面是个用HS256生成JWT的代码例子
HMACSHA256(base64UrlEncode (header) + "."+base64UrlEncode (payload)，secret)
1、用户端登录，用户名和密码在请求中被发往服务器
2、(确认登录信息正确后) 服务器生成JSON头部和声明，将登录信息写入JSON的声明中(通常不应写入密码，因为JWT是不加密的)，并用secret用指定算法进行加密，生成该用户的JWT。此时，服务器并没有保存登录状态信息。
3、服务器将JWT (通过响应)返回给客户端
4、用户下次会话时，客户端会自动将JWT写在HTTe请求头部的Authorization字段中
5、服务器对JwT进行验证，若验证成功，则确认此用户的登录状态
6、服务器返回响应

```

## JWT修改攻击思路：

更改"alg": "HS256"为"alg": "none"，base64加密，更改声明数据，签名留空

