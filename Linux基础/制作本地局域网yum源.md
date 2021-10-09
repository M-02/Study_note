#### 制作本地局域网yum源

1、安装vsftpd软件

```shell
yum install vsftpd -y
```

2、启动vsftpd

```shell
systemctl enable vsftpd

systemctl start vsftpd
```

3、挂载iso系统镜像到虚拟机

4、配置yum仓库

```shell
mkdir -p /var/ftp/centos7
mount /dev/sr0  /var/ftp/centos7

cat >/yum.repo.d/ftp_7.repo <<EOF
[ftp]
name=ftpbase
baseurl=ftp://10.0.0.100/centos7
enabled=1
gpgcheck=0
EOF

yum clean all
```

