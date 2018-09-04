# 整体架构(Architecture)

- MariaDB

每个公众号/发布号的首页（即爬虫抓取入口）存储于数据库中。

表结构 db/schema/mysql.sql

测试数据 db/data/mysql.sql


- Redis

为了支持分布式, 抓取任务单独存放于缓存, 这样在调试时, 需要手动执行创建任务。

参考[启动说明](Spiders/README.md)

为了方便调试, 本项目所有缓存key均以`scrapy:`作为前缀

- NodeJS

部分详情页面的信息抽取, 本项目使用js处理, 避免正则表达式规则的不完全覆盖。
