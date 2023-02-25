#### docker

```bash
docker -v  															查看版本
docker version  													版本详细状态
docker info 														运行状态
```



#### 镜像管理命令：

```shell
docker search centos                         					搜索centos镜像
docker search centos -s 100                  					搜索热度100以上的centos
docker pull daocloud.io/library/centos:7           	   		    拉取镜像
docker images                                       			查看镜像
docker image ls -q                                 				只查看镜像id
docker image inspect 镜像id（镜像地址）                            查看镜像详情
docker image rm/rmi 镜像id(镜像名称)                              删除镜像
docker image rm/rmi -f  镜像id(镜像名称)           			  	强制删除镜像
注意: 容器运行中不能删除，将容器停止后，删除容器在删除镜像。
docker images -q                                    		   查看全部镜像id     
docker image rm/rmi `docker images ls -q`                      删除所有镜像
docker image save 3556258649b2 > / tmp/ubu. tar				   导出镜像
docker image load -i / tmp/ubu . tar						   导入镜像
```



#### 容器管理

```bash
docker container run -it    --name="自定义容器名"   镜像id     交互式运行容器
-t让docker分配一个伪终端并绑定到容器的标准输入上, -i则让容器的标准输入保持打开

docker container run -d    --name="自定义容器名"   镜像id     守护式运行容器
docker container ls                                         查看正在运行的容器
docker container ls  -a/docker ps -a                          查看容器
docker container inspect   容器名字                            查看容器详细信息

CONTAINER ID：容器的唯一号码(自动生成的)
STATUS             ：容器运行状态（up，exited）
NAMES              ：容器的名字(可以自动,也可以手工指定)
```



#### 容器应用场景

```shell
交互式的容器:工具类:开发,测试,临时性的任务
docker container run -it - -name= ="oldguo_ cent76"  --rm 9f38484d220f     退出自动删除

守护式容器：网络服务
docker container run -d -p 8080:80   --name="nginx1"  nginx 
```



#### 容器的启动\关闭\连接

```shell
守护式容器的关闭和启动
 docker container stop nginx1		关闭容器
 docker container start nginx1	    开启容器
 docker kill 名字(id)                强制终止容器
 docker kill `docker container ls -a -q`       杀死所有running状态的容器
 快捷键：ctrl+p+q                     后台运行容器
 
交互式的容器的关闭和启动
 docker container stop centos         关闭容器
 docker container start -i centos	  开启容器并连接

容器的连接方法:
docker container attach centos         连接容器
docker container exec -it  centos /bin/bash     子进程方式登录（在已有工作容器中生成子进程登录，可以进行容器调试，退出也不会影响当前容器）
```

#### docker容器的网络访问

```shell
指定映射(docker 会自动添加一条iptables规则来实现端口映射)
    -p hostPort:containerPort            映射宿主机指定端口到容器指定端口（一 一对应）
    -p ip:hostPort:containerPort         指定容器IP、宿主机端口、容器端口
    -p ip::containerPort(随机端口:32768-60999)        指定容器IP和容器端口，宿主机端口随机映射
    -p hostPort:containerPort/udp        指定 udp 协议的端口映射
    -p 81:80 –p 443:443                  多端口映射，适用于多服务

随机映射
    docker run -P 80（随机端口:32768-60999）           映射宿主机随机端口到容器指定端口
```

#### 容器的其他管理

```shell
docker container ls -a  -q  等价于docker ps  -a -q 查看所有容器id

docker container top 容器ID  等价于docker top 容器ID 管理容器进程

docker container logs 容器ID                     查看容器日志
docker container logs -t 容器ID                  显示时间戳查看容器日志
docker container logs -tf 容器ID                 类似于tail -f 实时显示
docker container logs -tf  --tail 10 容器ID      查看最后10条日志
docker container logs -tf  --tail 0 容器ID       查看最后的日志
```

#### docker的数据卷实现持久化存储

手工交互数据：

```shell
docker container cp 宿主机路径  容器名称 : 容器内路径
docker container cp 容器名称 :容器内路径  宿主机路径
```

Volume实现宿主机和容器的数据共享

```shell
docker container run -d --name="nginx_1" -p 80:80 -v 宿主机路径:容器内路径        数据持久化
```

数据卷容器

```shell
（1）启动数据卷容器

docker run -d   --name"数据卷容器名" -v  宿主机路径:容器内路径   centos  /bin/bash

（2）使用数据卷容器

docker run -d -p 80:80 --volumes-from   数据卷容器名  --name=“nginx_2”   nginx

作用：在集中管理集群中，大批量容器都需要挂载相同的多个数据卷是，可以采用数据卷容器进行统一管理
```

