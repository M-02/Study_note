#### Docker本地网络类型

查看支持网络类型

```shell
docker network ls
```

测试使用各类网络类型

```shell
docker run network =XXX

none :无网络模式

bridge :默认模式，相当于NAT
docker run -it --name="c_ bri1" --network=bridge centos:6.9 /bin/bash

host :和宿主机共用宿主机命名空间，所有ip，端口，hosts文件，主机名
docker run -it --name="c_ host" --network=host centos:6.9 /bin/bash

container: 与其他容器公用Network Namespace

```



#### Docker跨主机访问-macvlan实现

```shell
docker network create --driver macvlan - -subnet=10.0.0.0/24 --gateway= 10.0.0.254 -o parent=eth0 macvlan_1

ip 1ink set eth0 promsic on (ubuntu或其他版本需要)

docker run -it --network macvlan_1 --ip=10.0.0.11 centos:6.9 /bin/bash
docker run -it --network macvlan_1 --ip=10.0.0.12 centos:6.9 /bin/bash
缺点：不能访问外网
```

#### Docker跨主机访问-overlay实现

1）启动consul服务，实现网络统一配置管理

```shell
docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap

consul: kv类型的存储数据库( key:value )
```
docker01、02_上: 
```shell
vim /lib/systemd/system/docker.service

docker1:（10.0.0.202）
#找到对应参数替换
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-store consul://10.0.0.202:8500 --cluster-advertise 10.0.0.202:2375

docker2:（10.0.0.203）
#找到对应参数替换
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-store consul://10.0.0.202:8500 --cluster-advertise 10.0.0.203:2375

systemctl daemon-reload
systemctl restart docker

```

2)创建overlay网络

```shell
在consul server端执行创建网络命令
docker network create -d overlay multihost

检查网络
docker network ls

NETWORK ID          NAME                DRIVER              SCOPE
a831d84cb458        bridge              bridge              local
081cfafe1edc        docker_gwbridge     bridge              local
95da90ef185f        host                host                local
88859625bf35        multihost           overlay             global
5f8c77dd4e2f        none                null                local

```

3)启动容器测试

```shell
docker1:（10.0.0.202）
 docker container run -it --network="multihost" --name="mysql" centos:7
 yum install iproute 
 ping 10.0.0.3   通过

docker2:（10.0.0.203）：
 docker container run -it --network="multihost" --name="mysql2" centos:7
 yum install iproute 
 ping 10.0.0.2   通过
```



每个容器有两块网卡,eth0实现容器间的通讯,eth1实现容器访问外网

