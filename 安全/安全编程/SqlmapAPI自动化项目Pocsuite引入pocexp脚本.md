## 本课知识点:

Request爬虫技术，Sqlmap深入分析，Pocsuite分析， 框架代码二次修改等

## 本课目的:

掌握安全工具的API接口开发利用，掌握优秀框架的二次开发插件引用等

## SqlmapAPI调用实现自动化SQL注入安全检测

参考: https://www.freebuf.com/articles/web/204875.html
前期通过信息收集拿到大量的URL地址，这个时候可以配合Sq1mapAP I接口进行批量的SQL注入检测,开发当前项目过程: (利用sqlmapapi接口实现批量URL注入安全检测)

启动sqlmapapi

```
 sqlmapapi -s
```

1.创建新任务记录任务ID

```
@get ("/task/new")
```

2.设置任务ID扫描信息

```
@post ("/option/<taskid>/set")
```

3.开始扫描对应I D任务

```
@post ("/scan/<taskid>/start")
```

4.读取扫描状态判断结果

```
@get ("/scan/<taskid>/status")
```

4.如果结束删除I D并获取结果

```
@get ("/task/<taskid>/delete")
```

5.扫描结果查看

```
@get ("/scan/<taskid>/data")
```

## Pocsuite3漏扫框架二次开发POC/ EXP引入使用

参考: https://www.freebuf.com/articles/people/162868.html
开发当前项目过程: (利用已知框架增加弓 |入最新或内部的EX P进行安全检测)
1.熟悉Pocsuite 3项目使用及介绍
2.熟悉使用命令及代码文件对应情况
3.选取Glassfi sh漏洞进行编写测试
4.参考自带漏洞模版代码模仿写法测试

```
python cli.py -u X.X.X.X -r Glassfish.py --verify
```

