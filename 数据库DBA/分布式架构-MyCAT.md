# 1. MyCAT基础架构图

![img](https:////upload-images.jianshu.io/upload_images/16956686-7e5ff50e4071c7eb.png?imageMogr2/auto-orient/strip|imageView2/2/w/843/format/webp)

image.png

# 2. MyCAT基础架构准备

## 2.1 环境准备：



```undefined
两台虚拟机 db01 db02
每台创建四个mysql实例：3307 3308 3309 3310
```

## 2.2 删除历史环境：



```kotlin
pkill mysqld
rm -rf /data/330* 
mv /etc/my.cnf /etc/my.cnf.bak
```

## 2.3 创建相关目录初始化数据



```kotlin
mkdir /data/33{07..10}/data -p
mysqld --initialize-insecure  --user=mysql --datadir=/data/3307/data --basedir=/application/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/data/3308/data --basedir=/application/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/data/3309/data --basedir=/application/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/data/3310/data --basedir=/application/mysql
```

## 2.4 准备配置文件和启动脚本



```cnf
========db01==============
cat >/data/3307/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3307/data
socket=/data/3307/mysql.sock
port=3307
log-error=/data/3307/mysql.log
log_bin=/data/3307/mysql-bin
binlog_format=row
skip-name-resolve
server-id=7
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF

cat >/data/3308/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3308/data
port=3308
socket=/data/3308/mysql.sock
log-error=/data/3308/mysql.log
log_bin=/data/3308/mysql-bin
binlog_format=row
skip-name-resolve
server-id=8
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF

cat >/data/3309/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3309/data
socket=/data/3309/mysql.sock
port=3309
log-error=/data/3309/mysql.log
log_bin=/data/3309/mysql-bin
binlog_format=row
skip-name-resolve
server-id=9
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF
cat >/data/3310/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3310/data
socket=/data/3310/mysql.sock
port=3310
log-error=/data/3310/mysql.log
log_bin=/data/3310/mysql-bin
binlog_format=row
skip-name-resolve
server-id=10
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF

cat >/etc/systemd/system/mysqld3307.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3307/my.cnf
LimitNOFILE = 5000
EOF

cat >/etc/systemd/system/mysqld3308.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3308/my.cnf
LimitNOFILE = 5000
EOF

cat >/etc/systemd/system/mysqld3309.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3309/my.cnf
LimitNOFILE = 5000
EOF
cat >/etc/systemd/system/mysqld3310.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3310/my.cnf
LimitNOFILE = 5000
EOF



========db02===============
cat >/data/3307/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3307/data
socket=/data/3307/mysql.sock
port=3307
log-error=/data/3307/mysql.log
log_bin=/data/3307/mysql-bin
binlog_format=row
skip-name-resolve
server-id=17
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF
cat >/data/3308/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3308/data
port=3308
socket=/data/3308/mysql.sock
log-error=/data/3308/mysql.log
log_bin=/data/3308/mysql-bin
binlog_format=row
skip-name-resolve
server-id=18
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF
cat >/data/3309/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3309/data
socket=/data/3309/mysql.sock
port=3309
log-error=/data/3309/mysql.log
log_bin=/data/3309/mysql-bin
binlog_format=row
skip-name-resolve
server-id=19
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF


cat >/data/3310/my.cnf<<EOF
[mysqld]
basedir=/application/mysql
datadir=/data/3310/data
socket=/data/3310/mysql.sock
port=3310
log-error=/data/3310/mysql.log
log_bin=/data/3310/mysql-bin
binlog_format=row
skip-name-resolve
server-id=20
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
EOF

cat >/etc/systemd/system/mysqld3307.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3307/my.cnf
LimitNOFILE = 5000
EOF

cat >/etc/systemd/system/mysqld3308.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3308/my.cnf
LimitNOFILE = 5000
EOF

cat >/etc/systemd/system/mysqld3309.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3309/my.cnf
LimitNOFILE = 5000
EOF
cat >/etc/systemd/system/mysqld3310.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3310/my.cnf
LimitNOFILE = 5000
EOF
```

## 2.5 修改权限，启动多实例



```kotlin
chown -R mysql.mysql /data/*
systemctl start mysqld3307
systemctl start mysqld3308
systemctl start mysqld3309
systemctl start mysqld3310

mysql -S /data/3307/mysql.sock -e "show variables like 'server_id'"
mysql -S /data/3308/mysql.sock -e "show variables like 'server_id'"
mysql -S /data/3309/mysql.sock -e "show variables like 'server_id'"
mysql -S /data/3310/mysql.sock -e "show variables like 'server_id'"
```

## 2.6 节点主从规划



```css
箭头指向谁是主库
    10.0.0.51:3307    <----->  10.0.0.52:3307
    10.0.0.51:3309    ------>  10.0.0.51:3307
    10.0.0.52:3309    ------>  10.0.0.52:3307

    10.0.0.52:3308  <----->    10.0.0.51:3308
    10.0.0.52:3310  ----->     10.0.0.52:3308
    10.0.0.51:3310  ----->     10.0.0.51:3308
```

## 2.7 分片规划



```css
shard1：
    Master：10.0.0.51:3307
    slave1：10.0.0.51:3309
    Standby Master：10.0.0.52:3307
    slave2：10.0.0.52:3309
shard2：
    Master：10.0.0.52:3308
    slave1：10.0.0.52:3310
    Standby Master：10.0.0.51:3308
    slave2：10.0.0.51:3310
```

## 2.8 开始配置

### 第一组四节点结构

#### 10.0.0.51:3307    <----->  10.0.0.52:3307

##### db02



```kotlin
mysql  -S /data/3307/mysql.sock -e "grant replication slave on *.* to repl@'10.0.0.%' identified by '123';"
mysql  -S /data/3307/mysql.sock -e "grant all  on *.* to root@'10.0.0.%' identified by '123'  with grant option;"
```

##### db01



```kotlin
mysql  -S /data/3307/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.52', MASTER_PORT=3307, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3307/mysql.sock -e "start slave;"
mysql  -S /data/3307/mysql.sock -e "show slave status\G"
```

##### db02



```kotlin
mysql  -S /data/3307/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.51', MASTER_PORT=3307, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3307/mysql.sock -e "start slave;"
mysql  -S /data/3307/mysql.sock -e "show slave status\G"
```

#### 10.0.0.51:3309    ------>  10.0.0.51:3307

##### db01



```kotlin
mysql  -S /data/3309/mysql.sock  -e "CHANGE MASTER TO MASTER_HOST='10.0.0.51', MASTER_PORT=3307, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3309/mysql.sock  -e "start slave;"
mysql  -S /data/3309/mysql.sock  -e "show slave status\G"
```

#### 10.0.0.52:3309    ------>  10.0.0.52:3307

##### db02



```kotlin
mysql  -S /data/3309/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.52', MASTER_PORT=3307, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3309/mysql.sock -e "start slave;"
mysql  -S /data/3309/mysql.sock -e "show slave status\G"
```

### 第二组四节点结构

#### 10.0.0.52:3308  <----->    10.0.0.51:3308

##### db01



```kotlin
mysql  -S /data/3308/mysql.sock -e "grant replication slave on *.* to repl@'10.0.0.%' identified by '123';"
mysql  -S /data/3308/mysql.sock -e "grant all  on *.* to root@'10.0.0.%' identified by '123'  with grant option;"
```

##### db02



```kotlin
mysql  -S /data/3308/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.51', MASTER_PORT=3308, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3308/mysql.sock -e "start slave;"
mysql  -S /data/3308/mysql.sock -e "show slave status\G"
```

##### db01



```kotlin
mysql  -S /data/3308/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.52', MASTER_PORT=3308, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3308/mysql.sock -e "start slave;"
mysql  -S /data/3308/mysql.sock -e "show slave status\G"
```

#### 10.0.0.52:3310    ----->       10.0.0.52:3308

##### db02



```kotlin
mysql  -S /data/3310/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.52', MASTER_PORT=3308, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3310/mysql.sock -e "start slave;"
mysql  -S /data/3310/mysql.sock -e "show slave status\G"
```

#### 10.0.0.51:3310  ----->     10.0.0.51:3308

##### db01



```kotlin
mysql  -S /data/3310/mysql.sock -e "CHANGE MASTER TO MASTER_HOST='10.0.0.51', MASTER_PORT=3308, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';"
mysql  -S /data/3310/mysql.sock -e "start slave;"
mysql  -S /data/3310/mysql.sock -e "show slave status\G"
```

## 2.9 检测主从状态

```shell
mysql -S /data/3307/mysql.sock -e "show slave status\G"|grep Yes
mysql -S /data/3308/mysql.sock -e "show slave status\G"|grep Yes
mysql -S /data/3309/mysql.sock -e "show slave status\G"|grep Yes
mysql -S /data/3310/mysql.sock -e "show slave status\G"|grep Yes

注：如果中间出现错误，在每个节点进行执行以下命令
mysql -S /data/3307/mysql.sock -e "stop slave; reset slave all;"
mysql -S /data/3308/mysql.sock -e "stop slave; reset slave all;"
mysql -S /data/3309/mysql.sock -e "stop slave; reset slave all;"
mysql -S /data/3310/mysql.sock -e "stop slave; reset slave all;"
```



## 2.10 MySQL分布式架构介绍

![img](https:////upload-images.jianshu.io/upload_images/16956686-7c753fb3640bc0ec.png?imageMogr2/auto-orient/strip|imageView2/2/w/475/format/webp)

image.png



```undefined
1. schema拆分及业务分库
2. 垂直拆分-分库分表
3. 水平拆分-分片，range，取模，枚举，hash，时间等等

```

## 2.11 企业代表产品



```undefined
360 Atlas-Sharding
Alibaba  cobar 
Mycat
TDDL
Heisenberg
Oceanus
Vitess
OneProxy 
DRDS
```

# 3. MyCAT安装

## 3.1 预先安装Java运行环境



```undefined
yum install -y java
```

## 3.2下载



```cpp
Mycat-server-xxxxx.linux.tar.gz
http://dl.mycat.io/
```

## 3.3 解压文件



```css
tar xf Mycat-server-1.6.5-release-20180122220033-linux.tar.gz
```

## 3.4 软件目录结构



```css
ls
bin  catlet  conf  lib  logs  version.txt
```

## 3.5 启动和连接



```bash
配置环境变量
vim /etc/profile
export PATH=/application/mycat/bin:$PATH
source /etc/profile
启动
mycat start
连接mycat：
mysql -uroot -p123456 -h 127.0.0.1 -P8066
```

# 4. 配置文件介绍



```css
logs目录:
wrapper.log       ---->mycat启动日志
mycat.log         ---->mycat详细工作日志
conf目录:
schema.xml      
主配置文件（读写分离、高可用、分布式策略定制、节点控制）
server.xml
mycat软件本身相关的配置
rule.xml 
分片规则配置文件,记录分片规则列表、使用方法等
```

# 5.应用前环境准备

## 5.1 用户创建及数据库导入



```kotlin
db01:
mysql -S /data/3307/mysql.sock 
grant all on *.* to root@'10.0.0.%' identified by '123';
source /root/ocp.sql

mysql -S /data/3308/mysql.sock 
grant all on *.* to root@'10.0.0.%' identified by '123';
source /root/world.sql
```

## 5.2 配置文件处理



```xml
cd /application/mycat/conf

mv schema.xml schema.xml.bak

vim schema.xml 

<?xml version="1.0"?>  
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">  
<mycat:schema xmlns:mycat="http://io.mycat/">
<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="dn1"> 
</schema>  
    <dataNode name="dn1" dataHost="localhost1" database= "wordpress" />  
    <dataHost name="localhost1" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1"> 
        <heartbeat>select user()</heartbeat>  
    <writeHost host="db1" url="10.0.0.51:3307" user="root" password="123"> 
            <readHost host="db2" url="10.0.0.51:3309" user="root" password="123" /> 
    </writeHost> 
    </dataHost>  
</mycat:schema>
```

# 6. 配置文件简单介绍

## 6.1 逻辑库：schema



```xml
<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="dn1"> 
</schema>  
```

## 6.2 数据节点:datanode



```xml
<dataNode name="dn1" dataHost="localhost1" database= "world" />  
```

## 6.3 数据主机：datahost(w和r)



```xml
<dataHost name="localhost1" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1"> 
        <heartbeat>select user()</heartbeat>  
    <writeHost host="db1" url="10.0.0.51:3307" user="root" password="123"> 
            <readHost host="db2" url="10.0.0.52:3309" user="root" password="123" /> 
    </writeHost> 
    </dataHost>  
```

# 7. 读写分离结构配置



```xml
vim schema.xml 

<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">  
<mycat:schema xmlns:mycat="http://io.mycat/">
<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="sh1"> 
</schema>  
        <dataNode name="sh1" dataHost="oldguo1" database= "world" />         
        <dataHost name="oldguo1" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1">    
                <heartbeat>select user()</heartbeat>  
        <writeHost host="db1" url="10.0.0.51:3307" user="root" password="123"> 
                        <readHost host="db2" url="10.0.0.51:3309" user="root" password="123" /> 
        </writeHost> 
        </dataHost>  
</mycat:schema>

重启mycat
mycat restart

读写分离测试
 mysql -uroot -p -h 127.0.0.1 -P8066
 show variables like 'server_id';
 begin;
 show variables like 'server_id';

总结： 
以上案例实现了1主1从的读写分离功能，写操作落到主库，读操作落到从库.如果主库宕机，从库不能在继续提供服务了。
```

# 8. 配置读写分离及高可用



```xml
[root@db01 conf]# mv schema.xml schema.xml.rw
[root@db01 conf]# vim schema.xml

<?xml version="1.0"?>  
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">  
<mycat:schema xmlns:mycat="http://io.mycat/">
<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="sh1"> 
</schema>  
    <dataNode name="sh1" dataHost="oldguo1" database= "ocp" />  
    <dataHost name="oldguo1" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1"> 
        <heartbeat>select user()</heartbeat>  
    <writeHost host="db1" url="10.0.0.51:3307" user="root" password="123"> 
            <readHost host="db2" url="10.0.0.51:3309" user="root" password="123" /> 
    </writeHost> 
    <writeHost host="db3" url="10.0.0.52:3307" user="root" password="123"> 
            <readHost host="db4" url="10.0.0.52:3309" user="root" password="123" /> 
    </writeHost>        
    </dataHost>  
</mycat:schema>

第一个writeHost: 10.0.0.51:3307	真正的写节点,负责写操作
第二个writeHost: 10.0.0.52:3307	standby准备写节点，负责读,当10.0.0.51:3307宕掉,会切换为真正的写节点

当写节点宕机后，后面跟的readhost也不提供服务，这时候standby的writehost就提供写服务，
后面跟的readhost提供读服务

测试：
mysql -uroot -p123456 -h 127.0.0.1 -P 8066
show variables like 'server_id';
读写分离测试
 mysql -uroot -p -h 127.0.0.1 -P8066
 show variables like 'server_id';
 show variables like 'server_id';
 show variables like 'server_id';
 begin;
 show variables like 'server_id';
 对db01 3307节点进行关闭和启动,测试读写操作
 
```

# 9. 配置中的属性介绍:

## balance属性



```csharp
负载均衡类型，目前的取值有3种： 
1. balance="0", 不开启读写分离机制，所有读操作都发送到当前可用的writeHost上。 
2. balance="1"，全部的readHost与standby writeHost参与select语句的负载均衡，简单的说，
  当双主双从模式(M1->S1，M2->S2，并且M1与 M2互为主备)，正常情况下，M2,S1,S2都参与select语句的负载均衡。 
3. balance="2"，所有读操作都随机的在writeHost、readhost上分发。
```

## writeType属性



```ruby
负载均衡类型，目前的取值有2种： 
1. writeType="0", 所有写操作发送到配置的第一个writeHost，
第一个挂了切到还生存的第二个writeHost，重新启动后已切换后的为主，切换记录在配置文件中:dnindex.properties . 
2. writeType=“1”，所有写操作都随机的发送到配置的writeHost，但不推荐使用
```

## switchType属性



```dart
-1 表示不自动切换 
1 默认值，自动切换 
2 基于MySQL主从同步的状态决定是否切换 ，心跳语句为 show slave status 
```

## datahost其他配置



```csharp
<dataHost name="localhost1" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1"> 

maxCon="1000"：最大的并发连接数
minCon="10" ：mycat在启动之后，会在后端节点上自动开启的连接线程
tempReadHostAvailable="1"
这个一主一从时（1个writehost，1个readhost时），可以开启这个参数，如果2个writehost，2个readhost时
<heartbeat>select user()</heartbeat>  监测心跳
```

# 10. 垂直分表

![img](https:////upload-images.jianshu.io/upload_images/16956686-c188becb93fdef0f.png?imageMogr2/auto-orient/strip|imageView2/2/w/1059/format/webp)

image.png



![img](https:////upload-images.jianshu.io/upload_images/16956686-96987959032a94c2.png?imageMogr2/auto-orient/strip|imageView2/2/w/1063/format/webp)

image.png



```xml
mv  schema.xml  schema.xml.ha 

vim schema.xml

<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">
<mycat:schema xmlns:mycat="http://io.mycat/">
<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="sh1">
        <table name="user" dataNode="sh1"/>
        <table name="order" dataNode="sh2"/>
</schema>
    <dataNode name="sh1" dataHost="oldguo1" database= "ocp" />
    <dataNode name="sh2" dataHost="oldguo2" database= "ocp" />
    <dataHost name="oldguo1" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1">
        <heartbeat>select user()</heartbeat>
    <writeHost host="db1" url="10.0.0.51:3307" user="root" password="123">
            <readHost host="db2" url="10.0.0.51:3309" user="root" password="123" />
    </writeHost>
    <writeHost host="db3" url="10.0.0.52:3307" user="root" password="123">
            <readHost host="db4" url="10.0.0.52:3309" user="root" password="123" />
    </writeHost>
    </dataHost>
    <dataHost name="oldguo2" maxCon="1000" minCon="10" balance="1"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1">
        <heartbeat>select user()</heartbeat>
    <writeHost host="db1" url="10.0.0.51:3308" user="root" password="123">
            <readHost host="db2" url="10.0.0.51:3310" user="root" password="123" />
    </writeHost>
    <writeHost host="db3" url="10.0.0.52:3308" user="root" password="123">
            <readHost host="db4" url="10.0.0.52:3310" user="root" password="123" />
    </writeHost>
    </dataHost>
</mycat:schema>

创建测试库和表:
[root@db01 conf]# mysql -S /data/3307/mysql.sock -e "create database taobao charset utf8;"
[root@db01 conf]# mysql -S /data/3308/mysql.sock -e "create database taobao charset utf8;"
[root@db01 conf]# mysql -S /data/3307/mysql.sock -e "use taobao;create table user(id int,name varchar(20))";
[root@db01 conf]# mysql -S /data/3308/mysql.sock -e "use taobao;create table order_t(id int,name varchar(20))"



```

# 11. MyCAT核心特性——分片（水平拆分）



```bash
分片：对一个"bigtable"，比如说t3表

(1)行数非常多，800w
(2)访问非常频繁

分片的目的：
（1）将大数据量进行分布存储
（2）提供均衡的访问路由

分片策略：
范围 range  800w  1-400w 400w01-800w
取模 mod    取余数
枚举 
哈希 hash 
时间 流水

优化关联查询
全局表
ER分片
```

# 12 .范围分片

![img](https:////upload-images.jianshu.io/upload_images/16956686-71a4dc83c387d7b0.png?imageMogr2/auto-orient/strip|imageView2/2/w/933/format/webp)

image.png



```csharp
比如说t3表
(1)行数非常多，2000w（1-1000w:sh1   1000w01-2000w:sh2）
(2)访问非常频繁，用户访问较离散
mv schema.xml schema.xml.1  
vim schema.xml
<schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100" dataNode="sh1"> 
        <table name="t3" dataNode="sh1,sh2" rule="auto-sharding-long" />
</schema>  
    <dataNode name="sh1" dataHost="oldguo1" database= "taobao" /> 
    <dataNode name="sh2" dataHost="oldguo2" database= "taobao" />  

vim rule.xml
<tableRule name="auto-sharding-long">
                <rule>
                        <columns>id</columns>
                        <algorithm>rang-long</algorithm>
                </rule>             
<function name="rang-long"
    class="io.mycat.route.function.AutoPartitionByLong">
    <property name="mapFile">autopartition-long.txt</property>
</function>
===================================         
vim autopartition-long.txt
0-10=0	------>  0<x<=10
11-20=1	------>  10<x<=20

创建测试表：
mysql -S /data/3307/mysql.sock -e "use taobao;create table t3 (id int not null primary key auto_increment,name varchar(20) not null);"

mysql -S /data/3308/mysql.sock  -e "use taobao;create table t3 (id int not null primary key auto_increment,name varchar(20) not null);"

测试：
重启mycat
mycat restart
mysql -uroot -p123456 -h 127.0.0.1 -P 8066
insert into t3(id,name) values(1,'a');
insert into t3(id,name) values(2,'b');
insert into t3(id,name) values(3,'c');
insert into t3(id,name) values(4,'d');
insert into t3(id,name) values(10,'aa');
insert into t3(id,name) values(11,'aa');
insert into t3(id,name) values(12,'bb');
insert into t3(id,name) values(13,'cc');
insert into t3(id,name) values(14,'dd');
insert into t3(id,name) values(20,'dd');
```

# 13. 取模分片（mod-long）：



```csharp
取余分片方式：分片键（一个列）与节点数量进行取余，得到余数，将数据写入对应节点
vim schema.xml
<table name="t4" dataNode="sh1,sh2" rule="mod-long" />
vim rule.xml
<property name="count">2</property>

准备测试环境
     
创建测试表：
mysql -S /data/3307/mysql.sock -e "use taobao;create table t4 (id int not null primary key auto_increment,name varchar(20) not null);"
mysql -S /data/3308/mysql.sock -e "use taobao;create table t4 (id int not null primary key auto_increment,name varchar(20) not null);"

重启mycat 
mycat restart 

测试： 
mysql -uroot -p123456 -h10.0.0.51 -P8066

use TESTDB
insert into t4(id,name) values(1,'a');
insert into t4(id,name) values(2,'b');
insert into t4(id,name) values(3,'c');
insert into t4(id,name) values(4,'d');

分别登录后端节点查询数据
mysql -S /data/3307/mysql.sock -e "select * from taobao.t4;"

mysql -S /data/3308/mysql.sock -e "select * from taobao.t4;"
```

# 14. 枚举分片



```csharp
t5 表
id name telnum
1   bj   1212
2   sh   22222
3   bj   3333
4   sh   44444
5   bj   5555

sharding-by-intfile
vim schema.xml
<table name="t5" dataNode="sh1,sh2" rule="sharding-by-intfile" />

vim rule.xml
<tableRule name="sharding-by-intfile"> 
<rule> <columns>name</columns> 
<algorithm>hash-int</algorithm> 
</rule> 
</tableRule> 

<function name="hash-int" class="org.opencloudb.route.function.PartitionByFileMap"> 
<property name="mapFile">partition-hash-int.txt</property> 
  <property name="type">1</property>
                <property name="defaultNode">0</property>
</function> 

partition-hash-int.txt 配置： 
bj=0 
sh=1
DEFAULT_NODE=1 
columns 标识将要分片的表字段，algorithm 分片函数， 其中分片函数配置中，mapFile标识配置文件名称

准备测试环境
mysql -S /data/3307/mysql.sock -e "use taobao;create table t5 (id int not null primary key auto_increment,name varchar(20) not null);"

mysql -S /data/3308/mysql.sock -e "use taobao;create table t5 (id int not null primary key auto_increment,name varchar(20) not null);"
重启mycat 
mycat restart 
mysql -uroot -p123456 -h10.0.0.51 -P8066
use TESTDB
insert into t5(id,name) values(1,'bj');
insert into t5(id,name) values(2,'sh');
insert into t5(id,name) values(3,'bj');
insert into t5(id,name) values(4,'sh');
insert into t5(id,name) values(5,'tj');

分别登录后端节点查询数据
mysql -S /data/3307/mysql.sock -e "select * from taobao.t5;"

mysql -S /data/3308/mysql.sock -e "select * from taobao.t5;"
```

# 15 .  Mycat全局表



```csharp
a   b   c  d   
join 
t 

select  t1.name   ,t.x  from  t1 
join t 
select  t2.name   ,t.x  from  t2 
join t 
select  t3.name   ,t.x  from  t3 
join t 

使用场景：
如果你的业务中有些数据类似于数据字典，比如配置文件的配置，
常用业务的配置或者数据量不大很少变动的表，这些表往往不是特别大，
而且大部分的业务场景都会用到，那么这种表适合于Mycat全局表，无须对数据进行切分，
要在所有的分片上保存一份数据即可，Mycat 在Join操作中，业务表与全局表进行Join聚合会优先选择相同分片内的全局表join，
避免跨库Join，在进行数据插入操作时，mycat将把数据分发到全局表对应的所有分片执行，在进行数据读取时候将会随机获取一个节点读取数据。 

vim schema.xml 
<table name="t_area" primaryKey="id"  type="global" dataNode="sh1,sh2" /> 

后端数据准备
mysql -S /data/3307/mysql.sock 
use taobao
create table t_area (id int not null primary key auto_increment,name varchar(20) not null);

mysql -S /data/3308/mysql.sock 
use taobao
create table t_area  (id int not null primary key auto_increment,name varchar(20) not null);

重启mycat 
mycat restart 

测试： 
mysql -uroot -p123456 -h10.0.0.52 -P8066

use TESTDB
insert into t_area(id,name) values(1,'a');
insert into t_area(id,name) values(2,'b');
insert into t_area(id,name) values(3,'c');
insert into t_area(id,name) values(4,'d');
```

# 16. E-R分片



```csharp
A 
join 
B  
为了防止跨分片join，可以使用E-R模式
A   join   B
on  a.xx=b.yy
join C
on A.id=C.id
<table name="A" dataNode="sh1,sh2" rule="mod-long"> 
       <childTable name="B" joinKey="yy" parentKey="xx" /> 
</table> 
```



