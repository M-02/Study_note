4)Shell特殊位置变量
$0 代表了脚本的名称如果全路径执行则脚本名称带全路径
使用方法给用户提示

```
echo $ "Usage: $0 { start | stop | status | restart |reload | force -reload} "
```

了解只获取脚本名称

```
[root@web01 scripts] # basename test. sh
test. sh
[root@web01 scripts]# basename / server / scripts/test. sh
test. sh
```

$n 脚本的第n个参数0被脚本名称占用从1开始$1 $2 $9后 面的参数需要加{}
$# 获取脚本传参的总个数
控制脚本的传参的个数 [$#-ne2] && echo "请输入两个参数"
&& exit
$  获取脚本所有的参数不加引号和$@相同加_上双引号则把参数视为一个参数$1$2$2
$@ 获取脚本所有的参数不加双引号和$*相同，加_上双引号则吧参数是为独立的参数$1 $2 $3  $*和$@在脚本中相同在循环体内不同_

$? 获取_上一条命令的返回结果0为成功非0失败

可指定返回结果[$#-ne2]&&echo"请输入两个参数"&&exit50
$$ 获取脚本的PID
echo $$ > / tmp/nginx_ log.pid
$! 获取.上一个在后台运行脚本的PID调试使用
$_ 获取命令行最后一个参数相当于EsC.

1.1) 数学比较运算
运算符解释

```
-eq		等于
-gt 		大于
-lt 		小于
-ge		大于或等于
-le		小于或等于
-ne		不等于
```

