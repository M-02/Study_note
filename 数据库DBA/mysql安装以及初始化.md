#### 创建应用目录

```shell
mkdir -p /server/tools
mkdir -p /application
```

#### 下载MySQL二进制包

```shell
wget https://cdn.mysql.com/archives/mysql-5.7/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
```

#### 解压，移动

```shell
tar vxf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz

mv mysql-5.7.26-linux-glibc2.12-x86_64 /application/mysql

cd /application/mysql 
```

#### 创建MySQL用户以及处理原始环境

```shell
yum remove mariadb

useradd -s /sbin/nologin mysql
```

#### 设置环境变量

```shell
vim /etc/profile

export PATH=/application/mysql/bin:$PATH

source /etc/profile

mysql -V
```

#### 添加新磁盘，格式化并挂载磁盘

```shell
fdisk -l                       #查看所有磁盘
mkfs.xfs /dev/sdb
mkdir /data
blkid
vim /etc/fstab

UUID="9cae8337-79e4-4300-aa46-38a5ff99c015"    /data  xfs  defaults  0  0

mount -a
df -h
```

#### 授权,更改属主属组

```shell
chown -R mysql.mysql /application/*
chown -R mysql.mysql /data
```

#### 初始化数据（创建系统数据）

```shell
5.6版本 初始化命令 /app1ication/mysql/scripts/mysql_install_db
5.7版本：
mkdir /data/mysql/data -p
chown -R mysql.mysql /data
mysqld --initialize --user=mysql --basedir=/application/mysql --datadir=/data/mysql/data

# --initialize 参数:
#1.对于密码复杂度进行定制:12位，4种
#2.密码过期时间:180
#3.给root@localhost用户设置临时密码

2020-11-15T08:02:09.982496Z 1 [Note] A temporary password is generated for root@localhost: 8wy!d4=%wl1M

8wy!d4=%wl1M 临时密码

#--initialize-insecure 参数:
#无限制，无临时密码
 \rm -rf /data/mysql/data/*
mysqld --initialize-insecure --user=mysql --basedir=/application/mysql --datadir=/data/mysql/data
```

#### 配置文件准备

```shell
cat >/etc/my.cnf <<EOF
[mysqld]
user=mysql
basedir=/application/mysql 
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=6
port=3306
[mysql]
socket=/tmp/mysql.sock
EOF
```

#### 启动数据库

```shell
#sys-v启动方式
cp /application/mysql/support-files/mysql.server /etc/init.d/mysqld
service mysqld restart

#systemd启动方式
cat >/etc/systemd/system/mysqld.service <<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.htm1
After=network.target
After=syslog.target
[Install]
WantedBy=multi--user.target
[Service]
User=mysql
Group=mysql
ExecStart=/app1ication/mysql/bin/mysqld --defaults-file=/etc/my.cnf
LimitNOFILE=5000
EOF

systemctl start mysqld
#查看启动进程端口
netstat -lnp|grep 3306

ps -ef|grep 3306

```

#### 如何分析处理MySQL数据库无法启动

- without updating PID类似错误
  查看日志:
  /data/mysql/data/主机名.err
  [ERROR]上下文
- 可能情况:
  /etc/my .cnf路径不对等
  / tmp/mysql.sock文件修改过或删除过
  数据目录权限不是mysql
  参数改错了

#### 管理员密码设置（root@localhost）

```shell
mysqladmin -u root -p password 'root'
```

#### 管理员忘记密码操作

```shell
1，关闭数据库
service mysqld stop  

2，启动数据库到维护模式
mysqld_safe --skip-grant-tables --skip-networking &

3，登录并修改密码
mysql

select user,host,authentication_string from mysql.user;

flush privileges;

grant all on *.* to root@'localhost' identified by 'root';
grant all on *.* to HAIRUI@'%' identified by 'root';

4，关闭数据库，正常启动验证


```

