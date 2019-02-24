# 头条(M端)

创建任务详情
```mysql
INSERT INTO `fetch_task` VALUES (134, 3, 0, '55982516338', '奇文志怪', '', 'http://m.toutiao.com/profile/55982516338/', 1, '', '2018-09-06 14:01:05', '2018-09-06 14:01:05');
```

进入redis, 检查调度任务数量
```
127.0.0.1:6379> SCARD "scrapy:tasks_set:toutiao_m"
(integer) 439
```

如果没有调度任务, 需要创建调度任务
```
python tasks/job_put_tasks.py tm
```

开启爬虫
```
scrapy crawl toutiao_m
```
