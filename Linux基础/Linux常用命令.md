1. ```shell
   ip address show /ip a   检查网卡地址配置
   ```

   

2. ```shell
   ping                   测试网络连通性
   ```

   

3. ```shell
   nmtui                  图形界面修改网卡地址信息
   ```

   

4. ```shell
   exit                   注销
   ```

   

05. ```shell
    shutdown               关机命令
	shutdown -h 5          指定关机时间 （推荐）
	shutdown -r 5          重启主机时间 （推荐）
	shutdown -c            取消关机或重启计划
    shutdown -h now/0      立即关机
	shutdown -r now/0      立即重启	
	halt                   直接关机
	poweroff               直接关机 
reboot                 直接重启
    ```
    
    
    
06. ```shell
	list=ls                查看文件或目录是否存在
	ls 文件或目录路径信息
	ls -d 目录信息
	ls -l 文件或目录信息    查看数据的属性信息
	ls -la 目录信息        查看目录中隐藏文件
    ls -lt 目录信息        将目录中的信息按照时间进行排序显示   
    ls -ltr 目录信息       按照时间信息,进行反向排序
	ls -lh	数据信息       显示的数据信息大小,以人类可读方式显示
	```
	
	
	
07. ```shell
    make directory=mkdir   创建目录
	mkdir -p 多级目录       创建多级目录/忽略错误提示
	```
	
	
	
08. ```shell
    manual=man             查看命令手册信息
    man 查看的命令
    NAME     命令作用说明
	   mkdir - make directories
    SYNOPSIS 命令使用方法
	   mkdir [OPTION]... DIRECTORY...
    DESCRIPTION 命令的参数解释
       -p, --parents
	          no error if existing, make parent directories as needed
	```
```
    
09. change directory==cd   切换目录命令
	cd /xxx   绝对
	cd xxx    相对
	cd ..     上一级
	cd ../../ 上多级
	cd -      返回上一次所在路径
	cd/cd ~   返回到用户家目录
```


​	
10. ```shell
    vi                   编辑文件内容
	vi 文件信息
	i   --- 进入编辑模式
	esc --- 退出编辑模式
	:wq --- 保存并退出
	:w
	:q
	:wq!--- 强制保存退出
	:q! --- 强制退出
	
	命令模式-->插入模式
	i   --- 表示从光标所在位置进入编辑状态    
	I   --- 表示将光标移动到一行的行首，再进入编辑状态
	o   --- 在光标所在行的下面，新起一行进行编辑
	O   --- 在光变所在行的上面，新起一行进行编辑
	a   --- 将光标移动到右边的下一个字符，进行编辑
	A   --- 将光标移动到一行的行尾，进入到编辑状态
	C   --- 将光标到行尾内容进行删除，并进入编辑状态
	cc  --- 将整行内容进行删除并进入编辑状态
	总结：移动光标位置，并进入编辑状态方法
	
	只移动光标，不进入编辑状态
	大写字母G   将光标快速切换尾部
	小写字母gg  将光标快速切换首部
	ngg         n表示移动到第几行
	$           将光标移动到一行的结尾
	0/^         将光标移动到一行的行首
	
	命令模式--底行模式
	:           输入一些命令
	/           进入搜索状态(向下搜索 n依次向下)
	?           进入搜索状态(向上搜索 n依次向上)
	
	
	特殊使用技巧:
	将一行内容进行删除(剪切)   	deletedelete=dd
	将多行内容进行删除(剪切)   	3dd
    将内容进行粘贴                 	p
    粘贴多次内容                   	3p
    复制一行内容                   yy
	复制多行内容                   3yy	
	操作错误如何还原     	       小写字母u  undo
	```
	
	
	
11. ```shell
    echo                将信息输出到屏幕上
	echo "你好 世界"
	```
	
	
	
12. ```shell
    cat                 查看文件内容信息
cat -n 文件信息     显示文件内容行号信息
    ```
    
    
    
13. ```shell
    cp                  复制文件或目录数据到其他目录中
    cp -r               递归复制目录数据
	\cp                 强行覆盖数据
	```
	
	
	
14. ```shell
    rm                  删除数据命令
	rm -r               递归删除数据
\rm -f               强制删除数据,不需要进行确认
    ```
    
    
    
15. ```shell
    mv                  移动剪切数据信息
    ```

    

16. ```bash
    mount               对存储设备进行挂载
	mount 存储设备文件  挂载点
	umount              对存储设备进行卸载
umount 挂载点
    ```
    
    
    
17. ```shell
    hostname            查看修改主机名称
    ```

    

18. ```shell
    hostnamectl         直接修改主机名称（centos7）
	hostnamectl set-hostname 主机名称
	```
	
	
	
19. ```shell
    df                  查看磁盘挂载情况/查看磁盘使用情况
df -h               以人类可读方式查看磁盘使用情况
    ```
    
    
    
20. ```shell
    source              立即加载文件配置信息 
	                    /etc/profile
						/etc/bashrc
						~/.bashrc 
						~/.bash_profile
						/etc/sysconfig/i18n  --- centos6字符集配置文件
						/etc/locale.conf     --- centos7字符集配置文件
	```
	
	
	
21. ```shell
    which               显示命令文件所在路径位置
    which 命令
    ```
    
    
    
22. ```shell
    export              定义环境变量
	export 环境变量=xxx
	```
	
	
	
23. ```shell
    alias               设置系统别名命令
alias 别名='命令信息'
    ```
    
    
    
24. ```shell
    unalias             取消系统别名命令
unalias 别名 
    ```
    
    
    
25. ```shell
    head                查看文件前几行内容(默认前10行)
head -5             查看前5行
    ```
    
    
    
26. ```shell
    tail                查看文件后几行内容(默认后10行)
	tail -5             查看后5行
	tail -f             一直追踪一个文件内容变化
	```
	
	
	
27. ```shell
    yum                 下载并安装软件命令
	yum install -y 名称 			直接安装软件
	yum groupinstall -y 包组名称   	直接安装软件包组
	yum repolist        			查看yum源信息
	yum list            			查看哪些软件可以安装/查看所有系统已安装的软件
	yum grouplist       			查看哪些软件包组可以安装/查看所有系统已安装的软件包组
	yum --help                      help参数可以只显示命令的参数帮助信息
yum provides locate             获取命令属于哪个软件大礼包
	
	
	```
	
	
	
28. ```shell
    ps                  查看系统进程信息
	ps -ef              查看所有详细的进程信息
	```
	
	
	
29. ```shell
    kill                删除指定进程
	kill pid            删除指定pid号码的进程
	kill -9 pid         强制删除指定pid号码的进程
	```
	
	
	
30. ```shell
    free                查看内存命令
free -h             人类可读方式查看
    ```
    
    
    
31. ```shell
    lscpu               查看CPU信息
    ```

    

32. ```shell
    w                   查看负载信息/查看系统用户登录信息	
    ```

    

33. ```shell
    useradd             创建用户(用户管理)
	useradd 用户名	
	```
	
	
	
34. ```shell
    passwd             	设置用户密码命令
	passwd 用户名      	指定修改哪个用户的密码
	passwd             	修改当前用户密码
	```
	
	
	
35. ```shell
    su                  切换用户命令
	su - 用户名称 
	```
	
	
	
36. ```shell
    id                  检查创建的用户是否存在
	id  用户名
	```
	
	
	
37. ```shell
    whoami              确认用户身份
    ```

    

38. ```shell
    rpm                 管理软件程序包的
	rpm -qa 软件名称   	查看软件大礼包是否安装成功
    rpm -ql 软件名称   	查看软件大礼包中都有什么
rpm -qf 文件名称(绝对路径)   查看文件属于哪个软件大礼包
    rpm -hvi 文件名称    安装软件
    ```
    
    
    
39. ```shell
    systemctl           管理服务程序的运行状态
	systemctl start 	服务名称  	--- 启动服务
	systemctl stop 		服务名称  	--- 停止服务
	systemctl restart 	服务名称 	--- 重启服务
	systemctl status 	服务名称  	--- 查看服务详细的运行状态
	systemctl disable   服务名称  	--- 让服务开机不要运行
	systemctl enable   	服务名称  	--- 让服务开机运行
	systemctl is-active   服务名称 	--- 检查确认服务是否运行
	systemctl is-enabled  服务名称 	--- 检查确认服务是否开机运行
	```
	
	
	
40. ```shell
    localectl set-locale LANG=zh_CN.UTF-8   --- centos7修改字符集信息
    ```

    

41. ```shell
    less/more           逐行或逐页查看文件信息内容
    ```

    

42. ```shell
    whereis             查看命令所在路径以及命令相关手册文件所在路径
    ```

    

43. ```shell
    locate              查看文件所在路径信息
	updatedb            更新文件所在路径的索引数据库表
	```
	
	
	
44. ```shell
    file                查看文件的类型
	file 文件信息
	```
	
	
	
45. ```shell
    stat                查看数据详细属性信息
	stat file.txt       看到文件的三个时间信息
	```
	
	
	
46. ```shell
    tar                 压缩数据命令
	-z           压缩类型
	-c           创建压缩包
	-v           显示过程
	-f           指定压缩文件路径
	-x           解压文件
	-t           查看压缩文件内容
	--exclude        排除指定文件不被压缩处理
	--exclude-from
	```
	
	
	
47. ```shell
    xargs               分组命令 按照分组显示
xargs -n1 <文件 
    
    总结: <
    tr xxx <
	xargs <
	```
	
	​	
	
48. ```shell
    tree                显示目录结构树
    tree -L 1           查看下几级目录机构
	tree -d             目录结构中目录信息
	```
	
	
	
49. ```shell
    date                查看时间信息和修改时间信息
	date "+%F_%T"
	date -s             设置系统时间 
date -d             显示未来或过去的时间信息
    ```
    
    
    
50. ```shell
    ln                  创建链接文件
	ln 源文件 链接文件 创建硬链接
	ln -s               创建软链接
	```
	
	
	
51. ```shell
    wc                  统计命令
	wc -l               统计有多少行
	```
	
	
	
52. ```shell
    chmod               修改文件目录数据权限信息
	chmod u/g/o 
	chmod a 
	```
	
	
	
53. ```shell
    useradd             创建用户命令
	-s /sbin/nologin    指定用户shell登录方式
	-M                  不创建家目录
	-u                  指定用户uid信息
	-g                  指定用户所属主要组信息
	-G                  指定用户所属附属组信息
-c                  指定用户注释信息
    ```
    
    
    
54. ```shell
    usermod             修改用户信息
	-s /sbin/nologin    指定用户shell登录方式
	-u                  指定用户uid信息
	-g                  指定用户所属主要组信息
	-G                  指定用户所属附属组信息
	-c                  指定用户注释信息   
	```
	
	
	
55. ```shell
    userdel             删除用户信息
	userdel -r          彻底删除用户和家目录信息
	```
	
	
	
56. ```shell
    groupadd            创建用户组 
	groupmod            修改用户组
	groupdel            删除用户组
	```
	
	
	
57. ```shell
    chown               修改用户属主和属组的信息
	chown -R            递归修改用户属主和属组信息
	```
	
	
	
58. ```shell
    sort                排序命令
	sort -n             按照数值进行排序
	sort -k1            按照指定列进行排序
	```
	
	
	
59. ```shell
    dd                  模拟创建出指定大小的文件
	dd if=/dev/zero of=/tmp/oldboy.txt  bs=10M                    count=100
	    从哪取出数据  放到哪          占用1个block多少空间     总共使用多少个block
	```
	
	
	
60. ```shell
    du                  查看目录的大小
du -sh              汇总查看目录大小,以人类可读方式
	```
	
	

高级命令：4剑客
00. ```shell
    老四 find       查询文件所在路径
	find /oldboy -type 文件类型 -name "文件名称"
	find /oldboy -type f -mtime +10 -delete   --- 删除历史数据信息
	find /oldboy -type f -size  +10 -delete   --- 删除大于10k文件
	-maxdepth       查找目录层级的深度
	-inum           根据文件inode信息查找
    -exec           对查找出的数据进行相应处理
	-perm           根据权限查找数据信息
      -iname          忽略名称大小写
	
	
	```
	
	
	
01. ```shell
    老三 grep 文件  对信息进行过滤筛选
    grep -B n       显示指定信息前几行内容
    grep -A n       显示指定信息后几行内容
	grep -C n       显示指定信息前后几行内容
	grep -c         显示指定信息在文件中有多少行出现
	grep -v         进行取反或者排除
	grep -E/egrep   识别扩展正则符号
	grep -o         显示过滤过程信息
	grep -n         过滤信息并显示信息行号
	grep -i         过滤信息忽略大小写
	```
	
	```shell
	老二 sed
	
	老大 awk
	```
	
	



系统中的常见环境变量
1. ```shell
   1.  PATH                方便命令的使用
   
   2.  PS1                 定义提示符的信息或格式
   ```

   

快捷方式：
1. ```shell
   1. ctrl+c             	中断命令执行操作过程
   2. ctrl+l             	清屏操作
   3. ctrl+d             	注销功能
   4. tab               	补全快捷键 补全目录路径或文件名称信息/命令   
   5. 方向键上下         	调取之前输入过的历史命令
   6. ctrl+a              快速将光标移动到行首 a b c d
   7. ctrl+e              快速将光标移动到行尾
   8. ctrl+左右方向键    	按照一个英文单词进行移动光标
   9. esc+.               将上一个命令最后一个信息进行调取
   10. ctrl+u     			将光标所在位置到行首内容进行删除（剪切）
   11. ctrl+k     			将光标所在位置到行尾内容进行删除（剪切）
   12. ctrl+y     			粘贴剪切的内容
   13. ctrl+s     			xshell进入到了锁定状态 suo锁
   14. ctrl+q     			解除锁定状态           quit推出锁定状态
   15. ctrl+r              快速搜索历史命令					
   ```

   ​	

系统特殊符号

```shell
~                           家目录符号
..                          上一级目录"
.                           当前目录"""                          标准输出重定向符号

> >                            标准输出追加重定向符号
2>                         错误输出重定向符号
2>>                        错误输出追加重定向符号
<                          标准输入重定向符号
<<                         标准输入追加重定向符号

&&                         代表前一个命令执行成功后，再执行后面的命令
;                          代表前一个命令执行之后,再执行后面的命令
#                          代表将配置文件信息进行注释
                           在命令提示符中表示超级管理员身份
$                          用于加载读取变量信息
                           表示一行的结尾
						   在命令提示符中表示普通用户身份
!                          强制
``反引号                   将引号中命令执行结果交给引号外面的命令进行处理
| 管道符号                 将前一个命令的结果交给管道后面命令进行处理
{} 序列符号(通配符)        通配符号,显示数字或字母的序列信息   
```

​                     



11. 系统中不是所有命令都可以对文件进行编辑修改
    
    ```shell
    vim 文件  
    
    sed -i 文件  
    
    cat >> 
    
    echo >>
    ```
    
     