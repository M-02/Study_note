#### Dockerfile基本使用

创建一个lamp镜像

```shell
mkdir -p /opt/dockerfile
cd /opt/dockerfile
mkdir centos6.9_sshd 
vim Dockerfile

docker image build -t "cecntos_6.9_sshd:v1.0" ./   构建镜像

```

Dockerfile文件：

```dockerfile
# Centos6.9 sshd_LAMP
FROM centos:6.9

RUN mv /etc/yum.repos.d/*.repo /tmp && echo -e "[ftp]\nname=ftp\nbaseurl=ftp://172.17.0. 1/centos6.9\ngpgcheck =0">/etc/yum.repos.d/ftp.repo && yum makecache fast && yum install openssh- server htppd mysql mysql-server php php-mysql 

RUN /etc/init.d/sshd start && echo "123456" | passwd root --stdin && /etc/init.d/mysqld start && /etc/init.d/httpd start 
RUN mysq1 -e "grant all on *.* to root@'%' identified by '123';grant all on *,* to discuz@'%' identified by '123' ;create database discuz charset utf8;"

COPY init.sh
ENV CODEDIR /var/www/html/
ENV DATADIR /data/mysql/data
ADD bbs.tar.gz ${CODEDIR}
ADD https://mirrors.aliyun.com/centos/7.6.1810/0s/x8664/Packages/centos bookmarks-7-1.el7.noarch.rpm /tmp
VOLUME ["${CODEDIR}","${DATADIR}"]
EXPOSE 22
EXPOSE 80
EXPOSE 3306
CMD ["/bin/bash","/init.sh"]
```

init.sh

```shell
#!/bin/bash
/etc/init.d/mysqld start
mysq1 -e "grant all on *.* to root@'%' identified by '123' ;grant all on *.* to discuz'%' identified by '123'; create database discuz charset utf8;
/etc/init.d/httpd start
/usr/sbin/sshd -D
```



```shell
Dockerfile基础指令介绍：
FROM:         
	Syntax:
		centos:6.9
		centos@2199b8eb8390
		基础镜像

EXPOSE：
	Syntax:
    	EXPOSE:22
    	容器向外暴露的端口
    	
RUN:          
	Syntax:
		mv /etc/yum.repos.d/*.repo /tmp 
		["mysq1d", "-- initialize-ins ecure", "--user=mysq1" , "--bas edir=/usx/1oca1/mysq1", "--datadir=/data/mysq1/data"]
		构建镜像过程中运行的命令
		
CMD:           
	Syntax:
		CMD ["/usr/sbin/sshd","-D"]
		使用镜像启动容器时运行的命令

COPY:
	Syntax:
			<src>...   <dest>
			从dockerfile目录，拷贝目标文件到容器的指定目录下，可以支持通配符，如果拷贝的是目录，只拷贝目录下的子文件
			
ADD:
	Syntax:
			<src>...   <dest>
			<url>...   <desc>
			从dockerfile目录，拷贝目标文件到容器的指定目录下（压缩文件自动解压 .tar .tar.gz .tar.bz2 .tar.xz）可以指定原路径为URL地址
			
VOLUME: 
	Syntax:
		["var/www/html","/data/mysql/data"]  
		创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等

WORKDIR:
	Syntax:
		WORKDIR /path/to/workdir
		指定当前工作目录，相当于cd

ENV:
	Syntax:
		ENV PATH /usr/local/nginx/sbin:$PATH
		指定一个环境变量，会被后续 RUN 指令使用，并在容器运行时保持。
		
USER:
	Syntax: 
			USER daemon
			指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。当服务不需要管理员权限时，可以通过该命令指定运行用户。并且可以在之前创建所需要的用户，例如： RUN useradd -s /sbin/nologin -M www

ENTRYPOINT:
	Syntax:
	ENTRYPOINT ["/usr/sbin/sshd","-D","init.sh"]
	可以防止在启动容器时，第一进程被手工输入的命令替换掉，防止容器秒启秒挂
```



