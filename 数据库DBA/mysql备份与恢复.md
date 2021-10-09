# 1. 运维在数据库备份恢复方面的职责

## 1.1 设计备份策略



```undefined

备份周期:根据数据量，
备份工具: mysq1dump (MDP) ，XBK (PBK) percona Xtrabackup,
MEB (MySQL Enterprise BACKUP MEB ) mysqlbinlog
备份方式:
逻辑备份：
	全备：mysqldump
	增量：binlog（flush logs，cp）
物理备份：
	全备：XBK
	增量：XBK
```

## 1.2 日常备份检查



```undefined
crontab -l		查看是否存在备份脚本
备份脚本
备份路径
看备份日志，检查备份文件（大小，内容）


备份存在性
备份空间够用否
```

## 1.3 定期恢复演练(测试库)



```undefined
一季度 或者 半年
```

## 1.4 故障恢复



```undefined
通过现有完整的备份完整的日志,能够将数据库恢复到故障之前的时间点.（快速）       
```

## 1.5 迁移



```undefined
mysql -> mysql
其他 -> mysql
mysql -> 其他
不同操作系统迁移

1. 停机时间
2. 回退方案
```

## 1.6导出数据库数据

```mysql
/etc/my.cnf
#导出数据的限制
secure-file-priv=


select concat ("alter table ",table_schema, " ", table_name," discard tablespace;") from information_schema.tables where table_schema='ocp' into outfile '/tmp/discard.sql';

select * from user into outfile '/tmp/user.csv';
```



# 2. 备份类型

## 2.1 热备



```undefined
在数据库正常业务时,备份数据,并且能够一致性恢复（只能是innodb）
对业务影响非常小
```

## 2.2 温备



```undefined
锁表备份,只能查询不能修改（myisam）
影响到写入操作
```

## 2.3 冷备



```undefined
关闭数据库业务,数据库没有任何变更的情况下,进行备份数据.
业务停止
```

# 3. 备份方式及工具介绍

## 3.1 逻辑备份工具



```undefined
基于SQL语句进行备份
mysqldump       *****
mysqlbinlog     *****
```

## 3.2 物理备份工具



```undefined
基于磁盘数据文件备份
xtrabackup(XBK) ：percona 第三方   *****
MySQL Enterprise Backup（MEB）
```

# 4.  逻辑备份和物理备份的比较

## 4.1 mysqldump (MDP)



```undefined
优点：
1.不需要下载安装
2.备份出来的是SQL，文本格式，可读性高,便于备份处理
3.压缩比较高，节省备份的磁盘空间

缺点：
4.依赖于数据库引擎，需要从磁盘把数据读出
然后转换成SQL进行转储，比较耗费资源，数据量大的话效率较低
建议：
100G以内的数据量级，可以使用mysqldump
超过TB以上，我们也可能选择的是mysqldump，配合分布式的系统
1EB  =1024 PB =1000000 TB
```

## 4.2 xtrabackup(XBK)



```undefined
优点：
1.类似于直接cp数据文件，不需要管逻辑结构，相对来说性能较高
缺点：
2.可读性差
3.压缩比低，需要更多磁盘空间
建议：
>100G<TB
```

# 5.备份策略



```undefined
备份方式：
全备:全库备份，备份所有数据
增量:备份变化的数据
逻辑备份=mysqldump+mysqlbinlog
物理备份=xtrabackup_full+xtrabackup_incr+binlog或者xtrabackup_full+binlog
备份周期:
根据数据量设计备份周期
比如：周日全备，周1-周6增量
```

# 6.备份工具使用-mysqldump

## 6.1 mysqldump (逻辑备份的客户端工具)

### 6.1.1 客户端通用参数



```undefined
-u  -p   -S   -h  -P    
本地备份:
mysqldump -uroot -p  -S /tmp/mysql.sock
远程备份:
mysqldump -uroot -p  -h 10.0.0.51 -P3306
```

### 6.1.2 备份专用基本参数

#### -A   全备参数



```swift
例子1:
[root@db01 ~]# mkdir -p /data/backup
mysqldump -uroot -p1 -A > /backup/full.sql
# 补充:
# 1.常规备份是要加 --set-gtid-purged=OFF,解决备份时的警告
# [root@db01 ~]# mysqldump -uroot -p123 -A  --set-gtid-purged=OFF  >/backup/full.sql
# 2.构建主从时,做的备份,不需要加这个参数
# [root@db01 ~]# mysqldump -uroot -p123 -A    --set-gtid-purged=ON >/backup/full.sql
```

#### -B db1  db2  db3  备份多个单库



```kotlin
说明：生产中需要备份，生产相关的库和MySQL库
例子2 :
 mysqldump -uroot -p1 -B ocp cuoni school  > /backup/db.sql 
```

#### 备份单个或多个表



```bash
例子3 world数据库下的city,country表
mysqldump -uroot -p1 world city country >/backup/tab.sql
以上备份恢复时:必须库事先存在,并且ues才能source恢复
```

### 6.1.3 高级参数应用

#### 特殊参数1使用（必须要加）



```csharp
-R            备份存储过程及函数
--triggers  备份触发器
-E             备份事件

例子4:
[root@db01 backup]# mysqldump -uroot -p -A -R -E --triggers >/data/backup/full.sql
(5) 特殊参数2使用
```

#### -F  在备份开始时,刷新一个新binlog日志



```jsx
例子5:
mysqldump -uroot -p  -A  -R --triggers -F >/bak/full.sql
```

#### --master-data=2



```kotlin
（1）以注释的形式,保存备份开始时间点的binlog的状态信息
（2）自动开启锁表功能

mysqldump -uroot -p  -A  -R --triggers --master-data=2   >/back/world.sql
[root@db01 ~]# grep 'CHANGE' /backup/world.sql 
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000035', MASTER_LOG_POS=194;

功能：
（1）在备份时，会自动记录，二进制日志文件名和位置号
0 默认值
1  以change master to命令形式，可以用作主从复制
2  以注释的形式记录，备份时刻的文件名+postion号
（2） 自动锁表
（3）如果配合--single-transaction，只对非InnoDB表进行锁表备份，InnoDB表进行“热“”备，实际上是实现快照备份。
```

#### --single-transaction



```kotlin
innodb 存储引擎开启热备(快照备份)功能       
master-data可以自动加锁
（1）在不加--single-transaction ，启动所有表的温备份，所有表都锁定
（1）加上--single-transaction ,对innodb进行一致性快照备份，不锁表,对非innodb表可以实现自动锁表功能
例子6: 备份必加参数
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
```

#### --set-gtid-purged=auto



```kotlin
默认是auto
主从复制,忽略此参数
普通备份，可以OFF

使用场景:
1. --set-gtid-purged=OFF,可以使用在日常备份参数中.
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
2. auto , on:在构建主从复制环境时需要的参数配置
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=ON >/data/backup/full.sql
```

#### --max-allowed-packet=#



```csharp
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF --max-allowed-packet=256M >/data/backup/full.sql

 --max-allowed-packet=# 
The maximum packet length to send to or receive from server.
```



#### 6.2 小练习：

6.2.1. 实现所有表的单独备份



```csharp
提示：
information_schema.tables
mysqldump -uroot -p123 world city >/backup/world_city.sql

select concat("mysqldump -uroot -p123 ",table_schema," ",table_name," --master-data=2 --single-transaction --set-gtid-purged=0  -R -E --triggers>/backup/",table_schema,"_",table_name,".sql") from information_schema.tables where table_schema not in ('sys','information_schema','performance_schema');
```

#### 6.2.2.模拟故障案例并恢复



```csharp
（1）每天全备
（2）binlog日志是完整
（3）模拟白天的数据变化
（4）模拟下午两点误删除数据库

需求： 利用全备+binlog回复数据库误删除之前。
故障模拟及恢复：
1. 模拟周一23:00的全备
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
2. 模拟白天的数据变化
Master [(none)]>create database day1 charset utf8;
Master [(none)]>use day1
Master [day1]>create table t1(id int);
Master [day1]>insert into t1 values(1),(2),(3);
Master [day1]>commit;
Master [world]>update city set countrycode='CHN';
Master [world]>commit;
模拟磁盘损坏：
[root@db01 data]# \rm -rf /data/mysql/data/*
3. 恢复故障
[root@db01 data]# pkill mysqld
[root@db01 data]# \rm -rf /data/mysql/data/*
4. 恢复思路
1.检查备份可用性
2.从备份中获取二进制日志位置
3.根据日志位置截取需要的二进制日志
4.初始化数据库,并启动
5.恢复全备
6.恢复二进制日志
```

## 6.3. 压缩备份并添加时间戳



```jsx
例子：
mysqldump -uroot -p123 -A  -R  --triggers --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz
mysqldump -uroot -p123 -A  -R  --triggers --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F-%T).sql.gz

mysqldump备份的恢复方式（在生产中恢复要谨慎，恢复会删除重复的表）
set sql_log_bin=0;
source /backup/full_2018-06-28.sql

注意：
1、mysqldump在备份和恢复时都需要mysql实例启动为前提。
2、一般数据量级100G以内，大约15-45分钟可以恢复，数据量级很大很大的时候（PB、EB）
3、mysqldump是覆盖形式恢复的方法。

一般我们认为，在同数据量级，物理备份要比逻辑备份速度快.
逻辑备份的优势:
1、可读性强
2、压缩比很高
```

# 7、企业故障恢复案例

## 7.1 背景环境：



```css
正在运行的网站系统，mysql-5.7.20 数据库，数据量50G，日业务增量1-5M。
```

## 7.2 备份策略：



```css
每天23:00点，计划任务调用mysqldump执行全备脚本
```

## 7.3 故障时间点：



```undefined
年底故障演练:模拟周三上午10点误删除数据库，并进行恢复.
```

## 7.4 思路：



```css
1、停业务，挂维护页面，避免数据的二次伤害
2、找一个临时库，恢复周三23：00全备
3、截取周二23：00  --- 周二10点误删除之间的binlog，恢复到临时库
4、测试可用性和完整性
5、 
    5.1 方法一：直接使用临时库顶替原生产库，前端应用割接到新库
    5.2 方法二：将误删除的表导出，导入到原生产库
6、开启业务
处理结果：经过20分钟的处理，最终业务恢复正常
```

## 7.5 故障模拟演练

### 7.5.1 准备数据



```csharp
create database backup;
use backup
create table t1 (id int);
insert into t1 values(1),(2),(3);
commit;
rm -rf /backup/*
```

### 7.5.2 周二 23：00全备



```tsx
mysqldump -uroot -p1 -A  -R  --triggers --set-gtid-purged=OFF --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz
```

### 7.5.3 模拟周二 23：00到周三 10点之间数据变化



```csharp
use backup
insert into t1 values(11),(22),(33);
commit;
create table t2 (id int);
insert into t2 values(11),(22),(33);
```

### 7.5.4 模拟故障,删除表(只是模拟，不代表生产操作)



```rust
drop database backup;
```

## 7.6 恢复过程

### 7.6.1 准备临时数据库（多实例3307）



```undefined
systemctl start mysqld3307
```

### 7.6.2 准备备份



```ruby
（1）准备全备：
cd /backup
gunzip full_2018-10-17.sql.gz 
（2）截取二进制日志
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000003', MASTER_LOG_POS=793;

show binlog events in 'mysql-bin.000003';
793
1559

mysqlbinlog  --skip-gtids --start-position=793 --stop-position=1559   /data/binlog/mysql-bin.000003>/backup/bin.sql
```

### 7.6.3 恢复备份到临时库



```bash
mysql -S /data/3307/mysql.sock
set sql_log_bin=0;
source /backup/full_2020-11-26.sql
source /backup/bin.sql
set sql_log_bin=1;
```

### 7.6.4 将故障表导出并恢复到生产



```bash
mysqldump   -S /data/3307/mysql.sock -B backup >/backup/t1.sql
mysql -uroot -p1 
set sql_log_bin=0;
source /backup/t1.sql;
set sql_log_bin=1;
```

# 8. 课下作业：



```undefined
练习：
1、创建一个数据库 oldboy
2、在oldboy下创建一张表t1
3、插入5行任意数据
4、全备
5、插入两行数据，任意修改3行数据，删除1行数据
6、删除所有数据
7、再t1中又插入5行新数据，修改3行数据
需求，跳过第六步恢复表数据
写备份脚本和策略
```

# 9. 备份时优化参数:



```tsx
(1) max_allowed_packet   控制的是备份时传输数据包的大小.

mysqldump -uroot -p123 -A  -R  --triggers --set-gtid-purged=OFF --master-data=2 max_allowed_packet=128M  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz

(2) 增加key_buffer_size    (临时表有关)
(3) 分库分表并发备份       (作业)
(4) 架构分离,分别备份      (架构拆分,分布式备份)
(5) --set-gtid-purged=AUTO/ON 在构建主从时,使用AUTO/ON
(6) --set-gtid-purged=OFF 仅是做普通的本机备份恢复时,可以添加

```

# 10. MySQL物理备份工具-xtrabackup(XBK、Xbackup)

## 10.1安装

### 10.1.1 安装依赖包：



```cpp
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum -y install perl perl-devel libaio libaio-devel perl-Time-HiRes perl-DBD-MySQL libev
```

### 10.1.2 下载软件并安装



```ruby
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.12/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.12-1.el7.x86_64.rpm

https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.4/binary/redhat/6/x86_64/percona-xtrabackup-24-2.4.4-1.el6.x86_64.rpm

yum -y install percona-xtrabackup-24-2.4.4-1.el7.x86_64.rpm
```

## 10.2、备份命令介绍:



```undefined
xtrabackup
innobackupex    ******
```

## 10.3 备份方式——物理备份



```ruby
（1）对于非Innodb表（比如 myisam）时，锁表cp所有非innoDB表数据文件，属于一种温备份。
（2）对于Innodb的表（支持事务的），立即触发checkpoint，立即触发CKPT,copy所有InnoDB表相关的文件(ibdata1,ibd,frm)，并且将备份过程中产生,新的数据变化的部分redo一起备份走，属于热备方式。
（3）在恢复时,xbk会调用InnoDB引擎的CSR过程,将数据和redo的LSN追平,然后进行一致性恢复.
```

## 面试题： xbk 在innodb表备份恢复的流程



```ruby
  0、xbk备份执行的瞬间,立即触发checkpoint,已提交的数据脏页,从内存刷写到磁盘,并记录此时的LSN号
  1、备份时，拷贝磁盘数据页，并且记录备份过程中产生的redo和undo一起拷贝走,也就是checkpoint LSN之后的日志
  2、在恢复之前，模拟Innodb“自动故障恢复”的过程，将redo（前滚）与undo（回滚）进行应用
  3、恢复过程是cp 备份到原来数据目录下

1.备份的过程
(1)非InnoDB表,进行短暂的锁表,然后Copy数据文件
(2) 对于InnoDB表,立即出发checkpoint,会立即记录一个LSN, COPY数据文件.
(3)将备份过程中产生的redo进行截取和保存,并记录此时最新的LSN
2.恢复过程
模拟了CSR的全过程,在恢复之。前,将数据的LSN号和redoLSN号追平
恢复方法就是直接cp回去即可

```

## 10.4、innobackupex使用

### 10.4.1 全备



```csharp
[root@db01 backup]# innobackupex --host=127.0.0.1  --user=root --password=1  /backup/full

```

### 自主定制备份路径名



```csharp
[root@db01 backup]# innobackupex --host=127.0.0.1  --user=root --password=1 --no-timestamp /backup/full
```

### 备份集中多出来的文件：



```ruby
-rw-r----- 1 root root       24 Jun 29 09:59 xtrabackup_binlog_info
-rw-r----- 1 root root      119 Jun 29 09:59 xtrabackup_checkpoints
-rw-r----- 1 root root      489 Jun 29 09:59 xtrabackup_info
-rw-r----- 1 root root     2560 Jun 29 09:59 xtrabackup_logfile

xtrabackup_binlog_info ：（备份时刻的binlog位置）
[root@db01 full]# cat xtrabackup_binlog_info 
mysql-bin.000003    536749
79de40d3-5ff3-11e9-804a-000c2928f5dd:1-7
记录的是备份时刻，binlog的文件名字和当时的结束的position，可以用来作为截取binlog时的起点。

xtrabackup_checkpoints ：
backup_type = full-backuped
from_lsn = 0            上次所到达的LSN号(对于全备就是从0开始,对于增量是上次备份结束的位置)
to_lsn = 160683027      备份开始时间(ckpt)点数据页的LSN    
last_lsn = 160683036    备份结束后，redo日志最终的LSN
compact = 0
recover_binlog_info = 0
（1）备份时刻，立即将已经commit过的，内存中的数据页刷新到磁盘(CKPT).开始备份数据，数据文件的LSN会停留在to_lsn位置。
（2）备份时刻有可能会有其他的数据写入，已备走的数据文件就不会再发生变化了。
（3）在备份过程中，备份软件会一直监控着redo的undo，如果一旦有变化会将日志也一并备走，并记录LSN到last_lsn。
从to_lsn  ----》last_lsn 就是，备份过程中产生的数据变化.
```

### 10.4.2 全备的恢复

#### 准备备份（Prepared）



```ruby
将redo进行重做，已提交的写到数据文件，未提交的使用undo回滚掉。模拟了CSR的过程
[root@db01 ~]# innobackupex --apply-log  /backup/full
```

#### 恢复备份



```undefined
前提：
1、被恢复的目录是空
2、被恢复的数据库的实例是关闭
systemctl stop mysqld
```

创建新目录



```csharp
[root@db01 backup]# mkdir /data/mysql1
```

#### 数据授权



```kotlin
chown -R mysql.mysql /data/mysql1
```

#### 恢复备份



```ruby
[root@db01 full]# cp -a /backup/full/* /data/mysql1/
```

#### 启动数据库



```kotlin
vim /etc/my.cnf
datadir=/data/mysql1
[root@db01 mysql1]# chown -R mysql.mysql /data/mysql1
systemctl start mysqld
```

### 10.4.3 innobackupex 增量备份(incremental)



```undefined
（1）增量备份的方式，是基于上一次备份进行增量。
（2）增量备份无法单独恢复。必须基于全备进行恢复。
（3）所有增量必须要按顺序合并到全备中。
```

#### 增量备份命令



```bash
（1）删掉原来备份
 rm -rf /backup/*
 
（2）全备（周日）
[root@db01 backup]# innobackupex --host=127.0.0.1  --user=root --password=1 --no-timestamp /backup/full
（3）模拟周一数据变化
db01 [(none)]>create database inc1 charset utf8mb4;
db01 [(none)]>use inc1
mysql>create table t1 (id int);
mysql>insert into t1 values(1),(2),(3);
mysql>commit;

（4）第一次增量备份（周一）
innobackupex --host=127.0.0.1  --user=root --password=1 --no-timestamp --incremental  --incremental-basedir=/backup/full /backup/inc1

--inccremental	增量备份开关
--inccremental-basedir=/backup/full   基于那个备份进行增量
/backup/inc1	增量备份位置
    
（5）检查增量备份
[root@db01 inc1 ]$ cat /backup/full/xtrabackup_checkpoints
backup_type = full-backuped
from_lsn = 0
to_lsn = 2842887
last_lsn = 2842896
compact = 0
recover_binlog_info = 0
[root@db01 inc1 ]$ cat /backup/inc1/xtrabackup_checkpoints
backup_type = incremental
from_lsn = 2842887
to_lsn = 2848802
last_lsn = 2848811
compact = 0
recover_binlog_info = 0

 上一次备份last_lsn = 2842896 减去 9 等于 本次备份from_lsn = 2842887
    
（6）模拟周二数据
mysql>create database inc2 charset utf8mb4;
mysql>create table t2 (id int);
mysql>insert into t2 values(1),(2),(3);
mysql>commit;

（7）周二增量
 innobackupex --host=127.0.0.1  --user=root --password=1 --no-timestamp --incremental  --incremental-basedir=/backup/inc1 /backup/inc2
    
（8）检查增量备份
[root@db01 /backup ]$ cat /backup/inc1/xtrabackup_checkpoints
backup_type = incremental
from_lsn = 2842887
to_lsn = 2848802
last_lsn = 2848811
compact = 0
recover_binlog_info = 0
[root@db01 /backup ]$ cat /backup/inc2/xtrabackup_checkpoints
backup_type = incremental
from_lsn = 2848802
to_lsn = 2854690
last_lsn = 2854699
compact = 0
recover_binlog_info = 0

上一次备份last_lsn = 2848811 减去 9 等于 本次备份 from_lsn = 2848802

（9）模拟周三数据变化
mysql>create database inc3 charset utf8mb4;
mysql>create table t3 (id int);
mysql>insert into t3 values(1),(2),(3);
mysql>commit;

(10)模拟上午10点数据库崩溃
pkill mysqld
\rm -rf /data/mysql/data/*
```

#### 恢复到周三误drop之前的数据状态



```undefined
恢复思路：
1.停业务,挂维护页
2.查找可用备份并处理备份:full+inc1+inc2
3. binlog: inc2 到故障时间点的binlog
4.恢复全备+增量+binlog
5.验证数据
6.起业务,撤维护页
```

#### 恢复过程



```bash
恢复前的准备
(1) 整理full
innobackupex --apply-log --redo-only /backup/full

--redo-only	当作为增量备份基础的时候加上，除了最后一次增量备份

(2)合并inc1到full,并整理备份
innobackupex --apply-log --redo-only --incremental-dir=/backup/inc1  /backup/full 

[root@db01 ~ ]$ cat /backup/full/xtrabackup_checkpoints
backup_type = log-applied
from_lsn = 0
to_lsn = 2848802
last_lsn = 2848811
compact = 0
recover_binlog_info = 0
[root@db01 ~ ]$ cat /backup/inc1/xtrabackup_checkpoints
backup_type = incremental
from_lsn = 2842887
to_lsn = 2848802
last_lsn = 2848811
compact = 0
recover_binlog_info = 0

合并之后，full备份last_lsn = 2848811 等于增量备份 last_lsn = 2848811

(3)合并inc2到full,并整理备份
innobackupex --apply-log  --incremental-dir=/backup/inc2 /backup/full

[root@db01 ~ ]$ cat /backup/full/xtrabackup_checkpoints
backup_type = full-prepared
from_lsn = 0
to_lsn = 2854690
last_lsn = 2854699
compact = 0
recover_binlog_info = 0
[root@db01 ~ ]$ cat /backup/inc2/xtrabackup_checkpoints                              
backup_type = incremental
from_lsn = 2848802
to_lsn = 2854690
last_lsn = 2854699
compact = 0
recover_binlog_info = 0

合并之后，full备份last_lsn = 2854699 等于增量备份 last_lsn = 2854699

(4) 最后一次整理full
innobackupex --apply-log /backup/full

截取二进制日志
起点：[root@db01 inc2 ]$ cat xtrabackup_binlog_info  
mysql-bin.000004	1997	2fa25f12-271a-11eb-9b2f-000c2943bd92:1-20
终点：[root@db01 inc2 ]$ mysqlbinlog /data/binlog/mysql-bin.000004 |grep 'SET' 

SET @@SESSION.GTID_NEXT= '2fa25f12-271a-11eb-9b2f-000c2943bd92:23'/*!*/;

截取日志：[root@db01 inc2 ]$ mysqlbinlog --skip-gtids --include-gtids='2fa25f12-271a-11eb-9b2f-000c2943bd92:21-23' /data/binlog/mysql-bin.000004 >/tmp/binlog.sql


进行恢复
[root@db01 backup]# mkdir /data/mysql/data -p
[root@db01 full]# cp -a * /data/mysql/data
[root@db01 backup]# chown -R mysql.mysql  /data/*
[root@db01 backup]# service mysqld start
Master [(none)]>set sql_log_bin=0;
Master [(none)]>source /data/backup/binlog.sql

验证数据
mysql> select *from inc1.t1;
mysql> select *from inc2.t1;
mysql> select *from inc3.t1;
```

# 11.迁移（5.6.44-->5.7.26）

### 11.1搭建5.6的测试环境

(1)创建必须的目录

```bash
[root@cuoni ~]# mkdir /data/mysql/data -p
[root@cuoni ~]# mkdir /application/ -p
[root@cuoni ~]# mkdir /data/binlog -p
```

上传软件至/application 下
(2)建用户,改权限

```bash
[root@cuoni ~]# useradd mysql
[root@cuoni ~]# chown -R mysql. /data/application/
```

（3）修改环境变量

```bash
vim /etc/profile 

export PATH=/application/mysql/bin:$PATH;

source /etc/profile 
```

（4）数据初始化

先卸载自带的mairadb

```bash
/application/mysql/scripts/mysql_install_db --user=mysql --basedir=/application/mysql --datadir=/data/mysql/data

```

(5)准备配置文件和启动脚本

```bash
vim /etc/my.cnf

[mysqld]
user=mysql
basedir=/application/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=6
port=3306
autocommit=0
log_error=/tmp/mysql3306.log
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
#慢日志开关:
slow_query_log=1
#文件位置及名字
slow_query_log_file=/data/mysql/slow.log
#设定慢查询时间:
long_query_time=0.1
#没走索引的语句也记录:
log_queries_not_using_indexes
#导出数据的限制
secure-file-priv=

[mysql]
socket=/tmp/mysql.sock


cp /application/mysql/support-files/mysql.server /etc/init.d/mysqld

```

(6)启动数据库

```bash
/etc/init.d/mysqld start

mysql

mysqladmin -uroot -p password 1

```

### 11.2迁移5.6数据到5.7

（1）备份5.6数据

```bash
mysqldump -uroot -p123 -A - -master-data=2 --single-t ransaction -R -E --triggers > /tmp/full.sql 

```

(2)准备5.7数据库

传输5.6备份数据到5.7服务器

```bash
scp /tmp/full root@10.0.0.51:/tmp
```

启动数据库并登陆

```bash
mysql -uroot -1
```

导入数据并更新

```bash
mysql>source /tmp/full.sql 

[root@ db01 /] # mysql_upgrade -uroot -p1 -S /data/3308/mysq1.sock

```

(3)binlog持续追加

(4)停业务，恢复剩余binlog

(5)业务割接

