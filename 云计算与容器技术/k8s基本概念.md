### Kubernetes基本概念

#### 四组基本概念

##### Pod/Pod控制器

1. Pod
    Pod是K8S里能够被运行的最小的逻辑单元(原子单元)
    1个Pod里面可以运行多个容器,它们共享UTS+NET +IPC名称空间
    可以把Pod理解成豌豆荚,而同一Pod内的每个容器是一颗颗豌豆
    1个Pod里运行多个容器,又叫:边车( SideCar )模式

2. Pod控制器
    Pod控制器是Pod启动的一 -种模板,用来保证在K8S里启动的Pod
    应始终按照人们的预期运行(副本数、生命周期、健康状态检查... )

  ​	K8S内提供了众多的Pod控制器,常用的有以下几种:
  ​	Deployment      部署
  ​	DaemonSet     
  ​	ReplicaSet
  ​	StatefulSet
  ​	Job
  ​	Cronjob

##### Name/Namespace

1. Name 
   由于K8S内部,使用"资源”来定义每一-种逻辑概念(功能)故每种' 资源”, 都应该有自己的"名称"
   "资源”有api版本( apiVersion )类别( kind )、元数据.( metadata )、定义清单( spec)、状态( status )等配置信息
   "名称”通常定义在"资源”的“元数据”信息里
2. Namespace
   随着项目增多、人员增加、集群规模的扩大,需要- -种能够隔离K8S内各种“资源”的方法,这就是名称空间
   名称空间可以理解为K8S内部的虚拟集群组不同名称空间内的"资源”, 名称可以相同,相同名称空间内的同种
   “资源”，"名称”不能相同
   合理的使用K8S的名称空间,使得集群管理员能够更好的对交付到K8S里的服务进行分类管理和浏览
   K8S里默认存在的名称空间有: default、kube-system、 kube- public
   查询K8S里特定“资源”要带_上相应的名称空间

##### Label/Label选择器

1. 
   Label

   标签是k8s特色的管理方式,便于分类管理资源对象。
   一个标签可以对应多个资源，一个资源也可以有多个标签,它们是多对多的关系。
   一个资源拥有多个标签,可以实现不同维度的管理。
   标签的组成: key=value
   与标签类似的，还有一-种“注解”( annotations )

2. Label选择器
   给资源打上标签后,可以使用标签选择器过滤指定的标签
   标签选择器目前有两个:基于等值关系(等于、不等于)和基于集合关系(属于、不属于、存在)
   许多资源支持内嵌标签选择器字段
   	matchl abels
   	matchExpressions

##### Service/Ingress

1. Service
   在K8S的世界里, 虽然每个Pod都会被分配一个单独的IP地址 ,但这个IP地址会随着Pod的销毁而消失
   Service (服务)就是用来解决这个问题的核心概念
   一个Service可以看作- -组提供相同服务的Pod的对外访问接口
   Service作用于哪些Pod是通过标签选择器来定义的
2. Ingress
   Ingress是K8S集群里工作在OSI网络参考模型下,第7层的应用,对外暴露的接C ]
   Service只能进行4流量调度,表现形式是ip+ port
   Ingress则可以调度不同业务域、 不同URL访问路径的业务流量



#### k8s核心组件

1. ##### 配置存储中心→etcd服务

2. ##### 主控( master )节点

   ######      kube-apiserver服务（k8s大脑）

   ​     	提供了集群管理的RESTAPI接口(包括鉴权、数据校验及集群状态变更)
   ​		 负责其他模块之间的数据交互,承担通信枢纽功能
   ​		 是资源配额控制的入口
   ​	 	提供完备的集群安全机制

######        kube-controller-manager服务

​           由一系列控制器组成,通过apiserver监控整个集群的状态,并确保集群处于预期的工作状态
​			Node Controller              （节点控制器）
​			Deployment Controller  （pod控制器）
​			Service C ontroller          （服务控制器）
​			Volume ( ontroller          （存储卷控制器）
​			Endpoint Controller       （接入点控制器）
​			Garbage Controller        （垃圾回收控制器）
​			Namespace Controller   （名称空间控制器）
​			Job Controller                   （作业控制器）
​			Resource quta Controller （资源控制器）
​			...

######         kube-scheduler服务

   			主要功能是接收调度pod到适合的运算节点上
​				预算策略( predict )
​				优选策略( priorities )

3. ##### 运算( node )节点

###### kube-kubelet服务（主要干活的）

 		简单地说, kubelet的主要功能就是定时从某个地方获取节点上pod的期望状态(运行什么容器、运行的副本数量、网络或者存储如何配置等等) , 并调用对应的容器平台接口达到这个状态
定时汇报当前节点的状态给apiserver，以供调度的时候使用
 镜像和容器的清理工作;，保证节点上镜像不会占满磁盘空间，退出的容器不会占用太多资源

###### Kube-proxy服务

​	是K8S在每个节点上运行网络代理, service资源的载体
​		建立了pod网络和集群网络的关系( clusterip> podip )
​		常用三种流量调度模式：
​				Userspace (废弃)
​				Iptables (濒临废弃)
​				Ipvs(推荐)
​		 负责建立和删除包括更新调度规则、通知apiserver自己的更新,或者从apiserver哪里获取其他kube-proxy的调度规则变化来更新自己的	


4. ##### CLI客户端

   kubectl

5. ##### 核心附件

   CNI网络插件→ flannel/calico
   服务发现用插件→ coredns
   服务暴露用插件→ traefik
   GUI管理插件→ Dashboard