HttpServletRequest常用方法

```java
getParameter(String name)		获取请求中的参数，该参数是由name指定的
getParameterValues(String name)	返回请求中的参数值，该参数值是由name指定的
getRealPath(String path)		获取Web资源目录
gettribute(String name)			返回name指定的属性值
getAttributeNames()				返回当前请求的所有属性的名字集合
getCookies()					返回客户端发送的Cookie
getSession()					获取session回话对象
getInputStream)					获取请求主题的输入流
getReader()						获取请求主体的数据流
getMethod()						获取发送请求的方式，如GET、POST
getParameterNames()				获取请求中所有参数的名称
getRemoteAddr()					获取客户端的IP地址
getRemoteHost()					获取客户端名称
getServerPath(					获取请求的文件的路径
```

HttpServletResponse常用方法

```java
getWriter()							获取响应打印流对象
getOutputStream()					获取响应流对象
addCookie(Cookie cookie)			将指定的Cookie加入到当前的响应中
addHeader(String name ,String value)将指定的名字和值加入到响应的头信息中
sendError(int sc)					使用指定状态码发送一个错误到客户端
sendRedirect(String location)		发送一个临时的响应到客户端:
setDateHeader(String name ,long date)将给出的名字和日期设置响应的头部
setHeader(String name, String value)将给出的名字和值设置响应的头部
setStatus(int sc)给					当前响应设置状态码
setContentType(String ContentType)	设置响应的MIME类型
```

## 必备知识点:

简要理解JAVAWEB项目组成
代码方面，框架方面，中间件容器方面等
简要理解JAVAWEB执行流程
参考下图及
https://www.cnb1ogs.com/1987721594zy/p/9186584.htm1
https://blog.cadn.net/weily11/article/detai1s/80643472
com:
公司项目，copyright由项目发起的公司所有
包名为com.公司名.项目名.模块名. ...
持久层: dao、persist、mapper
实体类: entity、 model、 bean、javabean、 pojo
业务逻辑: service、 biz
控制器: controller、 servlet、 action、 web
过滤器: filter
异常: exception
监听器: listener
在不同的框架下一般包的命名规则不同，但大概如上，不同功能的Java 文件放在不同的包中，根据Java文件的功能统一安放及命名。

#审计思路:
根据业务功能审计优点:
明确程序的架构以及业务逻辑;明确数据流向，
可以从获取参数-->表现层->业务层- - >持久层，通读源码;
缺点:耗费时间;
根据敏感函数审计优点:
可以快速高效的挖出想要的漏洞，判断敏感函数上下文，追踪参数源头;
缺点:覆盖不了逻辑漏洞，不了解程序的基本框架;

审计开始前:
1、确定框架;
通过以下三种方式确定框架:
web.xml
看导入的jar包或pom. xml
看配置文件
`Struts2`配置文件: struts.xml
`Spring`配置文件: applicationContext.xml
`Spring MVC`配置文件:spring- mvc.xml
`Hibernate`配置文件: Hibernate.cfg.xml
`Mybaits`配置文件: mybatis -config.xml

2、查看是否存在拦截器
通过查看web.xml文件，确定是否配置相关拦截器。







https://www.cnblogs.com/csnd/p/11807776.html
https://blog.csdn.net/x62982/article/details/88392968
https://blog.csdn.net/weily11/article/details/80643472
https://www.cnblogs.com/kingsonfu/p/12419817.html
https://www.cnblogs.com/1987721594zy/p/9186584.html
https://pan.baidu.com/s/1miETaZcez30jmUEA5n2EWw提: xiao

