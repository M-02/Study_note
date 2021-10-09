Linux 查看端口占用情况可以使用 lsof 和 netstat 命令，所以接下来简单介绍一下这两个命令的使用情况。
一、lsof语法：

```shell
lsof -i:端口号
如查看8080端口的占用情况：
lsof -i:8080
其他命令如下：
lsof -i:8080-----查看8080端口占用。
lsof abc.txt-----显示开启文件abc.txt的进程。
lsof -c abc-----显示abc进程现在打开的文件。
lsof -c -p 1234-----列出进程号为1234的进程所打开的文件。
lsof -g gid-----显示归属gid的进程情况。
lsof +d /usr/local/-----显示目录下被进程开启的文件。
lsof +D /usr/local/-----同上，但是会搜索目录下的目录，时间较长。
lsof -d 4-----显示使用fd为4的进程。
lsof -i -U-----显示所有打开的端口和UNIX domain文件。
```

二、netstat语法：

```shell
netstat -tunlp | grep 端口号-----查看某个端口的占用情况。
如，查看8080端口的占用情况：
netstat -tunlp | grep 8080
其他相关的参数如下：
-t (tcp) 仅显示tcp相关选项
-u (udp)仅显示udp相关选项
-n 拒绝显示别名，能显示数字的全部转化为数字
-l 仅列出在Listen(监听)的服务状态
-p 显示建立相关链接的程序名
```

三、介绍kill的命令。

```shell
kill -9 PID-----杀死进程号的进程。
kill -9 nginx-----杀死nginx服务的进行
```

### free命令

free命令默认是显示单位kb，free -m和free -g命令查看，分别表示MB和GB

top