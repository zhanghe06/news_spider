# Spiders

1、部署系统依赖

- MariaDB
- Redis
- NodeJS

2、部署项目依赖

```
pip install requirements.txt
```

3、创建数据库, 建立抓取入口

- 建表结构 db/schema/mysql.sql
- 测试数据 db/data/mysql.sql

4、创建抓取任务, 写入缓存
```
(news_spider.env) ➜  news_spider git:(master) ✗ python tasks/job_put_tasks.py
[√] 当前环境变量: develop
缺失参数
Example:
	python job_put_tasks.py wx  # 微信
	python job_put_tasks.py wb  # 微博
	python job_put_tasks.py tt  # 头条
```
参考以上提示, 对应蜘蛛执行各自的脚本完成任务创建

5、微信抓取, 需要初始化cookie, 其他两个蜘蛛不需要


生成环境, 可以使用`supervisor`自动守护`scrapy.ini`、`tasks.ini`这两组进程, 根据需要自行修改
