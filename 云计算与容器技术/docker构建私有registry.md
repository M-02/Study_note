#### docker构建私有registry

启动registry 

```shell
docker run -d -p 5000:5000  --restart=always  --name registry  -v  /opt/registry:/var/lib/registry   registry 
```

修改/etc/docker/daemon.json

```shell
vim  /etc/docker/daemon.json

{
"registry-mirrors":["https://XXXXXX.mirror.aliyuncs.com"],
 "insecure-registries":["10.0.0.202:5000"]
}

```

打标签

```shell
docker tag nginx:latest 10.0.0.202:5000/cuoni/nginx:v1
```

推送镜像

```shell
docker push 10.0.0.202:5000/cuoni/nginx:v1
```

拉取镜像

```shell
docker image pull 10.0.0.202:5000/cuoni/nginx:v1
```

本地仓库加入安全认证

```shell
生成密码:
yum install httpd-tools -y
mkdir /opt/registry-auth/ -p
htpasswd  -Bbn  cuoni 123 > /opt/registry-auth/htpasswd
```

重新启动带有秘钥功能的registry容器

```shell
docker container rm -f  `docker container ls -a -q`

docker run -d -p 5000:5000 -v /opt/registry-auth/:/auth/ -v /opt/registry:/var/1ib/registry --name register-auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" registry
```

推送镜像失败

```
docker push 10.0.0.202:5000/cuoni/centos:v1

被拒绝报错：The push refers to repository [10.0.0.202:5000/cuoni/centos]
Get http://10.0.0.202:5000/v2/: dial tcp 10.0.0.202:5000: connect: connection refused
```

登录仓库

```shell
docker login 10.0.0.202:5000
Username: cuoni
Password: 

Login Succeeded
```

推送镜像成功

```shell
docker push 10.0.0.202:5000/cuoni/centos:v1 

The push refers to repository [10.0.0.202:5000/cuoni/centos]
613be09ab3c0: Pushed 
v1: digest: sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9 size: 529
```

拉取镜像失败

```shell
docker pull 10.0.0.202:5000/cuoni/centos:v1 

Error response from daemon: Get http://10.0.0.202:5000/v2/cuoni/centos/manifests/v1: no basic auth credentials
```

登录之后成功拉取

```shell
docker pull 10.0.0.202:5000/cuoni/centos:v1

v1: Pulling from cuoni/centos
75f829a71a1c: Pull complete 
Digest: sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9
Status: Downloaded newer image for 10.0.0.202:5000/cuoni/centos:v1
10.0.0.202:5000/cuoni/centos:v1
```

