#### MySQL启动和关闭

##### 日常启停

```shell
mysql.server start  --->  mysql_safe --->mysqld
systemctl start mysqld ---> mysqld

需要依赖于/etc/my.cnf
```

##### 维护性的任务

```shell
mysqld_safe --skip-grant-tables --skip-networking &

我们一般会将我们需要的参数临时加到命令行.
也会读取/etc/my.cnf的内容,但是如果冲突,命令行优先级最高

mysqld_safe &                     开启数据库方法之一
mysqladmin -uroot -p123 shutdown  以上开启方法，只能如此关闭
```

#### 初始化配置

##### 作用

1.影响数据库启动
2.影响客户端的各项功能

##### 初始化配置方法

1.初始化配置文件（/etc/my.cnf）
2.启动命令行上进行设置（如：mysqld_safe mysqld）
3.预编译时设置（仅限于编译安装时设置）

##### 初始化配置文件的书写格式

```
[标签]
XXX=XXX
[标签]
XXX=XXX
```

##### 配置文件的标签归类

```
服务器端
[mysqld]
[mysqld_safe]
[server]
客户端
[mysql]
[mysqladmin]
[mysqldump]
[client]
```

##### 配置文件设置样板

```mysql
#服务器端
[mysqld]
#用户
user=mysql
#软件安装目录
basedir=/application/mysql 
#数据路径
datadir=/data/mysql/data
#socket文件位置
socket=/tmp/mysql.sock
#服务器id号
server_id=6
#端口号
port=3306

#客户端配置
[mysql]
##socket文件位置
socket=/tmp/mysql.sock
```

##### 配置文件读取顺序

```
/etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf 

实际应用配置以最后读取的为准
```

##### 强制使用自定义配置文件

```
mysqld_safe  --defaults-file=etc/my.cnf &
```

#### MySQL连接管理

##### MySQL命令

```shell
注意：提前把用户授权做好
grant all on *.* to root@'10.0.0.%' identified by '1';
TCP/IP:
mysql -uroot -p -h 10.0.0.51 -P3306

Scoket:
mysql -uroot -p -S /tmp/mysql.sock
```

#### 多实例管理

##### 准备多个目录

```shell
mkdir -p /data/330{7,8,9}/data
```

##### 准备配置文件

```
cat > /data/3307/my.cnf <<EOF
#服务器端
[mysqld]
#用户
user=mysql
#软件安装目录
basedir=/application/mysql 
#数据路径
datadir=/data/3307/data
#socket文件位置
socket=/data/3307/mysql.sock
#服务器id号
server_id=7
#端口号
port=3307
log_bin=/data/3307/mysql-bin
log_error=/data/3307/mysql.log
EOF
```

##### 初始化三套数据

```shell
mv /etc/my.cnf /etc/my.cnf.bak
mysqld --initialize-insecure --user=mysql --datadir=/data/3307/data --basedir=/application/mysql

```

##### systemd管理多实例

```shell
 cd /etc/systend/system
 cp mysqld.service mysqld3307.serveice
 cp mysqld.service mysqld3308.serveice
 cp mysqld.service mysqld3309.serveice
 
 vim mysqld3307.serveice
 #修改为
 ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3307/my.cnf
 
  
 vim mysqld3308.serveice
 #修改为
 ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3308/my.cnf
 
 
 vim mysqld3309.serveice
 #修改为
 ExecStart=/application/mysql/bin/mysqld --defaults-file=/data/3309/my.cnf
```

##### 授权

```shell
chown -R mysql.mysql /data/*
```

##### 启动实例

```shell
systemctl start mysqld3307.service
systemctl start mysqld3308.service
systemctl start mysqld3309.service
```

##### 验证多实例

```shell
netstat -lnp|grep 330  

tcp6       0      0 :::3306                 :::*                    LISTEN      15017/mysqld        
tcp6       0      0 :::3307                 :::*                    LISTEN      52316/mysqld        
tcp6       0      0 :::3308                 :::*                    LISTEN      52363/mysqld        
tcp6       0      0 :::3309                 :::*                    LISTEN      52408/mysqld        
unix  2      [ ACC ]     STREAM     LISTENING     133934   52316/mysqld         /data/3307/mysql.sock
unix  2      [ ACC ]     STREAM     LISTENING     134184   52408/mysqld         /data/3309/mysql.sock
unix  2      [ ACC ]     STREAM     LISTENING     134059   52363/mysqld         /data/3308/mysql.sock
```

##### 连接实例

```shell
mysql -uroot -p -S /data/3307/mysql.sock
mysql -uroot -p -S /data/3308/mysql.sock
mysql -uroot -p -S /data/3309/mysql.sock

mysql -uroot -p  -P3307
mysql -uroot -p  -P3308
mysql -uroot -p  -P3309
```

