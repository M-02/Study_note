# select语句的应用

## select单独使用的情况

```mysql
-- select @@xxx 查看系统参数
SELECT @@port;
SELECT @@basedir;
SELECT @@datadir;
SELECT @@socket;
SELECT @@server_id;
SELECT @@innodb_flush_log_at_trx_commit;
```

```mysql
-- select 函数();
SELECT NOW();
SELECT DATABASE();
SELECT USER();
SELECT CONCAT("hello world");
SELECT CONCAT(USER,"@",HOST) FROM mysql.user;
SELECT GROUP_CONCAT(USER,"@",HOST) FROM mysql.user;
```

## select通用语法、执行顺序（单表）

```mysql
select 列
from 表
where  条件
group by 条件
having  条件
order by 条件
limit
```

## 单表子句-from

```undefined
SELECT 列1,列2 FROM 表
SELECT  *  FROM 表
```

例子:
 -- 查询stu中所有的数据(不要对大表进行操作)

```undefined
SELECT * FROM stu ;
```

-- 查询stu表中,学生姓名和入学时间

```undefined
SELECT sname , intime FROM stu;
```

### 单表子句-where

```undefined
SELECT 列,列 FROM 表 WHERE 过滤条件;
```

##### where配合等值查询

例子:
 -- 查询中国(CHN)所有城市信息

```bash
SELECT * FROM city WHERE countrycode='CHN';
```

-- 查询北京市的信息

```bash
SELECT * FROM city WHERE NAME='peking';
```

-- 查询甘肃省所有城市信息

```bash
SELECT * FROM city WHERE district='gansu';
```

##### where配合比较操作符(> < >= <= <>)

例子:
 -- 查询世界上少于100人的城市

```undefined
SELECT * FROM city WHERE population<100;
```

##### where配合逻辑运算符(and  or )

例子:
 -- 中国人口数量大于500w

```bash
SELECT * FROM city WHERE countrycode='CHN' AND population>5000000;
```

-- 中国或美国城市信息

```bash
SELECT * FROM city WHERE countrycode='CHN' OR countrycode='USA';
```

##### where配合like语句模糊查询

例子:
 -- 查询省的名字前面带guang开头的

```ruby
SELECT * FROM city WHERE district LIKE 'guang%';    
注意:不要出现类似于%CH%，前后都有百分号的语句，因为不走索引，性能极差
如果业务中有大量需求,我们用"ES""来替代
```

##### where配合in语句

-- 中国或美国城市信息

```csharp
SELECT * FROM city WHERE countrycode IN ('CHN' ,'USA');
```

##### where配合between and

例子:
 -- 查询世界上人口数量大于100w小于200w的城市信息

```undefined
SELECT * FROM city  WHERE population >1000000 AND population <2000000;
SELECT * FROM city  WHERE population BETWEEN 1000000 AND 2000000;
```

###  group by + 常用聚合函数

##### 作用

```csharp
根据 by后面的条件进行分组，方便统计，by后面跟一个列或多个列
```

##### 常用聚合函数

```swift
**max()**      ：最大值
**min()**      ：最小值
**avg()**      ：平均值
**sum()**      ：总和
**count()**    ：个数
group_concat() : 列转行
```

##### 例子：

例子1：统计世界上每个国家的总人口数.

```php
USE world
SELECT countrycode ,SUM(population)    FROM  city  GROUP BY countrycode;
```

例子2： 统计中国各个省的总人口数量(练习)

```bash
SELECT district,SUM(Population) FROM city  WHERE countrycode='chn' GROUP BY district;
```

例子3：统计世界上每个国家的城市数量(练习)

```objectivec
SELECT countrycode,COUNT(id)  FROM city GROUP BY countrycode;
```

### having

```csharp
where|group|having
```

例子4：统计中国每个省的总人口数，只打印总人口数小于100

```csharp
SELECT district,SUM(Population)
FROM city
WHERE countrycode='chn'
GROUP BY district
HAVING SUM(Population) < 1000000 ;
```

### order by + limit

#####  作用

```csharp
实现排序，by后添加条件列
```

#####  应用案例

1. 查看中国所有的城市，并按人口数进行排序(从大到小)

```bash
SELECT * FROM city WHERE countrycode='CHN' ORDER BY population DESC;
```

1. 统计中国各个省的总人口数量，按照总人口从大到小排序

```php
SELECT district AS 省 ,SUM(Population) AS 总人口
FROM city
WHERE countrycode='chn'
GROUP BY district
ORDER BY 总人口 DESC ;
```

1. 统计中国,每个省的总人口,找出总人口大于500w的,并按总人口从大到小排序,只显示前三名

```csharp
SELECT  district, SUM(population)  FROM  city 
WHERE countrycode='CHN'
GROUP BY district 
HAVING SUM(population)>5000000
ORDER BY SUM(population) DESC
LIMIT 3 ;

LIMIT N ,M --->跳过N,显示一共M行
LIMIT 5,5
LIMIT M,N:跳过M行,显示一共N行
LIMIT Y OFFSET X:跳过x行,显示一共Y行


SELECT  district, SUM(population)  FROM  city 
WHERE countrycode='CHN'
GROUP BY district 
HAVING SUM(population)>5000000
ORDER BY SUM(population) DESC
LIMIT 5,5;
```

### distinct：去重复

```cpp
SELECT countrycode FROM city ;
SELECT DISTINCT(countrycode) FROM city  ;
```

### 联合查询- union all

```csharp
-- 中国或美国城市信息

SELECT * FROM city 
WHERE countrycode IN ('CHN' ,'USA');

SELECT * FROM city WHERE countrycode='CHN'
UNION ALL
SELECT * FROM city WHERE countrycode='USA'

说明:一般情况下,我们会将 IN 或者 OR 语句 改写成 UNION ALL,来提高性能
UNION     去重复
UNION ALL 不去重复
```

### 多表连接查询（内连接）

#### 多表连接基本语法

最核心的是，找到多张表之间的关联条件列

列书写时，必须是：表名.列

将所有的过滤,分组,排序等条件按顺序写在on的后面

```mysql
SELECT
country.name,
country.SurfaceArea,
city.name,
city.Population
FROM city
JOIN country
ON city.CountryCode = country.code
WHERE city.population<100;
```

多张表

```mysql
A
JOIN B
ON A.x=B.y
JOIN C
ONB.m=C.n.
```

![image-20201120151602216](C:\Users\HAIRUI_H\AppData\Roaming\Typora\typora-user-images\image-20201120151602216.png)

### 别名应用

#### 表别名

表别名是可以全局调用的

```mysql
SELECT t. tname , GROUP_ CONCAT (CONCAT (st.sname,":",sc. score) )
EROM teacher as t
JOIN
course as C
ON t.tno =C. tno
JOIN sc
ON c.cno=sc.cno
JOIN student as st
ON sc.sno=st.sno
WHERE sc.score<60
GROUP BY t.tno
```

#### 列别名

列别名可以被having 和 order 调用

```mysql
SELECT t.tname as讲师名, GROUP_ CONCAT (CONCAT (st. sname, ":",sc. score))
as不及格的
FROM teacher as t
JOIN course as C
ON t.tno=c. tno
JOIN sc
ON c.cno=sc.cno
JOIN student as st
ON sc. sno=st.sno 
WHERE sc.score<60
GROUP BY t.tno
```

### group_ concat

列转行聚合函数

```mysql
select user,group_concat(host) from mysql.user group by user;
```

### concat

做列值拼接

```mysql
select concat(user,"@",host) from mysql.user;
```

### 关于多表连接语法规则

1.首先找涉及到的所有表
2.找到表和表之;间的关联列
3.关联条件写在on后面
A join   B   on  关联列
4.所有需要查询的信息放在select后
5.其他的过滤条件where   group by   having   order by   limit往最后放

注意:对多表连接中，驱动表选择数据行少的表。后续所有表的关联列尽量是主键或唯一键（表设计），至少建立一个索引。