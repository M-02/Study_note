#### 准备环境

配置hosts

```shell
cat >> /etc/hosts << EOF
10.0.0.202 master
10.0.0.203 node1
10.0.0.204 node2
EOF
```

 设置主机名，三台分别执行

```shell
hostnamectl set-hostname master
hostnamectl set-hostname node1
hostnamectl set-hostname node2
```

 关闭防火墙

```shell
systemctl disable firewalld
systemctl stop firewalld
```

禁用SELinux，让容器可以顺利地读取主机文件系统

 ```shell
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config
 ```

   下载docker.repo包至 /etc/yum.repos.d/目录

```shell
wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

在/etc/yum.repos.d/目录中新建kubernetes仓库文件

```shell
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0
repo_gpgcheck=0
EOF
```

#### 开始安装

安装docker

```shell
yum install docker-ce
设置开机启动
systemctl enable docker && systemctl start docker
```

开始安装kubelet kubeadm kubectl 

```shell
yum install -y kubelet kubeadm kubectl etcd
```

启动kubelet并设置开机自启

```shell
systemctl enable kubelet etcd && systemctl start kubelet etcd
```

#### 配置阶段

配置主节点ETCD

```shell
vim /etc/etcd/etcd.conf
替换
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="http://10.0.0.204:2379"

重启etcd
systemctl restart etcd.service 
```

测试etcd

```shell
etcdctl set name cuoni
cuoni
[root@master ~ ]$ etcdctl get name      
cuoni
[root@master ~ ]$ 
```

配置