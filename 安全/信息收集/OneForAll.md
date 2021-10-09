安装：

```
1、复制到本地安装包
git clone https://gitee.com/shmilylty/OneForAll.git
2、安装依赖
cd OneForAll
pip3 install -r requirements.txt -i
https://mirrors.aliyun.com/pypi/simple/
3、查看帮助
cd oneforall
python3 oneforall.py --help
4、更新
git fetch --all
git reset --hard origin/master
git pull
三、命令
cd oneforall
python3 oneforall.py --target XXX.com run
结果会自动保存在/root/OneForAll/oneforall/results/里面
```

使用：

```
 python3 oneforall.py --target daishen.ltd run
 python3 oneforall.py --target ./域名集合.txt run
```

sublist3r\云悉\layer子域名挖掘机\御剑子域名扫描



目录扫描
工具: dirsearch
功能:目录扫描(基于字典)
用法: https://github.com/maurosoria/dirsearch

```
python dirsearch.py -u https://www.baidu.com
```

