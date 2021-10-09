#### MySQL用户与权限管理

##### 作用

登录MySQL
管理MySQL

##### 用户的定义

用户名@'白名单'

```mysql
wordpress@'%'
wordpress@'localhost'
wordpress@'127.0.0.1'
wordpress@'10.0.0.%'
wordpress@'10.0.0.5%'
wordpress@'10.0.0.0/255.255.254.0'
wordpress@'10.0.%'
```

##### 用户的操作

创建用户

```mysql
create user cuoni@'10.0.0.%' identified by '123';      创建新用户以及设置密码

grant all on *.* to cuoni@'10.0.0.%' identified by '123';      自动创建新用户并授权，仅限MySQL8.0以前版本
```

查询用户

```mysql
select user,host from mysql.user;                       
```

修改用户密码

```mysql
alter  user cuoni@'10.0.0.%' identified by '123456';
```

删除密码

```mysql
drop user cuoni@'10.0.0.%'；
```

##### 权限管理

权限列表

```mysql
ALL

SELECT , INSERT, UPDATE, DELETE， CREATE， DROP, RELOAD, SHUTDOWN， PROCESS， FILE， REFERENCES，INDEX, ALTER,SHOW DATABASES ,SUPER，CREATE TEMPORARY TABLES ,LOCK TABLES，EXECUTE， REPLICATION SLAVE，REPLICATIONCLIENT，CREATE VIEW，SHOW VIEW，CREATE ROUTINE, ALTER ROUTINE, CREATE USER， EVENT，TRIGGER， CREATE  TABLESPACE .

with grant option                   给别人授权的权限   
```

授权命令

```mysql
grant all on *.* to cuoni@'10.0.0.%' identified by '123' with grant option; 

grant 权限 on 作用目标 to 用户 identified by 密码;  
```

授权示例

```mysql
1.创建一个管理员用户root, 可以通过10网段，管理数据库

grant all on *.* to root@'10.0.0.*' identified by '123' with grant option;

2.创建一个应用用户wordpress, 可以通过10网段，wordpress库下的所有表进行SELECT , INSERT， UPDATE, DELETE.

grant SELECT,INSERT,UPDATE,DELETE on wordpress.* to wordpress@'110.0.0.*' identified by '123';

```

回收权限

```mysql
show grants for wordpress@'10.0.0.%';        查看用户权限

revoke delete on wordpress.* from wordpress@'10.0.0.%';  收回用户删除权限
```

关于生产中开用户
(1)如何沟通开用户
1.是否有邮件批复
2.对哪些库和表做操作
3.做什么操作
4.从什么地址来登录
(2)开发人员找你要root用户密码?
1.走流程拒绝他
2.如果是金融类的公司
(1)原则上是不允许任何非DBA人员持有或申请root
(2)如果有人私下索要root密码，及时举报。