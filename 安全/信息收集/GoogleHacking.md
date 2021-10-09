# GoogleHacking字符

+符号，and连接符，相当于与运算，举例 丑小鸭+ed2k

|符号，or连接符，相当于或运算，举例 苹果|橘子|梨子

-符号，not连接符，相当于非运算，举例 电影 -香港

*符号，通配符

. 符号,通配符，占一位

“ ” 精确匹配

@ 用于社交平台

.. 数字范围，例如  1..100

# GoogleHacking关键字

site: 指定域名搜索的相关内容    例如 site:zhihu.com 哈哈哈

intitle:搜索标题中存在特定关键词的网页  例如：intitle:哈哈哈

inurl:搜索URL中存在特定关键词的网页  例如：inurl:哈哈哈

intext:搜索正文中存在特定关键词的网页  例如：intext:哈哈哈

filetype：文件类型 例如：filetype:pdf 网络安全

link:显示链接到指定地址的网页内容 例如：link:www.baidu.com

cache:显示网站缓存的 例如：cache:baidu.com

# GoogleHaching综合应用

用以下命令查后台和敏感信息：

site:www.****.com intext:管理|后台|登陆|用户名|密码|验证码|系统|帐号|manage|admin|login|system


site:www.*****.com inurl:login|admin|manage|manager|admin_login|login_admin|system


site:www.***.com intitle:管理|后台|登陆|


site:www.****.com intext:验证码

inurl:/admin/login.php 登录

intitle:管理 inurl:admin

inurl:file_upload 文件上传

inurl:editer  编辑区

intitle:index.of" parent directory"  支持遍历目录

intext:Powered by Discuz 查找基于Powered by Discuz的论坛

filetype:log username putty   查找关于putty的username日志

inurl:/jmx-console/htmladaptor  查找Jboss漏洞站

inurl:wp-login.php 查找wordpress登录页面

