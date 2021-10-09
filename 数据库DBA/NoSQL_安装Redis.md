# 安装Redis

## 目录规划

```bash
### redis.下载目录
/data/soft/

### redis安装目录。
/opt/redis_cluster/redis_{PORT}/{conf,1ogs,pid}

### redis数据目录
/data/redis_cluster/redis_{PORT}/redis_{P0RT}.rdb

### redis运维脚本
/root/scripts/redis_shell.sh
```


## 安装命令

```bash
###编辑hosts文件。
[root@db01^ ]#vim /etc/hosts

10.0.0.51 db01
10.0.0.52 db02
10.0.0.53 db03

mkdir -p /data/soft

mkdir -p /data/redis_cluster/redis_6379

mkdir -p /opt/redis_cluster/redis_6379/{conf,pid,logs}

cd /data/soft/

wget https://download.redis.io/releases/redis-6.0.9.tar.gz

tar -zxf redis-6.0.9.tar.gz -C /opt/redis_cluster/

ln -s /opt/redis_cluster/redis-6.0.9/ /opt/redis_cluster/redis

cd /opt/redis_cluster/redis

make && make install

cd /opt/redis_cluster/redis_6379 

vim /opt/redis_cluster/redis_6379/conf/redis_6379.conf  

###以守护进程模式启动
daemonize yes 
###绑定的主机地址
bind 10.0.0.51
###监听端口
port 6379 
###pid文件和1og文件的保存地址
pidfile /opt/redis_cluster/redis_6379/pid/redis_6379.pid
logfile /opt/redis_cluster/redis_6379/logs/redis_6379.log
###设置数据库的数量，默认数据库为0
databases 16
###指定本地持久化文件的文件名，默认是dump.rdb
dbfilename redis_6379.rdb
###本地数据库的目录
dir /data/redis_cluster/redis_6379 

```

## 启动关闭Redis

redis-cli		客户端
redis-server	服务端

```bash
#启动Redis服务

redis-server /opt/redis_cluster/redis_6379/conf/redis_6379.conf 

#关闭Redis服务

10.0.0.51:6379> shutdown

redis-cli shutdown
```

## systemd启动配置



```csharp
groupadd -g 1000 redis
useradd -u 1000 -g 1000 -M -s /sbin/nologin
chown -R redis:redis /data/redis*
chown -R redis:redis /opt/redis*
    
cat >/usr/lib/systemd/system/redis.service<<EOF
[Unit]
Description=Redis persistent key-value database
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/redis /opt/redis_6379/conf/redis_6379.conf --supervised systemd
ExecStop=/usr/local/bin/redis-cli -h $(ifconfig eth0|awk 'NR==2{print $2}') -p 6379 shutdown
Type=notify
User=redis
Group=redis
RuntimeDirectory=redis
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload 
systemctl start redis
```



# 常用命令

## 全局命令

```
Redis有5种数据结构,他们是键值对中的值,对于键来说有一些通用的命令.
1.查看所有命键。
Keys *
#十分危险的命令,线上禁止使用
2.查看键的总数。
Dbsize 
# dbsize 命令在计算键总数时不会遍历所有键,而是直接获取Redis内置的键总数变量. 
3.检查键是否存在。
Exists key
#如果键存在则返回1,不存在则返回0
4.删除键
De1 key [key ..]
#通用命令,无论值是什么数据结构类型，del命令都可以将其删除
5.键过期。
Expire key seconds
ttl #查看过期时间
-1	永不过期
-2	没有这个key
数字	 这个key存在，并且在N秒后过期
注意：重复设置过期时间会造成永不过期
PERSIST k 取消过期时间
6.查看类型
TYPE key
```

## String类型对应操作

### set -- 设置一个键对应的值(键不存在会被创建)

```
用法：
set key value [expiration EX seconds|PX milliseconds] [NX|XX]
EX 是指暂存时间(秒)
例如：
127.0.0.1:6379> set k1 v1
OK
```

### get -- 得到一个键对应的值

```
用法：
get key
例如：
127.0.0.1:6379> get k1
v1
```

### append -- 为一个键对应的值进行拼接

```
用法：
append key value
例子：
127.0.0.1:6379> append animal ' Dog'
(integer) 7
127.0.0.1:6379> get animal
"Cat Dog"
127.0.0.1:6379>
```

### mset -- 设置多个键的值(键不存在会被创建)

```
用法：
mset key value [key value ...]
例子：
127.0.0.1:6379> mset k1 v1 k2 v2 k3 v3 k4 v4
OK
```

### mget -- 获取键对应的值

```
用法：
mget key [key ...]
例子：
127.0.0.1:6379> mget k1 k2 k3 k4
1) "v1"
2) "v2"
3) "v3"
4) "v4"
```

### del -- 删除一个键值对

```
用法：
del key [key ...]
例子：
127.0.0.1:6379> del k1
(integer) 1
127.0.0.1:6379>
```

### incr、decr   自增 、自减

```
用法：
incr key
incrby 自增多个
decr key
例子:
127.0.0.1:6379> set k1 8
OK
127.0.0.1:6379> incr k1  #加一个
(integer) 9
127.0.0.1:6379> incrby k1 100 #加100个

127.0.0.1:6379> decr k1
(integer) 8
```

### 键过期

```
EXPIRE key seconds
TTL #查看过期时间
-1	永不过期
-2	没有这个key
数字	还有多长时间过期
注意：重复设置过期时间会造成永不过期
PERSIST k 取消过期时间
```



## 列表对应操作

### lpush -- 从左插入一个数据(从队列头部插入一个数据)

```
用法：
lpush key value [value ...]
例子：
127.0.0.1:6379> lpush q1 'Jhon' 'Cat' 'Amy'
(integer) 3
```

### rpush -- 从右插入一个数据(从队列尾部插入一个数据)

```
用法：
rpush key value [value ...]
例子：
127.0.0.1:6379> rpush q1 'Bob'
(integer) 4
```

### llen -- 查看队列长度

```
用法：
llen key
例子：
127.0.0.1:6379> llen q1
(integer) 4
127.0.0.1:6379>
```

### lrange -- 查看队列内容

```
用法：
lrange key start stop
例子：
127.0.0.1:6379> lrange q1 0 -1
1) "Amy"
2) "Cat"
3) "Jhon"
4) "Bob"
```

与python类似-1代表倒数第一位，也就是最后一个

### lpushx -- 向存在的列表中左插入一个值(插入不存在的列表时不做任何操作)

```
用法：
lpushx key value
例子：
127.0.0.1:6379> lpushx q1 'zhang'
(integer) 5
127.0.0.1:6379> lrange q1 0 -1
1) "zhang"
2) "Amy"
3) "Cat"
4) "Jhon"
5) "Bob"
127.0.0.1:6379> lpushx q2 'zhang'
(integer) 0
127.0.0.1:6379>
```

### rpushx -- 向存在的列表中右插入一个值(插入不存在的列表时不做任何操作)

```undefined
向存在的列表中右插入一个值
```

### ltrim -- 左截取一定长度的列表(剩下的删除)

```
用法：
ltrim key start stop
例子：
127.0.0.1:6379> ltrim  q1 0 2
OK
127.0.0.1:6379> lrange q1 0 -1
1) "zhang"
2) "Amy"
3) "Cat"
127.0.0.1:6379>
```

### lpop -- 左删除列表中的一个值

```
用法：
 lpop key
例子：
127.0.0.1:6379> lpop q1
"zhang"
127.0.0.1:6379> lrange q1 0 -1
1) "Amy"
2) "Cat"
127.0.0.1:6379>
```

### rpop -- 右删除列表中的一个值

```undefined
把右边的弹走
```

------

## 集合类型相关操作

### sadd -- 向集合中加入元素

```
用法：
sadd key member [member ...]
例子：
SADD set1 1 2 3
SADD set2 1 3 5 7 
```

集合类型中，不允许出现重复内容

### smembers -- 查看集合中的元素

```
用法：
 smembers key
例子：
SMEMBERS set1
SMEMBERS set2
```

### srem -- 从集合中移除元素

```
用法：
srem key member [member ...]
例子：
127.0.0.1:6379> srem zoo Cat
(integer) 1
127.0.0.1:6379>
```

### sismember -- 查看某个值是否在某个集合中

```
用法：
sismember key member
例子：
127.0.0.1:6379> sismember zoo Dog
(integer) 1
127.0.0.1:6379> sismember zoo Cat
(integer) 0
127.0.0.1:6379>
```

1 代表存在，0 代表不存在

### sdiff -- 比较集合间的不同(查看集合的差集)

```
用法：
sdiff key [key ...]
例子：
127.0.0.1:6379> SDIFF set1 set2
1) "2"
  
127.0.0.1:6379> SDIFF set2 set1
1) "5"
2) "7"
```

先查看zoo 、zoo1里有什么，再比较一下不同

### sinter -- 计算集合的交集

```
用法：
sinter key [key ...]
例子：
127.0.0.1:6379> SINTER set1 set2
1) "1"
2) "3"
```

### sunion -- 计算集合的并集

```
用法：
sunion key [key ...]
例子：
127.0.0.1:6379> SUNION set1 set2
1) "1"
2) "2"
3) "3"
4) "5"
5) "7"
```

------

## Hash相关操作

## mysql数据如何缓存到redis

```
mysql存储格式：
user
id name   job  age
1  bobo   IT   28
2  json   py   25
3  hao    bug  26
  
hash类型存储格式：
key    field value field   value        
user:1   name  bobo  job     IT     age 28
user:2   name  json  job     py     age 25
user:3   name  hao   job     bug    age 26
```

### hset/hget --  设置/获取散列值

```
select name from user where id =1 ;
用法：
hset key field value
hget key field
例子：
HMSET user:1 name bobo job IT age 28
HMSET user:2 name json job py age 29
HMSET user:3 name hao job bug age 19 
```

这里（news:1）是一个整体，在这里作为key

### hmset/hmget -- 设置/获取多对散列值

```
用法：
hmset key field value [field value ...]
hmget key field [field ...]
例子：
HMGET user:1 name  
HMGET user:1 name job age

查看Hash里所有的值
select * from user where id =1 ;

HGETALL user:1
```

### hsetnx -- 如果散列值已经存在，则不设置

```
用法：
hsetnx key field value
例子：
127.0.0.1:6379> hget news:2 is_valid
"1"
127.0.0.1:6379> hsetnx news:2 is_valid 2
(integer) 0
127.0.0.1:6379> hget news:2 is_valid
"1"
127.0.0.1:6379>
```

### hkeys/hvals -- 返回所有Keys/Values

```
用法：
hkeys key
hvals key
例子：
127.0.0.1:6379> hkeys news:1
1) "title"
2) "content"
127.0.0.1:6379>
127.0.0.1:6379> hvals news:2
1) "Title2"
2) "Content2"
3) "1"
127.0.0.1:6379>
```

### hlen -- 返回散列包含域（field）的数量

```
用法：
hlen key
例子：
127.0.0.1:6379> hlen news:2
(integer) 3
127.0.0.1:6379>
```

### hdel -- 删除散列指定的域（field）

```
用法：
hdel key field [field ...]
例子：
127.0.0.1:6379> hdel news:2 is_valid
(integer) 1
127.0.0.1:6379>
```

### hexists --判断散列是否存在

```
用法：
hexists key field
例子：
127.0.0.1:6379> hexists news:2 is_valid
(integer) 0
```

# 数据持久化

## RDB和AOF介绍

```undefined
RDB：类似于快照的形式，当前内存里的状态持久化到硬盘里
优点：压缩格式/恢复速度快
缺点：不是实时的，可能会丢失数据,操作比较重
    
AOF：类似于mysql的binlog，可以设置为每秒/每次操作以追加的形式持久化
优点：安全，最多损失1秒的数据，可读
缺点：文件比较大，恢复速度慢
```

## RDB

RDB持久化是把当前进程数据生成快照保存到硬盘的过程触发RDB持久化过程分为手动出发和自动触发.

### 1.1触发机制

手动触发分为save 和bgsava命令:

#### 1.1.1 bgsave命令

Redis.进程执行fork操作创建子进程,RDB持久化过程由子进程负责完成后自动结束阻塞只发生在fork阶段,-般时间很短运行bgsave命令对应的Redis.日志如下
显然,bgsave命令是针对save阻塞问题做的优化因此Redis内部所有涉及RDB的操作都采用bgsave.的方式,save命令已经被废弃.

### 1.2 自动触发RDB的持久化机制

1.使用save 相关配置,如"save m n".表示m秒内数据集存在n次修改时，自动触发bgeave,
2.如果从节点执行全量复制操作，主节点自动执行bgsave 生成RDB文件并发给从节点.
3.执行debug reload命令重新加载Redis时，也会自动触发save操作.
4.默认情况下执行shutdown命令时,如果没有开启aof持久化功能则自动执行bgsave.

### 1.3流程说明

![image-20201216115743228](D:\BaiduNetdiskDownload\数据库DBA\RDB流程图.png)

1.执行bgsave命令Redis 父进程判断当前是否存在正在执行的子进程,如RDB/AOF子进程,如果存在bgsave命令直接返回.

2.父进程执行fork操作创建子进程fork操作过程中父进程会阻塞通过info stats命令查看lastest. fork. usec 选项,可以获取最近-个fork操作的耗时，单位为微秒.
3.父进程fork完成后,bgsave命令返回" Background saving started"信息并不再阻塞父进程，可以继续响应其他命令.
4.子进程创建RDB文件,根据父进程内存生成临时快照文件，完成后对源文件进行原子替换，执行lastsave命令可以获取最后一次生成RDB的时间，对应Info统计的rdb_ last_ save_time 选项
5.进程发送信号给父进程表示完成，父进程更新统计信息，具体见info Persistence 下的rdb_.*相关选项.

### 1.4 RDB文件的处理

#### 1.4.1 保存

RDB文件保存在dir配置指定的目录下,文件名通过dbfilename配置指定可以通过执行config, set dir{newDir}和config set dbfilename, {newFileName} 运行期动态执行，当下次运行时RDB文件会保存到指定目录.

#### 1.4.2 压缩

Redis默认采用LZF算法对生成的RDB文件做压缩处理压缩处理后的文件远远小于内存大小默认开启，可以通过参数confis, set rdbcompression {yes|no} 动态修改.

#### 1.4.3校验

如果Redis加载损坏的RDB文件时拒绝启动,并打印如下日志

```
#Short read or OMM loading DB .Unrecoverable error, aborting now.
```

这时可以使用redis提供的redis-check-dump工具检测RDB文件并获取对应的错误报告.

### 1.5 RDB的优缺点

#### 1.5.1 优点

1.RDB是一个紧湊压缩的二进制文件,代表Redis在某个时间点上的数据快照非常适用于备份,全量复制等场景.比如每6小时执行bgsave备份，并把RBD文件拷贝到远程机器，用于灾难恢复.
2.Redis加载RDB恢复数据远远快于AOF的方式，

#### 1.5.2 缺点

1.RDB方式数据没办法做到实时持久化秒级持久化因为bgsave每次运行都要执行fork操作创建子进程,属于重量级操作，执行频繁成本过高.
2.RDB文件使用特定二进制格式保存,Redis版本演进过程中有多个格式的RDB版本,存在老版本Redis不兼容新版RDB格式的问题

### 1.6  配置RDB

```kotlin
vim /etc/redis/6379.conf

save 900 1
save 300 10
save 60 10000
dbfilename redis.rdb
dir /data/redis_6379/
```

### 1.7 RDB结论

```bash
1.没有配置save参数时，shutdown不会持久化保存
2.没有配置save参数时，可以手动执行bgsave触发持久化
3.在配置了save参数后，shutdown,kill,pkill都会自动触发bgsave
4.恢复的时候，rdb文件名要和配置文件里写的一样。
5.RDB高版本兼容低版本，低版本不兼容高版本
```

## AOF

AOF(append only file)持久化:以独立日志的方式记录每次写命令,重启时再执行AOF文件中的命令打道回府数据的目的AOF的主要作用是解诀了数据持久化的实时性，目前已经是Redis持久化的主流
方式，

### 2.1 使用AOF

开启AOF功能需要设置配置: appendenly yes默认不开启.AOF文件名通过appendfilename配置设置,默认文件名是appendonly.aof,保存路径通RDB持久化方式一致通过dir配置指定.

### 2.2 AOF的工作流程

![image-20201216125539473](D:\BaiduNetdiskDownload\数据库DBA\AOF工作流程.png)

1.所有写入命令会追加到aof_ buf(缓冲区)中.
2.AOF缓冲区根据对应的策略向硬盘做同步操作
3.随着AOF文件越来越大需要定期对AOF文件进行重写，达到压缩
4.当Redis服务重启时，可以加载AOF文件进行数据恢复

### 2.3命令写入

AOF命令写入的内容直接是文本协议格式,例如set hello world这条命令,在AOF缓冲区会追加文本

```
*3\r\n$3\r\nset\r\n$5\r\nhello\rn$5\r\nworld\r\n 
```

2.3.1关于AOF的两个疑惑:
1) AOF为什么直接采用文本协议格式?可能的理由如下:
	-文本协议具有很好的兼容性
	-开启AOF后，所有写入命令都可以包含追加操作，直接采用协议格式，避免了二次处理开销.
	-文本协议具有可读性，方便直接修改和处理.
2)AOF为什么把命令追加到aof_ buf 中?
Redis.使用单线程响应命令,如果每次写入AOF文件命令都直接追加到硬盘,那么性能完全取决于当前硬盘负载先写入缓冲区aof_buf,中，还有另一个好处,Redis，可以提供多种缓冲区同步硬盘的策略,在性能和安全性方面做出平衡.

### 2.4 文件同步

Redis提供了多种AOF缓冲区同步文件策略，由参数appendfsync控制,不同值的含义如下表:

| 可配置值  | 说明                                                         |
| --------- | ------------------------------------------------------------ |
| alw ays   | 命令写入aof_ buf 后调用系统fsxns操作同步到AOF文件,fsync完成后线程返回. |
| everysec. | 命令写入aof_buf 后调用系统write操作,write完成后线程返回fsync同步文件操作由<br/>专门线程每秒调用一次. |
| no        | 命令写入aof_buf 后调用系统write操作，不对AOF文件做fsync同步,同步硬盘操作由<br/>操作系统负责通常同步周期最长30秒. |

#### 2.4.1系统调用write和fsync说明

1). write操作会触发延迟写(delayed write)机制Linux在内核提供页缓冲区用来提高硬盘IO性能write操作在写入系统缓冲区后直接返回同步硬盘操作依赖于系统调度机制,例如:缓冲区页空间写满或达到特定时间周期同步文件之前,如果此时系统故障宕机，缓冲区内数据将丢失.

2)fsync针对单个文件操作(比如AOF文件)，做强制磁盘同步,fsync将阻塞直到写入硬盘完成后返回,保证了数据持久化.

3)配置为always 时，每次写入都要同步AOF文件,在一般的SATA硬盘上,Redis只能支持大约几百TPS写入，显然每次写入都要同步AOF文件,在一-般的 SATA硬盘上,Redis只能支持大约几百TPS,显然跟Redis.高性能背道而驰,不建议配置.

4)配置为no,由于操作系统每次同步AOF文件的周期不可控，而且会加大每次同步硬盘的数据量，虽然提升了性能,但数据安全性无法保证

5)配置为everysec, 是建议的同步策略，也是默认配置,做到兼顾性能和数据安全性.理论上只有在系统突然宕机的情况下丢失1秒的数据当然严格来说，也有可能会全部丢失

### 2.5重写机制

随着命令不断写入AOF,文件会越来越大，为了解决这个问题,Redi s引入了AOF重写机制压缩文件体积AOF文件重写是把Redis进程内的数据转化为写命令同步到新AOF文件的过程.重写后的AOF文件为什么可以变小?有如下原因: 
1)进程内已经超时的数据不再写入文件.

2)旧的AOF文件含有无效命令,如del key 1,hdel key2, srem keys, set a 11,set a222等，重写使用进程内数据直接生成，这样新的AOF文件只保留最终数据的写入命令.

3)多条写命令可以合并为一个,如:npush list a , input list b, input list c可以转化为:input listabc.为了防止单条命令过大造成客户端緩冲区溢出，对于list,set,hash,zset等类型操作,以64个元素为界拆分为多条.
AOF重写降低了文件占用空间，除此之外，另一个目的是:更小的AOF文件可以更快地被Redis加载

#### 2.5.1 AOF重写过程的手动触发和自动触发

AOF重写过程可以手动触发和自动触发.
手动触发:直接调用bgrewriteaof命令
自动触发:根据auto-aof-rewrite-min-size和auto-aof-rewrte-percentage参数确定自动触发时机.
auto-aof-rewirte-min-size:表示运行AOF重写时文件最小体积默认为64M
auto-aof- rewirte-percentage:代表当前AOF文件空间(aof_ current_ size)和上 - -次重写后 AOF文件空间(aof_ base_ size)的比值.
自动触发时机=aof_ _current_ size > auto-aof- rewirte-min-size, && (aof_ current_ _size -aof_ base_ size) /aof_ _base_ size >= auto-aof-rewrite-percentage
其中aof_current_size 和aof_base_size 可以在info Persistence统计信息中查看.

### AOF配置

```bash
appendonly yes				#是否打开aof日志功能
appendfilename "redis.aof"	
appendfsync always			#每1个命令，都立即同步到aof
appendfsync everysec		#每秒写1次
appendfsync no				#写入工作交给操作系统，由操作系统判断缓神区大小，统一写入到aof
```

### AOF重写机制

```bash
执行的命令   aof记录        redis的数据       
set k1    v1    set k1   k1                 
set k2    v2    set k2   k1 k2          
set k3    v3    set k3   k1 k2 k3       
del k1      del k1       k2 k3
del k2      del k2       k3 
实际有意义的只有一条记录：
set k3
```

```undefined
当aof和rdb同时存在时，重启redis会优先读取aof的内容
```

# redis用户认证

## 1.写入配置文件

```undefined
requirepass 123456
```

## 2.使用密码登陆

第一种：

```bash
[root@db01 ~]# redis-cli 
127.0.0.1:6379> AUTH 123456
OK
127.0.0.1:6379> set k1 v1
OK
  
```

第二种：

```
redis-cli -a 123456 get k1
```

## 3.为什么redis的密码认证这么简单？

```css
1.redis一般都部署在内网环境，默认是比较安全的环境
2.有同学担心密码写在配置文件里，开发不允许登陆到Linux服务器上，但是可以连接到redis,设个密码安全些
```

# Redis主从复制

## 1.快速部署第二台服务器

```bash
rsync -avz 10.0.0.51:/opt/* /opt/*
mkdir /data/redis_6379/ -p
cd /opt/redis 
make install 
sed -i 's#51#52#g' /opt/redis_6379/conf/redis_6379.conf
redis-server /opt/redis_6379/conf/redis_6379.conf
```

## 2.db01插入测试命令

```bash
for i in {1..1000};do redis-cli -h 10.0.0.51 set ${i} ${i};done
```

## 3.配置主从复制

方法1:临时生效

```bash
redis-cli -h 10.0.0.52 slaveof 10.0.0.51 6379 
```

方法2:写进配置文件

```css
slaveof 10.0.0.51 6379
```

## 4.主从复制的流程

1.简单流程：

```undefined
1.从节点发送同步请求到主节点
2.主节点接收到从节点的请求之后,做了如下操作
  - 立即执行bgsave将当前内存里的数据持久化到磁盘上
  - 持久化完成之后,将rdb文件发送给从节点
3.从节点从主节点接收到rdb文件之后,做了如下操作
  - 清空自己的数据
  - 载入从主节点接收的rdb文件到自己的内存里
4.后面的操作就是和主节点实时的了
```

## 5.取消复制

```undefined
    SLAVEOF no one
```

## 6.主从复制注意

```
1.从节点只读不可写
2.从节点不会自动故障转移,它会一直同步主节点
10.0.0.52:6379> set k1 v1
(error) READONLY You can't write against a read only slave.
3.主从复制故障转移需要人工介入
  - 修改代码指向REDIS的IP地址
  - 从节点需要执行SLAVEOF no one
4.从节点会清空自己原有的数据,如果同步的对象写错了,就会导致数据丢失
5.从库和主库后续的同步依靠的是redis的SYNC协议，而不是RDB文件，RDB文件只是第一次建立同步时使用。
6.从库也可以正常的持久化文件
```

## 7.安全的操作

1.执行主从复制之前,现将数据备份一份
2.建议将主从复制写入到配置文件中
3.在业务低峰期做主从复制,
4.拷贝数据时候会占用带宽
5.不能自动完成主从切换，需要人工介入 

# Redis哨兵

![img](https:////upload-images.jianshu.io/upload_images/14248468-c5cf045607671b40.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

## 1.哨兵的作用

```undefined
解决了主从复制故障需要人为干预的问题
提供了自动的高可用解决方案

1.监控(Monitoring) :。
Sentine1会不断地定期检查你的主服务器和从服务器是否运作正常。。
2.提醒(Notification) :
当被监控的某个Redis服务器出现问题时，Sentinel可以通过API向管理员或者其他应用程序发送通知。
3.自动故障迁移(Automatic failover) :
当一个主服务器不能正常工作时，Sentine1 会开始一次自动故障迁移操作，它会将失效主服务器的其中一个从服务器升级为新的主服务器，并让失效主服务器的其他从服务器改为复制新的主服务器;当 客户端试图连接失效的主服务器时，集群也会向客户端返回新主服务器的地址，使得集群可以使用新主服务器代替失效服务器

```

## 2.目录和端口规划

| 角色        | IP        | 端口  |
| ----------- | --------- | ----- |
| Master      | 10.0.0.51 | 6379  |
| Sentinel-01 | 10.0.0.51 | 26379 |
| Master      | 10.0.0.52 | 6379  |
| Sentinel-02 | 10.0.0.52 | 26379 |
| Master      | 10.0.0.53 | 6379  |
| Sentinel-03 | 10.0.0.53 | 26379 |



## 3.部署3台redis单节点

哨兵是基于主从复制，所以需要先部置好主从复制
手工操作步骤如下:。
1.先配置和创建好1台服务器的节点和哨兵+
2.使用rsync传输到另外2台机器。
3.修改另外两台机器的IP地址。

### db01操作：

```bash
pkill redis
cat >/opt/redis_6379/conf/redis_6379.conf <<EOF   
daemonize yes
bind 127.0.0.1 10.0.0.51
port 6379
pidfile "/opt/redis_6379/pid/redis_6379.pid"
logfile "/opt/redis_6379/logs/redis_6379.log"
dbfilename "redis.rdb"
dir "/data/redis_6379"
appendonly yes
appendfilename "redis.aof"
appendfsync everysec
EOF
systemctl start redis
redis-cli
```

### db02和db03的操作：

```ruby
pkill redis 
rm -rf /opt/redis*
rsync -avz 10.0.0.51:/usr/local/bin/redis-*  /usr/local/bin
rsync -avz 10.0.0.51:/usr/lib/systemd/system/redis.service /usr/lib/systemd/system/
mkdir /opt/redis_6379/{conf,logs,pid} -p
mkdir /data/redis_6379 -p
cat >/opt/redis_6379/conf/redis_6379.conf <<EOF   
daemonize yes
bind 127.0.0.1 $(ifconfig eth0|awk 'NR==2{print $2}')
port 6379
pidfile "/opt/redis_6379/pid/redis_6379.pid"
logfile "/opt/redis_6379/logs/redis_6379.log"
dbfilename "redis.rdb"
dir "/data/redis_6379"
appendonly yes
appendfilename "redis.aof"
appendfsync everysec
EOF
useradd redis -M -s /sbin/nologin
chown -R redis:redis /opt/redis*
chown -R redis:redis /data/redis*
systemctl daemon-reload 
systemctl start redis 
redis-cli
```

## 4.配置主从复制

```css
redis-cli -h 10.0.0.52 slaveof 10.0.0.51 6379
redis-cli -h 10.0.0.53 slaveof 10.0.0.51 6379
redis-cli -h 10.0.0.51 info Replication
```

## 5.部署哨兵节点-3台机器都操作

db01:

```kotlin
mkdir -p /data/redis_cluster/redis_26379

mkdir -p /opt/redis_cluster/redis_26379/{conf,pid,logs}

cat >/opt/redis_cluster/redis_26379/conf/redis_26379.conf << EOF
bind $(ifconfig eth0|awk 'NR==2{print $2}')
port 26379
daemonize yes
logfile /opt/redis_cluster/redis_26379/logs/redis_26379.log
dir /data/redis_cluster/redis_26379
sentinel monitor myredis 10.0.0.51 6379 2
sentinel down-after-milliseconds myredis 3000
sentinel parallel-syncs myredis 1
sentinel failover-timeout myredis 18000
EOF

chown -R redis:redis  /data/redis*

chown -R redis:redis  /opt/redis*
```

参数解释：

```bash
sentinel monitor mymaster 10.0.0.51 6379 2
#mymaster 主节点别名 主节点 ip 和端口， 判断主节点失败， 两个 sentinel 节点同意
sentinel down-after-milliseconds mymaster 3000
#选项指定了 Sentinel 认为服务器已经断线所需的毫秒数。
sentinel parallel-syncs mymaster 1
#向新的主节点发起复制操作的从节点个数， 1 轮询发起复制
sentinel failover-timeout mymaster 180000
#故障转移超时时间
```



db02/db03:

```bash
rsync -avz /opt/* db02:/opt/
rsync -avz /opt/* db03:/opt/
```

db02:

```bash
mkdir -p /data/redis_cluster/redis_26379

cd /opt/redis_cluster/redis

make install

sed -i 's#bind 10.0.0.51#bind 10.0.0.52#g' /opt/redis_cluster/redis_26379/conf/redis_26379.conf

sed -i 's#bind 10.0.0.51#bind 10.0.0.52#g' /opt/redis_cluster/redis_6379/conf/redis_6379.conf

vim /opt/redis_cluster/redis_6379/conf/redis_6379.conf
slaveof 10.0.0.51 6379
```

db03:

```bash
mkdir -p /data/redis_cluster/redis_26379

cd /opt/redis_cluster/redis

make install

sed -i 's#bind 10.0.0.51#bind 10.0.0.53#g' /opt/redis_cluster/redis_26379/conf/redis_26379.conf

sed -i 's#bind 10.0.0.51#bind 10.0.0.53#g' /opt/redis_cluster/redis_6379/conf/redis_6379.conf

vim /opt/redis_cluster/redis_6379/conf/redis_6379.conf
slaveof 10.0.0.51 6379
```

## 6.启动Redis

db01/db02/db03:

```bash
redis-server /opt/redis_cluster/redis_6379/conf/redis_6379.conf
```

## 7.启动哨兵

db01/db02/db03:

```bash
redis-sentinel /opt/redis_cluster/redis_26379/conf/redis_26379.conf
```

## 8.验证主节点

```bash
redis-cli -h 10.0.0.51 -p 26379 info sentinel 
redis-cli -h 10.0.0.52 -p 26379 info sentinel
redis-cli -h 10.0.0.53 -p 26379 info sentinel
```



```bash
redis-cli -h 10.0.0.51 -p 26379 Sentinel get-master-addr-by-name myredis
redis-cli -h 10.0.0.52 -p 26379 Sentinel get-master-addr-by-name myredis
redis-cli -h 10.0.0.53 -p 26379 Sentinel get-master-addr-by-name myredis
```

## 9.模拟故障转移

关闭主节点服务上的所有redis进程
观察其他2个节点会不会发生选举
查看配置文件里会不会自动更新
查看新的主节点能不能写入
查看从节点能否正常同步

## 10.模拟故障修复上线

启动单节点
启动哨兵

## 11.来自json的灵魂发问：能够给redis 节点加权 来确定优先备选主节点嘛?

流程说明：
 设置其他节点的权重为0
 手动发起重新选举
 观察所有节点消息是否同步
 观察切换结果是否符合预期

命令解释：

```bash
查询命令:CONFIG GET slave-priority
设置命令:CONFIG SET slave-priority 0
主动切换:sentinel failover myredis
```

操作命令：

```bash
redis-cli -h 10.0.0.52 -p 6379 CONFIG SET slave-priority 0
redis-cli -h 10.0.0.53 -p 6379 CONFIG SET slave-priority 0
redis-cli -h 10.0.0.51 -p 26379 sentinel failover myredis
```

验证选举结果：

```bash
redis-cli -h 10.0.0.51 -p 26379 Sentinel get-master-addr-by-name myredis
```