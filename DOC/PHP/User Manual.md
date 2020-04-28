﻿
> Contents

[toc]

## 1 How pinpoint-php agent works?

Pinpoint php agent employs [php_simple_aop](https://github.com/eeliu/php_simple_aop) as its aspect programming library, it helps converting origin class.php to proxied_class.php which includes plugins.php and origin.php without affecting any function of origin class.php.

``` php
+--------------+                    +-----------------------+
|  origin.php  |                    | origin.php            |
|              |                    | proxied_origin.php    |
+--------------+                    | require_origin.php    |
                                    | entry for plugins.php |
      ^                             +-----------------------+
      |
      |   Before                                   ^
      |                                            |   After
      |                                            |
      +----+    vender/class_loader        +-------+

```

## 1.1 Performance Result

> TPS loss and TPR Loss

![FlarumPerformanceTest](../images/FlarumPerformanceTest.png)

> TPS: Time per request 
> TPR: Requests per second

[How to use pinpoint-php into Flarum?](../../PHP/pinpoint_php_example/demo/Flarum-demo/Reademe.md)

>  Call Tree

![CallTree](../images/Flarum-callstack.png)

> Summary
* Less than 5% loss, when Flarum add PHP Agent.

If you care about the performance most, you can call pinpoint-php agent module API directly, which is written by C&C++. [(pinpoint-php api)](../../PHP/pinpoint_php_ext/pinpoint_php_api.php)

## 2 How to hook a object ?

```
use A\a as a;
class Foo{
      public function foo(): a
      {
            return new a::factory_create_new();
      }
}

```

> As foo returns a new object and this scenario can't be detected by php_simple_aop easily.

### 2.1 Use a decorator

Replace the return object with a decorated object in onEnd(). There are some [magic methods](https://www.php.net/manual/en/language.oop5.magic.php) to help "hacking" the object.

[ [How it works ☚]](../../PHP/pinpoint_php_example/Plugins/InstancePlugins.php)


### 2.2 Examples

#### 2.2.1 Hook a generator.

> https://github.com/naver/pinpoint-c-agent/issues/100

``` php
    ...
    function generator($start, $limit, $step=1){
        if($start > $limit){
            throw new LogicException("start cannot bigger that limit.");
        }
        usleep(120000);
        for($i = $start; $i<=$limit; $i += $step){
            try{
                yield $i;
            }catch (Exception $exception){
                echo $exception->getMessage();
            }
        }
    }
    ...
```
[ [Goto GeneratorPlugin ☚] ](../../PHP/pinpoint_php_example/Plugins/GeneratorPlugin.php)

#### 2.2.2 PDO::prepare return a PDOStatement

``` php
Reference： https://www.php.net/manual/zh/pdo.prepare.php
<?php

$sth = $dbh->prepare('SELECT name, colour, calories
    FROM fruit
    WHERE calories < ? AND colour = ?');
$sth->execute(array(150, 'red'));
$red = $sth->fetchAll();
$sth->execute(array(175, 'yellow'));
$yellow = $sth->fetchAll();
?>

```

Replace $dbh->prepare return value with [Plugins\PDOStatement](../../PHP/pinpoint_php_example/Plugins/PDOStatement.php).

