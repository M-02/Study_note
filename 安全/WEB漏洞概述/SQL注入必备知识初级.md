# SQL注入必备知识初级

- ### 首先SQL语句对大小写不敏感，这也导致了后台程序对大小写的检测失效。

 

- ### SQL 注释语句 ("--"与"/*...*/")

```
（1）--：表示单行注释

（2）/*…*/：用于多行（块）注释
```

 

- ### SELECT 查询语句

SQL SELECT 语法

> ```html
> SELECT 列名称 FROM 表名称
> SELECT * FROM 表名称
> ```

 

- ### UNION 操作符

UNION 操作符用于合并两个或多个 SELECT 语句的结果集。

请注意，UNION 内部的 SELECT 语句必须拥有相同数量的列。列也必须拥有相似的数据类型。同时，每条 SELECT 语句中的列的顺序必须相同。

SQL UNION 语法

> ```html
> SELECT column_name(s) FROM table_name1
> UNION
> SELECT column_name(s) FROM table_name2
> ```

注释：默认地，UNION 操作符选取不同的值。如果允许重复的值，请使用 UNION ALL。

 

- ### concat()

CONCAT 函数用于将两个字符串连接为一个字符串

1、语法及使用特点：

```
CONCAT(str1,str2,…) 
```

返回结果为连接参数产生的字符串。如有任何一个参数为NULL ，则返回值为 NULL。可以有一个或多个参数。

2、使用示例：

```
SELECT CONCAT(id, ‘，’, name) AS con FROM info LIMIT 1;
```

 

- ### concat_ws()

使用函数CONCAT_WS（）。

使用语法为：

```
CONCAT_WS(separator,str1,str2,…)
```

CONCAT_WS() 代表 CONCAT With Separator ，是CONCAT()的特殊形式。第一个参数是其它参数的分隔符。分隔符的位置放在要连接的两个字符串之间。分隔符可以是一个字符串，也可以是其它参数。如果分隔符为 NULL，则结果为 NULL。函数会忽略任何分隔符参数后的 NULL 值。但是CONCAT_WS()不会忽略任何空字符串。 (然而会忽略所有的 NULL）。

如

```
SELECT CONCAT_WS('_',id,name) AS con_ws FROM info LIMIT 1;
```

 

- ### group_concat()

GROUP_CONCAT函数返回一个字符串结果，该结果由分组中的值连接组合而成。
使用表info作为示例，其中语句SELECT locus,id,journal FROM info WHERE locus IN('AB086827','AF040764');的返回结果为

```
+----------+----+--------------------------+
| locus    | id | journal                  |
+----------+----+--------------------------+
| AB086827 |  1 | Unpublished              |
| AB086827 |  2 | Submitted (20-JUN-2002)  |
| AF040764 | 23 | Unpublished              |
| AF040764 | 24 | Submitted (31-DEC-1997)  |
+----------+----+--------------------------+
```

 

1、使用语法及特点：

```
GROUP_CONCAT([DISTINCT] expr [,expr ...]
[ORDER BY {unsigned_integer | col_name | formula} [ASC | DESC] [,col ...]]
[SEPARATOR str_val])
```

在 MySQL 中，你可以得到表达式结合体的连结值。通过使用 DISTINCT 可以排除重复值。如果希望对结果中的值进行排序，可以使用 ORDER BY 子句。
SEPARATOR 是一个字符串值，它被用于插入到结果值中。缺省为一个逗号 (",")，可以通过指定 SEPARATOR "" 完全地移除这个分隔符。
可以通过变量 group_concat_max_len 设置一个最大的长度。在运行时执行的句法如下：

```
 SET [SESSION | GLOBAL] group_concat_max_len = unsigned_integer;
```

如果最大长度被设置，结果值被剪切到这个最大长度。如果分组的字符过长，可以对系统参数进行设置：SET @@global.group_concat_max_len=40000;

2、使用示例：
语句 

```
SELECT locus,GROUP_CONCAT(id) FROM info WHERE locus IN('AB086827','AF040764') GROUP BY locus;
```

的返回结果为

```
+----------+------------------+
| locus    | GROUP_CONCAT(id) |
+----------+------------------+
| AB086827 | 1,2              |
| AF040764 | 23,24            |
+----------+------------------+
```

语句

```
 SELECT locus,GROUP_CONCAT(distinct id ORDER BY id DESC SEPARATOR '_') FROM info WHERE locus IN('AB086827','AF040764') GROUP BY locus;
```

的返回结果为

```
+----------+----------------------------------------------------------+
| locus    | GROUP_CONCAT(distinct id ORDER BY id DESC SEPARATOR '_') |
+----------+----------------------------------------------------------+
| AB086827 | 2_1                                                      |
| AF040764 | 24_23                                                    |
+----------+----------------------------------------------------------+
```

 

- ### order by

ORDER BY 语句用于根据指定的列对结果集进行排序。

ORDER BY 语句默认按照升序对记录进行排序。

如果您希望按照降序对记录进行排序，可以使用 DESC 关键字。

实例：以（逆）字母顺序显示公司名称

> ```html
> SELECT Company, OrderNumber FROM Orders ORDER BY Company （DESC）
> ```

 

- ### group by

GROUP BY 语句用于结合合计函数，根据一个或多个列对结果集进行分组。

SQL GROUP BY 语法

> ```html
> SELECT column_name, aggregate_function(column_name) 
> FROM table_name 
> WHERE column_name operator value 
> GROUP BY column_name
> ```

 

- 对XML文档进行查询和修改的函数extractvalue() 和 updatexml()

> ```
> > EXTRACTVALUE(XML_document, XPath_string);
> >
> > UPDATEXML(XML_document, XPath_string, new_value);
> 
> ```

- ### if()

语法：IF(expr1,expr2,expr3)

其中，expr1是判断条件，expr2和expr3是符合expr1的自定义的返回结果。

例如：

> ```
> select
> if(il.status_id = 'INV_STTS_AVAILABLE','全新','二手') as status_id
> from inventory_location as il;
> ```

- ### sleep()

执行select sleep(N)可以让此语句运行N秒钟

 

- ### left()

LEFT(str,len)

返回最左边的n个字符的字符串str，或NULL如果任何参数是NULL。

> ```html
> SELECT LEFT('foobarbar', 5);
> ```

 

- ### count()

COUNT(column_name) 语法

COUNT(column_name) 函数返回指定列的值的数目（NULL 不计入）：

> ```html
> SELECT COUNT(column_name) FROM table_name
> ```

SQL COUNT(*) 语法

COUNT(*) 函数返回表中的记录数：

> ```html
> SELECT COUNT(*) FROM table_name
> ```

SQL COUNT(DISTINCT column_name) 语法

COUNT(DISTINCT column_name) 函数返回指定列的不同值的数目：

> ```html
> SELECT COUNT(DISTINCT column_name) FROM table_name
> ```

注释：COUNT(DISTINCT) 适用于 ORACLE 和 Microsoft SQL Server，但是无法用于 Microsoft Access。

 

- ### floor()

FLOOR() - 返回最大整数，使这个整数小于或等于指定数的数值运算。

- ### round()

 ROUND() – 四舍五入一个正数或者负数，结果为一定长度的值。

- ### rand()

SQL 有一个 **RAND** 函数，用于产生 0 至 1 之间的随机数

- ### length()

返回字符串的长度，以字节为单位

语法：

> LENGTH(*string*)

- ### extract()

EXTRACT() 函数用于返回日期/时间的单独部分，比如年、月、日、小时、分钟等等。

> ```html
> EXTRACT(unit FROM date)
> ```

*date* 参数是合法的日期表达式。*unit* 参数可以是下列的值：

> | Unit 值            |
> | :----------------- |
> | MICROSECOND        |
> | SECOND             |
> | MINUTE             |
> | HOUR               |
> | DAY                |
> | WEEK               |
> | MONTH              |
> | QUARTER            |
> | YEAR               |
> | SECOND_MICROSECOND |
> | MINUTE_MICROSECOND |
> | MINUTE_SECOND      |
> | HOUR_MICROSECOND   |
> | HOUR_SECOND        |
> | HOUR_MINUTE        |
> | DAY_MICROSECOND    |
> | DAY_SECOND         |
> | DAY_MINUTE         |
> | DAY_HOUR           |
> | YEAR_MONTH         |

 