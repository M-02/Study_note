准备五台虚拟机,

10.0.0.11,hdss7-11.host.com

10.0.0.12,hdss7-12.host.com

10.0.0.21,hdss7-21.host.com

10.0.0.22,hdss722.host.com

10.0.0.222，hdss7-222.host.com         运维管理主机

#### 配置DNS环境

安装常用软件

```shell
yum install -y wget telnet tree nmap sysstat lrzsz dos2unix bind-utils
```

在主机hdss7-11.host.com安装bind

```shell
yum install -y bind 
```

配置bind主配置文件

```shell
vim /etc/named.conf

listen-on port 53 { 10.0.0.11; };
allow-query     { any; };
forwarders      { 10.0.0.2; };
recursion yes;     
dnssec-enable no;
dnssec-validation no;
```

检查named.conf

```
named-checkconf 
```

  区域配置文件

```shell
zone "host.com" IN {
		type  master;
		file  "host.com.zone" ;
		allow-update { 10.0.0.11; };
};

zone "od.com" IN{
		type  master;
		file  "od.com.zone" ;
		allow-update { 10.0.0.11; };
};
```

配置主机域数据文件
```
$ORIGIN host.com.
$TTL 600          ;10 minutes
@   IN SOA dns.host.com. dnsadmin.host.com. (
2020111201  ;serial
10800     ;refresh (3 hours )
900       ;retry ( 15 minutes)
604800    ;expire (1 week)
86400     ;minimum (1 day)
NS        ;dns.host.com.
$TTL 60 ; 1 minute
dns        A          10.0.0.11
HDSS7-11   A          10.0.0.11
HDSS7-12   A          10.0.0.12
HDSS7-21   A          10.0.0.21
HDSS7-22   A          10.0.0.22
HDSS7-222  A          10.0.0.222
```

测试

```shell
[root@hdss7-11 /etc ]$ dig -t A hdss7-21.host.com @10.0.0.11 +short 
10.0.0.21
[root@hdss7-11 /etc ]$ dig -t A hdss7-222.host.com @10.0.0.11 +short
10.0.0.222
```

配置DNS客户端

```shell
vim /etc/resolv.conf

search host.com
nameserver 10.0.0.11
```

#### 准备证书签发环境

在hdss7-222上

安装CFSSL

```shell
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssl-json_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
```

赋予执行权限

```shell
chmod -x cfssl*
```

重命名

```shell
for x in cfssl*; do mv $x ${x%*_linux-amd64};  done
```

移动文件到目录 (/usr/bin)

```shell
mv cfssl* /usr/bin
```

自签证书

```shell
mkdir -p /opt/certs
cd /opt/certs
vim ca-csr.json

{
    "CN": "Cuoni",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "shanghai",
            "O": "choulaoyang",
            "ST": "shanghai",
            "OU": "print"
        }
    ],
    "ca":{
    "expiry":"175200h"
    }
}
```

CN: Common Name ,浏览器使用该字段验证网站是否合法, -般写的是域名。非常重要。浏览器使用该字段验证网站是否合法
C: Country,国家
ST:State,州,省
L: Locality ,地区,城市
O: Organization Name ,组织名称,公司名称
OU: Organization Unit Name ,组织单位名称,公司部门
"expiry":"175200h":证书过期时间：20年

生成证书

```shell
cfssl gencert -initca ca-csr.json | cfssl-json -bare ca
```

#### 安装Docker环境（21,22,222）

```shell
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

配置Docker服务

```shell
mkdir -p /etc/docker
vim /etc/docker/daemon.json

{
"graph": "/data/docker",
"storage-driver": "overlay2",
"insecure-registries": ["registry.access.redhat.com","quay.io","harbor.od.com"],
"registry-mirrors": ["https://stuue7zh.mirror.aliyuncs.com"],
"bip": "172.7.21.1/24",
"exec-opts": ["native.cgroupdriver-systemd"],
"live-restore": true
}

其中，"bip": "172.7.21.1/24",根据自己的主机所在网段分配

systemctl start docker
```

#### 部署docker镜像私有仓库harbor

hdss-200.host.com上

下载软件二进制包解压

```shell
wget https://github.com/goharbor/harbor/releases/download/v2.0.4-rc1/harbor-offline-installer-v2.0.4-rc1.tgz

tar vxf harbor-offline-installer-v2.0.4-rc1.tgz -C /opt/
mv harbor harbor-v2.0.4
ln -s harbor-v2.0.4 /opt/harbor
```

配置harbor.yml

```
vim /opt/harbor/harbor.yml

hostname:haibor.od.com
http:
  port:180
data_volume:/data/harbor
location:/data/harbor/logs

mkdir -p /data/harbor/logs  
```

安装 docker-compose 

```shell
 yum install docker-compose -y  
```

执行harbor安装脚本

```
./install.sh  
```

检查是否安装成功

```shell
docker-compose ps 
```

安装nginx

```shell
yum install nginx -y
```

配置Nginx代理

```shell
vim /etc/nginx/conf.d/harbor.od.com.conf

server{
     listen      80;
     server_name harbor.od.com;
     client_max_body_size  1000m;
     location / {
      proxy_pass  http://127.0.0.1:180;
}
}

```

启动nginx

```shell
systemctl start nginx   
systemctl enable nginx
```

hdss7-11添加解析记录

```
vim /var/named/od.com.zone

harbor    A      10.0.0.222

注意serial前滚一个序号

systemctl restart named

dig -t A harbor.od.com +short  
10.0.0.222
```

浏览器输入http://harbor.od.com/测试

登录，新建项目，public，公开

拉取一个镜像

```shell
docker image pull nginx:1.7.9
```

打标签

```shell
docker tag 84581e99d807 harbor.od.com/public/nginx:v1.7.9
```

登录http://harbor.od.com/，输入用户名密码

```shell
docker login harbor.od.com
```

推送镜像

```shell
docker image push harbor.od.com/public/nginx:v1.7.9
```

#### 部署master节点服务

部署etcd集群

| 主机名            | 角色        | ip        |
| ----------------- | ----------- | --------- |
| hdss7-12.host.com | etcd lead   | 10.0.0.12 |
| hdss7-21.host.com | etcd follow | 10.0.0.21 |
| hdss7-22.host.com | etcd follow | 10.0.0.22 |

签发etcd证书

证书签发服务器 hdss7-200:

- 创建ca的json配置: /opt/certs/ca-config.json

- server 表示服务端连接客户端时携带的证书，用于客户端验证服务端身份
- client 表示客户端连接服务端时携带的证书，用于服务端验证客户端身份
- peer 表示相互之间连接时使用的证书，如etcd节点之间验证

```shell
vim /opt/certs/ca-config.json

{
    "signing": {
        "default": {
            "expiry": "175200h"
        },
        "profiles": {
            "server": {
                "expiry": "175200h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "175200h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            },
            "peer": {
                "expiry": "175200h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            }
        }
    }
}
```

创建etcd证书配置：/opt/certs/etcd-peer-csr.json

```shell
vim /opt/certs/etcd-peer-csr.json

{
    "CN": "k8s-etcd",
    "hosts": [
        "10.0.0.11",
        "10.0.0.12",
        "10.0.0.21",
        "10.0.0.22"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "od",
            "OU": "ops"
        }
    ]
}
```

签发证书

```shell
cd /opt/certs/

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=peer etcd-peer-csr.json |cfssl-json -bare etcd-peer

ll etcd-peer*

-rw-r--r-- 1 root root 1062 Jan  5 17:01 etcd-peer.csr
-rw-r--r-- 1 root root  363 Jan  5 16:59 etcd-peer-csr.json
-rw------- 1 root root 1675 Jan  5 17:01 etcd-peer-key.pem
-rw-r--r-- 1 root root 1428 Jan  5 17:01 etcd-peer.pem
```

#### 安装etcd

etcd地址：https://github.com/etcd-io/etcd/

实验使用版本: [etcd-v3.1.20-linux-amd64.tar.gz](https://github.com/etcd-io/etcd/releases/download/v3.1.20/etcd-v3.1.20-linux-amd64.tar.gz)

本次安装涉及：hdss7-12，hdss7-21，hdss7-22

下载etcd

```shell
useradd -s /sbin/nologin -M etcd
cd /opt/src/
wget https://github.com/etcd-io/etcd/releases/download/v3.1.20/etcd-v3.1.20-linux-amd64.tar.gz
tar -xf etcd-v3.1.20-linux-amd64.tar.gz 
mv etcd-v3.1.20-linux-amd64 /opt/tcd-v3.1.20
ln -s /opt/etcd-v3.1.20 /opt/etcd
mkdir -p /opt/etcd/certs /data/etcd /data/logs/etcd-server /opt/certs
```

下发证书到各个etcd上(10.0.0.222上)

```shell
cd /opt/certs/

for i in 12 21 22;do scp ca.pem etcd-peer.pem etcd-peer-key.pem hdss7-${i}:/opt/etcd/certs/ ;done

```

创建启动脚本(部分参数每台机器不同)

```shell
vim /opt/etcd/etcd-server-startup.sh

#!/bin/sh
# listen-peer-urls etcd节点之间通信端口
# listen-client-urls 客户端与etcd通信端口
# quota-backend-bytes 配额大小
# 需要修改的参数：name,listen-peer-urls,listen-client-urls,initial-advertise-peer-urls

WORK_DIR=$(dirname $(readlink -f $0))
[ $? -eq 0 ] && cd $WORK_DIR || exit

/opt/etcd/etcd --name etcd-server-7-12 \
    --data-dir /data/etcd/etcd-server \
    --listen-peer-urls https://10.0.0.12:2380 \
    --listen-client-urls https://10.0.0.12:2379,http://127.0.0.1:2379 \
    --quota-backend-bytes 8000000000 \
    --initial-advertise-peer-urls https://10.0.0.12:2380 \
    --advertise-client-urls https://10.0.0.12:2379,http://127.0.0.1:2379 \
    --initial-cluster  etcd-server-7-12=https://10.0.0.12:2380,etcd-server-7-21=https://10.0.0.21:2380,etcd-server-7-22=https://10.0.0.22:2380 \
    --ca-file ./certs/ca.pem \
    --cert-file ./certs/etcd-peer.pem \
    --key-file ./certs/etcd-peer-key.pem \
    --client-cert-auth  \
    --trusted-ca-file ./certs/ca.pem \
    --peer-ca-file ./certs/ca.pem \
    --peer-cert-file ./certs/etcd-peer.pem \
    --peer-key-file ./certs/etcd-peer-key.pem \
    --peer-client-cert-auth \
    --peer-trusted-ca-file ./certs/ca.pem \
    --log-output stdout
```

创建用户并添加权限

```
useradd -s /sbin/nologin -M etcd
id etcd
chmod +x /opt/etcd/etcd-server-startup.sh
chown -R etcd.etcd /opt/etcd/ /data/etcd /data/logs/etcd-server
```

#### 启动etcd

因为这些进程都是要启动为后台进程，要么手动启动，要么采用后台进程管理工具，实验中使用后台管理工具

```shell
yum install -y supervisor
systemctl start supervisord ; systemctl enable supervisord
vim /etc/supervisord.d/etcd-server.ini

[program:etcd-server-7-12]
command=/opt/etcd/etcd-server-startup.sh              ; the program (relative uses PATH, can take args)
numprocs=1                                            ; number of processes copies to start (def 1)
directory=/opt/etcd                              ; directory to cwd to before exec (def no cwd)
autostart=true                                        ; start at supervisord start (default: true)
autorestart=true                                      ; retstart at unexpected quit (default: true)
startsecs=30                                          ; number of secs prog must stay running (def. 1)
startretries=3                                        ; max # of serial start failures (default 3)
exitcodes=0,2                                         ; 'expected' exit codes for process (default 0,2)
stopsignal=QUIT                                       ; signal used to kill process (default TERM)
stopwaitsecs=10                                       ; max num secs to wait b4 SIGKILL (default 10)
user=etcd                                             ; setuid to this UNIX account to run the program
redirect_stderr=true                                  ; redirect proc stderr to stdout (default false)
stdout_logfile=/data/logs/etcd-server/etcd.stdout.log ; stdout log path, NONE for none; default AUTO
stdout_logfile_maxbytes=64MB                          ; max # logfile bytes b4 rotation (default 50MB)
stdout_logfile_backups=5                              ; # of stdout logfile backups (default 10)
stdout_capture_maxbytes=1MB                           ; number of bytes in 'capturemode' (default 0)
stdout_events_enabled=false                           ; emit events on stdout writes (default false)


supervisorctl update           #刷新脚本
etcd-server-7-12: added process group
```

etcd 进程状态查看

```shell
supervisorctl status  # supervisorctl 状态
etcd-server-7-12                 RUNNING   pid 22375, uptime 0:00:39

netstat -lntp|grep etcd
tcp        0      0 10.0.0.12:2379          0.0.0.0:*               LISTEN      2060/etcd       
tcp        0      0 127.0.0.1:2379          0.0.0.0:*               LISTEN      2060/etcd          
tcp        0      0 10.0.0.12:2380          0.0.0.0:*               LISTEN      2060/etcd 

/opt/etcd/etcdctl member list # 随着etcd重启，leader会变化


/opt/etcd/etcdctl cluster-health

```

etcd 启停方式

```shell
 supervisorctl start etcd-server-7-12
 supervisorctl stop etcd-server-7-12
 supervisorctl restart etcd-server-7-12
 supervisorctl status etcd-server-7-12
```

### apiserver 安装

#### 下载kubernetes服务端

aipserver 涉及的服务器：hdss7-21，hdss7-22

下载 kubernetes 二进制版本包需要科学上网工具

- 进入kubernetes的github页面: https://github.com/kubernetes/kubernetes
- 进入tags页签: https://github.com/kubernetes/kubernetes/tags
- 选择要下载的版本: https://github.com/kubernetes/kubernetes/releases/tag/v1.15.2
- 点击 CHANGELOG-${version}.md  进入说明页面: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.15.md#downloads-for-v1152
- 下载Server Binaries: https://dl.k8s.io/v1.15.2/kubernetes-server-linux-amd64.tar.gz

```shell
cd /opt/src
wget https://dl.k8s.io/v1.15.2/kubernetes-server-linux-amd64.tar.gz

tar -xf kubernetes-server-linux-amd64.tar.gz 
mv kubernetes /opt/kubernetes-v1.15.2
ln -s /opt/release/kubernetes-v1.15.2 /opt/kubernetes
ll /opt/kubernetes


cd /opt/kubernetes
rm -f kubernetes-src.tar.gz 
cd server/bin/
rm -f *.tar *_tag  # *.tar *_tag 镜像文件

```

#### 3.2.2. 签发证书

签发证书 涉及的服务器：hdss7-200

- 签发client证书（apiserver和etcd通信证书）

```shell
cd /opt/certs/
vim /opt/certs/client-csr.json

{
    "CN": "k8s-node",
    "hosts": [
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "od",
            "OU": "ops"
        }
    ]
}


cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client client-csr.json |cfssl-json -bare client

ls client* -l
```

- 签发server证书（apiserver和其它k8s组件通信使用）

```shell
# hosts中将所有可能作为apiserver的ip添加进去，VIP 10.0.0.10 也要加入
vim /opt/certs/apiserver-csr.json

{
    "CN": "k8s-apiserver",
    "hosts": [
        "127.0.0.1",
        "192.168.0.1",
        "kubernetes.default",
        "kubernetes.default.svc",
        "kubernetes.default.svc.cluster",
        "kubernetes.default.svc.cluster.local",
        "10.0.0.10",
        "10.0.0.21",
        "10.0.0.22",
        "10.0.0.23"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "od",
            "OU": "ops"
        }
    ]
}


cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server apiserver-csr.json |cfssl-json -bare apiserver

ls apiserver* -l
```

- 证书下发

```shell
 for i in 21 22;do echo hdss7-$i;ssh hdss7-$i "mkdir /opt/kubernetes/server/bin/certs";scp apiserver-key.pem apiserver.pem ca-key.pem ca.pem client-key.pem client.pem hdss7-$i:/opt/kubernetes/server/bin/certs/;done
```

#### 配置apiserver日志审计

aipserver 涉及的服务器：hdss7-21，hdss7-22

```shell
mkdir /opt/kubernetes/conf

vim /opt/kubernetes/conf/audit.yaml # 打开文件后，设置 :set paste，避免自动缩进

apiVersion: audit.k8s.io/v1beta1 # This is required.
kind: Policy
# Don't generate audit events for all requests in RequestReceived stage.
omitStages:
  - "RequestReceived"
rules:
  # Log pod changes at RequestResponse level
  - level: RequestResponse
    resources:
    - group: ""
      # Resource "pods" doesn't match requests to any subresource of pods,
      # which is consistent with the RBAC policy.
      resources: ["pods"]
  # Log "pods/log", "pods/status" at Metadata level
  - level: Metadata
    resources:
    - group: ""
      resources: ["pods/log", "pods/status"]

  # Don't log requests to a configmap called "controller-leader"
  - level: None
    resources:
    - group: ""
      resources: ["configmaps"]
      resourceNames: ["controller-leader"]

  # Don't log watch requests by the "system:kube-proxy" on endpoints or services
  - level: None
    users: ["system:kube-proxy"]
    verbs: ["watch"]
    resources:
    - group: "" # core API group
      resources: ["endpoints", "services"]

  # Don't log authenticated requests to certain non-resource URL paths.
  - level: None
    userGroups: ["system:authenticated"]
    nonResourceURLs:
    - "/api*" # Wildcard matching.
    - "/version"

  # Log the request body of configmap changes in kube-system.
  - level: Request
    resources:
    - group: "" # core API group
      resources: ["configmaps"]
    # This rule only applies to resources in the "kube-system" namespace.
    # The empty string "" can be used to select non-namespaced resources.
    namespaces: ["kube-system"]

  # Log configmap and secret changes in all other namespaces at the Metadata level.
  - level: Metadata
    resources:
    - group: "" # core API group
      resources: ["secrets", "configmaps"]

  # Log all other resources in core and extensions at the Request level.
  - level: Request
    resources:
    - group: "" # core API group
    - group: "extensions" # Version of group should NOT be included.

  # A catch-all rule to log all other requests at the Metadata level.
  - level: Metadata
    # Long-running requests like watches that fall under this rule will not
    # generate an audit event in RequestReceived.
    omitStages:
      - "RequestReceived"
```

####  配置启动脚本

aipserver 涉及的服务器：hdss7-21，hdss7-22

- 创建启动脚本

```shell
 vim /opt/kubernetes/server/bin/kube-apiserver-startup.sh
#!/bin/bash

WORK_DIR=$(dirname $(readlink -f $0))
[ $? -eq 0 ] && cd $WORK_DIR || exit

/opt/kubernetes/server/bin/kube-apiserver \
    --apiserver-count 2 \
    --audit-log-path /data/logs/kubernetes/kube-apiserver/audit-log \
    --audit-policy-file ../../conf/audit.yaml \
    --authorization-mode RBAC \
    --client-ca-file ./certs/ca.pem \
    --requestheader-client-ca-file ./certs/ca.pem \
    --enable-admission-plugins NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota \
    --etcd-cafile ./certs/ca.pem \
    --etcd-certfile ./certs/client.pem \
    --etcd-keyfile ./certs/client-key.pem \
    --etcd-servers https://10.0.0.12:2379,https://10.0.0.21:2379,https://10.0.0.22:2379 \
    --service-account-key-file ./certs/ca-key.pem \
    --service-cluster-ip-range 192.168.0.0/16 \
    --service-node-port-range 3000-29999 \
    --target-ram-mb=1024 \
    --kubelet-client-certificate ./certs/client.pem \
    --kubelet-client-key ./certs/client-key.pem \
    --log-dir  /data/logs/kubernetes/kube-apiserver \
    --tls-cert-file ./certs/apiserver.pem \
    --tls-private-key-file ./certs/apiserver-key.pem \
    --v 2
    
    
    chmod +x /opt/kubernetes/server/bin/kube-apiserver-startup.sh 
```

- 配置supervisor启动配置

```shell
vim /etc/supervisord.d/kube-apiserver.ini

[program:kube-apiserver-7-21]
command=/opt/kubernetes/server/bin/kube-apiserver-startup.sh
numprocs=1
directory=/opt/kubernetes/server/bin
autostart=true
autorestart=true
startsecs=30
startretries=3
exitcodes=0,2
stopsignal=QUIT
stopwaitsecs=10
user=root
redirect_stderr=true
stdout_logfile=/data/logs/kubernetes/kube-apiserver/apiserver.stdout.log
stdout_logfile_maxbytes=64MB
stdout_logfile_backups=5
stdout_capture_maxbytes=1MB
stdout_events_enabled=false

mkdir -p /data/logs/kubernetes/kube-apiserver
supervisorctl update
supervisorctl status

```

- 启停apiserver

```
 supervisorctl start kube-apiserver-7-21
 supervisorctl stop kube-apiserver-7-21
 supervisorctl restart kube-apiserver-7-21
 supervisorctl status kube-apiserver-7-21
```

