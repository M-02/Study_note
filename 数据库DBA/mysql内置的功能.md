# mysql内置的功能
-u   指定用户名
-p   指定密码
-S   指定sock文件
-h   指定ip地址
-P   指定端口
-e   面交互直接执行SQL语句

<    导入SQL文件

例子

```shell
1.mysql -uroot -p -S /tmp/mysql.sock
2.mysql -uroot -p -h10.0.0.51 -P3306
3.mysql -uroot -p -e "show databeses;"
4.mysql -uroot -p1 < /root/ocp.sql
```

#### 内置命令

```
help  						打印mysql帮助
\c    Ctrl+d    			结束上个命令运行
\q  quit;  exit;  Ctrl+d    退出mysql  
\G							将数据竖起来显示
source						恢复备份文件

```

# sql基础应用

## sql介绍

结构化的查询语言
关系型数据库通用的命令
遵循SQL92的标准(SQL_MODE)

## SQL常用种类

DDL	数据定义语言
DCL	数据控制语言
DML	数据操作语言
DQL	数据查询语言

## SQL引入-数据库的逻辑结构

库
​		库名字
​		库属性：字符集，排序规则

表
​		表名
​		表属性：存储引擎类型，字符集，排序规则
​		列名
​		列属性：数据类型，约束，其他属性
​		数据行

### 字符集（charset）

相当于mysql的密码本（编码表）
show charset;				查看支持的字符类型

utf8								：3个字节
utf8mb4（建议使用） ：4个字节，支持emoji

#### 排序规则（collation）

对于英文字符串的，大小写的敏感

utf8mb4_generalci			大小写不敏感
utf8mb4_bin					   大小写敏感（拼音，日文）

#### 数据类型

##### 数字

| 类     | 类型      | 说明                                             |
| ------ | --------- | ------------------------------------------------ |
| 整数   | TINYINT   | 极小整数数据类型(0-255)                          |
| 整数   | SMALLINT  | 较小整数数据类型(-2^15 到2^15-1 )                |
| 整数   | MEDIUMINT | 中型整数数据类型                                 |
| 整数   | INT       | 常规(平均)大小的整数数据类型(-2^31 到2^31-1)     |
| 整数   | BIGINT    | 较大整数数据类型(-2 63到2^63-1 )                 |
| 浮点数 | FLOAT     | 小型单精度(四个字节)浮点数                       |
| 浮点数 | DOUBLE    | 常规双精度(八个字节)浮点数                       |
| 定点数 | DECIMAL   | 包含整数部分、小数部分或同时包括二者的精确值数值 |
| BIT    | BIT       | 位字段值                                         |

##### 字符串

| 类型       | 大小                  | 用途                            |
| :--------- | :-------------------- | :------------------------------ |
| CHAR       | 0-255 bytes           | 定长字符串                      |
| VARCHAR    | 0-65535 bytes         | 变长字符串                      |
| TINYBLOB   | 0-255 bytes           | 不超过 255 个字符的二进制字符串 |
| TINYTEXT   | 0-255 bytes           | 短文本字符串                    |
| BLOB       | 0-65 535 bytes        | 二进制形式的长文本数据          |
| TEXT       | 0-65 535 bytes        | 长文本数据                      |
| MEDIUMBLOB | 0-16 777 215 bytes    | 二进制形式的中等长度文本数据    |
| MEDIUMTEXT | 0-16 777 215 bytes    | 中等长度文本数据                |
| LONGBLOB   | 0-4 294 967 295 bytes | 二进制形式的极大文本数据        |
| LONGTEXT   | 0-4 294 967 295 bytes | 极大文本数据                    |

##### 时间

| 类型      | 大小 ( bytes) | 范围                                                         | 格式                | 用途                     |
| :-------- | :------------ | :----------------------------------------------------------- | :------------------ | :----------------------- |
| DATE      | 3             | 1000-01-01/9999-12-31                                        | YYYY-MM-DD          | 日期值                   |
| TIME      | 3             | '-838:59:59'/'838:59:59'                                     | HH:MM:SS            | 时间值或持续时间         |
| YEAR      | 1             | 1901/2155                                                    | YYYY                | 年份值                   |
| DATETIME  | 8             | 1000-01-01 00:00:00/9999-12-31 23:59:59                      | YYYY-MM-DD HH:MM:SS | 混合日期和时间值         |
| TIMESTAMP | 4             | 1970-01-01 00:00:00/2038结束时间是第 **2147483647** 秒，北京时间 **2038-1-19 11:14:07**，格林尼治时间 2038年1月19日 凌晨 03:14:07 | YYYYMMDD HHMMSS     | 混合日期和时间值，时间戳 |

##### 二进制

## DDL的应用

定义或改变表（TABLE）的结构，数据类型，表之间的链接和约束等初始化工作

#### DDL语句库的定义

创建库

```mysql
create database zabbix charset utf8mb4 collate utf8mb4_bin;

show databases;              	查看库情况
show create database zabbix;    查看库情况
```

删除库

```mysql
drop database zabbix;
```

修改数据库字符集

注意：一定是从小往大了改，比如utf8--->utf8mb4

目标的字符集一定是原字符集的超集

```mysql
alter database zabbix charset utf8mb4;
```

#### 库的定义规范

建库名称使用小写

库名不能以数字开头

不能是数据库内部的关键字

建库必须设置字符集

#### DDL表规范

建表

​		表名，列名，列属性，表属性

```
建表规范：
1.表名小写字母，不能数字开头，
2.不能是保留字符,使用和业务有关的表名
3.选择合适的数据类型及长度
4.每个列设置NOT NULL + DEFAULT .对于数据0填充,对于字符使用有效宇
5.没个列设置注释
6.表必须设置存储引擎和字符集
7.主键列尽量是无关列，最好是自增长
9.enum类型不要保存数字，只能是字符串类型
```



```
列属性：

​			PRIMARY KEY：主键约束
​			NOT NULL：非空约束，不允许控制
​			UNIQE KEY：唯一键约束，不允许重复值
​			DEFAULT：一般配合NOT NULL使用
​			UNSIGNED：无符号，一般配合数字列，非负数
​			COMMENT：注释
​			AUTO_INCREMENT：自增长的列
```

```mysql
CREATE TABLE stu (
id INT PRIMARY KEY NOT NULL AUTO INCREMENT COMMENT '学号',
sname VARCHAR (255) NOT NULL COMMENT '姓名'，
age TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '年龄',
gender ENUM( 'm', 'f', 'n') NOT NULL DEFAULT 'n' COMMENT '性别"，
intime DATETIME NOT NULL DEFAULT NOW() COMMENT '入学时间'
) ENGINE INNODB CHARSET utf8mb4;
```

查询建表信息

```mysql
SHOW TABLES;
SHOW CREATE TABLE stu;
CREATE TABLE test LIKE stu;       创建一个表结构一样的表
```

删表

```mysql
DROP TABLE test;
```

修改

在stu表中添加qq列

```php
DESC stu;
ALTER TABLE stu ADD qq VARCHAR(20) NOT NULL UNIQUE COMMENT 'qq号';
```

在sname后加微信列

```php
ALTER TABLE stu ADD wechat VARCHAR(64) NOT NULL UNIQUE  COMMENT '微信号' AFTER sname ;
```

在id列前加一个新列num

```dart
ALTER TABLE stu ADD num INT NOT NULL COMMENT '数字' FIRST;
DESC stu;
```

把刚才添加的列都删掉(危险)

```dart
ALTER TABLE stu DROP num;
ALTER TABLE stu DROP qq;
ALTER TABLE stu DROP wechat;
```

修改sname数据类型的属性

```cpp
ALTER TABLE stu MODIFY sname VARCHAR(128)  NOT NULL ;
```

将sgender 改为 sg  数据类型改为 CHAR 类型

```php
ALTER TABLE stu CHANGE sgender sg CHAR(1) NOT NULL DEFAULT 'n' ;
DESC stu;
```

#### 表属性查询（DQL）

```dart
use school
show tables；
desc stu;
show create table stu；
CREATE TABLE ceshi LIKE stu;
```

## DCL应用 

是数据库控制功能。是用来设置或更改数据库用户或角色权限的语句

```shell
grant 
revoke
```

## DML应用

##### 作用

```undefined
对表中的数据行进行增、删、改
```

#### insert

```csharp
--- 最标准的insert语句
INSERT INTO stu(id,sname,sage,sg,sfz,intime) 
VALUES
(1,'zs',18,'m','123456',NOW());
SELECT * FROM stu;

--- 省事的写法
INSERT INTO stu 
VALUES
(2,'ls',18,'m','1234567',NOW());

--- 针对性的录入数据
INSERT INTO stu(sname,sfz)
VALUES ('w5','34445788');

--- 同时录入多行数据
INSERT INTO stu(sname,sfz)
VALUES 
('w55','3444578d8'),
('m6','1212313'),
('aa','123213123123');

SELECT * FROM stu;
```

#### update

```bash
DESC stu;
SELECT * FROM stu;
UPDATE stu SET sname='zhao4' WHERE id=2;
注意：update语句必须要加where。
```

#### delete（危险！！）

```objectivec
DELETE FROM stu  WHERE id=3;
```

全表删除:

```cpp
DELETE FROM stu
truncate table stu;
区别:
delete: DML操作, 是逻辑性质删除,逐行进行删除,速度慢.
truncate: DDL操作,对与表段中的数据页进行清空,速度快.
```

伪删除：用update来替代delete，最终保证业务中查不到（select）即可

```objectivec
1.添加状态列
ALTER TABLE stu ADD state TINYINT NOT NULL DEFAULT 1 ;
SELECT * FROM stu;

2. UPDATE 替代 DELETE
UPDATE stu SET state=0 WHERE id=6;

3. 业务语句查询
SELECT * FROM stu WHERE state=1;
```

## DQL介绍

select

```mysql
select 列
from 表
where  条件
group  条件
having  条件
order by 条件
limit
```



## 扩展类内容-元数据获取

#### 元数据介绍及获取介绍

元数据存储在“基表”中。
通过专用DDL语句，DCL语句进行修改
通过专用视图和命令进行元数据查询
information_schema中保存了大量元数据查询的试图
show命令是封装好功能，提供基础元数据查询

#### information_schema的基本应用

##### tables视图的应用

```mysql
use in formation_ schema ;
desc tables ;

TABLE_SCHEMA		表所在的库名
TABLE_NAME			表名
ENGINE				存储引擎
TABLE_ROWS			数据行
AVG_ROW_LENGTH		平均行长度
INDEX_LENGTH		索引长度
```

例子：

1.显示所有的库和表的信息

```mysql
SELECT table schema, table_name FROM in formation_schema.tables;
```

2.以以下模式显示所有的库和表的信息
world：city , country , countrylanguage

```mysql
SELECT table_schema,GROUP_CONCAT(table_name)
FROM information_schema.tables
GROUP BY table_schema ;
```

3.查询所有innodb引擎的表

```mysql
SELECT table_schema,table_name,ENGINE
FROM information_schema.tables
WHERE ENGINE='innodb';
```

4.统计world下的city表占用空间大小
表的数据量=平均行长度*行数+索引长度

AVG_ROW_LENGTH*TABLE_ROWS+INDEX_LENGTH

```mysql
SELECT table_name,(AVG_ROW_LENGTH*TABLE_ROWS+INDEX_LENGTH)/1024
FROM information_schema.TABLES
WHERE table_schema='ocp' AND table_name= 'products';
```

5.统计world库数据量总大小

```mysql
SELECT table_schema,SUM((AVG_ROW_LENGTH*TABLE_ROWS+INDEX_LENGTH))/1024
FROM information_schema.TABLES 
WHERE table_schema='ocp';
```

6.统计每个库的数据量大小，并按数据量从大到小排序

```mysql
SELECT table_schema,SUM((AVG_ROW_LENGTH*TABLE_ROWS+INDEX_LENGTH))/1024
FROM information_schema.TABLES 
GROUP BY TABLE_SCHEMA;
ORDER BY SUM((AVG_ROW_LENGTH*TABLE_ROWS+INDEX_LENGTH))/1024 DESC;
```

##### 配合concat()函数拼接语句或命令

例子:
1.模仿以下语句，进行数据库的分库分表备份。

mysqldump -uroot -p123 world city >/bak/world_ city. sql

```mysql
SELECT
CONCAT("mysqldump -uroot -p123",table_schema," ",table_name
," >/bak/",table_schema," ",table_name,".sql")
FROM information_schema.tables;
```

2.模仿以下语句,进行批量生成对world库下所有表进行操作
ALTER TABLE world.city DISCARD TABLESPACE;

```mysql
SELECT
CONCAT("ALTER TABLE ",table_schema,".",table_name," DISCARD TABLESPACE;")
FROM information_schema.tables
WHERE table_schema='school';
```



#### show语句介绍

```mysql
show databases;                           #查看所有数据库
show tables;                              #查看当前库的所有表
SHOW TABLES FROM                          #查看某个指定库下的表
show create database world                #查看建库语句
show create table world.city              #查看建表语句
show  grants for  root@'localhost'        #查看用户的权限信息
show  charset;                            #查看字符集
show collation                            #查看校对规则
show processlist;                         #查看数据库连接情况
show index from                           #表的索引情况
show status                               #数据库状态查看
SHOW STATUS LIKE '%lock%';                #模糊查询数据库某些状态
SHOW VARIABLES                            #查看所有配置信息
SHOW variables LIKE '%lock%';             #查看部分配置信息
show engines                              #查看支持的所有的存储引擎
show engine innodb status\G               #查看InnoDB引擎相关的状态信息
show binary logs                          #列举所有的二进制日志
show master status                        #查看数据库的日志位置信息
show binlog evnets in                     #查看二进制日志事件
show slave status \G                      #查看从库状态
SHOW RELAYLOG EVENTS in ''                #查看从库relaylog事件信息
desc  (show colums from city)             #查看表的列定义信息
```

