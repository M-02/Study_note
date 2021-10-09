#### Git基础命令

```bash
1.git init 初始化代码库，把一个目录初始化为版本仓库（可以是空目录，也可以是带内容的目录）

2.git status 查看当前仓库的状态

3.git add [file] 添加文件到暂存区

4.git add * 添加当前所有改动过的文件到暂存区

5.git rm --cached 撤出工作区

6.git rm -f 同时删除工作目录和暂存区的内容

7.git commit -m "你的提交信息" 提交代码，从缓存区提交到本地仓库，-m提交信息

8.git mv old-filename new-filename 直接更改工作区与暂存区文件名称，更改完成直接提交即可

9.git diff 默认比对工作目录和暂存区有什么不同

10.git diff --cached 比对暂存区和本地仓库

11.git commit -am "你的提交信息"  如果某个文件已经被仓库管理，如果再次更改此文件，直接用此命令提交

12.git log 查看历史提交过的信息 git reflog 查看历史所有提交信息

13.git reset --hard 296e997   回滚数据到某一个提交

14.git log --oneline --decorate 查看当前指针的指向

15.git branch 查看分支

16.git branch testing 创建 一个测试分支

17.git checkout testing 切换到测试分支

18.git checkout -b testing 创建并切换到testing分支

19.git tag -a v1.0 -m "aaa bbb master tesing version v1.0" # - a指定标签名字-m指定说明文字

20.git tag -a v2.0 dbead4c -m "add bbb version v2.0" #指定某次的提交为标签   -d 删除标签  git tag -d v1.0

21.git show v1.0 #查看v1. 0的信息  git show 加标签查看

22.git reset --hard v2.0 # 直接还原数据到v2. 0

23.git remote add origin https://github.com/M-02/test.git     添加远程仓库,名称为origin

24.git remote  查看当前的远程仓库的名称

25.git clone 克隆代码

26.git push -u test master 推送代码到远程仓库
```





#### 小结:如何真正意义上通过版本控制系统管理文件

1.工作目录必须有个代码文件
2.通过 git add file
添加到暂存区域
3.通过 git comnit -m "你自己输入的信息"”添加到本地仓库

#### .git 隐藏文件介绍:

branches #分支目录
config #定义项目特有的配置选项
description #仅供git web程序使用
HEAD # 指示当前的分支
hooks # 包含git钩子文件
info # 包含一个全局排除文件( exclude文件)
objects # 存放所有数据内容，有info和pack两个子文件夹
refs # 存放指向数据(分支)的提交对象的指针
index # 保存暂存区信息,在执行git init的时候，这个文件还没有

