# 微博

进入redis, 检查任务数量
```
127.0.0.1:6379> SCARD "scrapy:tasks_set:weibo"
(integer) 0
```

如果没有任务, 需要创建抓取任务
```
python tasks/job_put_tasks.py wb
```

开启爬虫
```
scrapy crawl weibo
```
