## 新闻抓取

[![Build Status](https://travis-ci.org/zhanghe06/news_spider.svg?branch=master)](https://travis-ci.org/zhanghe06/news_spider)
[![Coverage Status](https://coveralls.io/repos/github/zhanghe06/news_spider/badge.svg?branch=master)](https://coveralls.io/github/zhanghe06/news_spider?branch=master)

### 项目演示

服务依赖:
- MariaDB
- Redis
- NodeJS

本项目依赖第三方验证码识别服务, 注册地址: http://www.ruokuai.com/

更新配置 config/develop.py 用户名和密码
```
RK_CONFIG = {
    'username': '******',
    'password': '******',
    'soft_id': '93676',
    'soft_key': '5d0e00b196c244cb9d8413809c62f9d5',
}
```

```bash
virtualenv news_spider.env          # 创建虚拟环境
source env_develop.sh               # 激活虚拟环境
pip install -r requirements.txt     # 安装环境依赖
# 开发环境 模拟单次抓取
python tasks/job_put_tasks.py wx    # 初次创建任务
python tasks/jobs_sogou.py          # 初次应对反爬
scrapy crawl weixin                 # 开启微信爬虫
# 生产环境 开启持续抓取
supervisord                         # 开启守护进程
supervisorctl start all             # 开启工作进程
```

- env_develop.sh   # 开发环境
- env_product.sh   # 生产环境

### 项目创建过程记录

项目依赖明细
```bash
pip install requests
pip install scrapy
pip install sqlalchemy
pip install MySQL-python
pip install sqlacodegen
pip install redis
pip install PyExecJS
pip install Pillow
pip install psutil
pip install apscheduler
pip install supervisor
pip install future  # 兼容py2、py3
```

Mac 系统环境依赖（mariadb）
```bash
brew unlink mariadb
brew install mariadb-connector-c
ln -s /usr/local/opt/mariadb-connector-c/bin/mariadb_config /usr/local/bin/mysql_config
pip install MySQL-python
rm /usr/local/bin/mysql_config
brew unlink mariadb-connector-c
brew link mariadb
```
安装 mysqlclient 同理

CentOS 系统环境依赖
```bash
yum install gcc
yum install mysql-devel
yum install python-devel
yum install epel-release
yum install redis
yum install nodejs
```

CentOS 安装 python3 环境（CentOS 默认是不带 python3 的）
```bash
yum install python34
yum install python34-devel
```


创建项目
```bash
scrapy startproject news .
scrapy genspider weixin mp.weixin.qq.com
```

启动蜘蛛
```bash
scrapy crawl weixin
```

如需测试微博, 修改以下方法, 更改正确用户名和密码

tools/weibo.py
```
def get_login_data():
    return {
        'username': '******',
        'password': '******'
    }
```

### 蜘蛛调试（以微博为例）
1. 清除中间件去重缓存, 重置调试任务
```
127.0.0.1:6379> DEL "dup:weibo:0"
(integer) 1
127.0.0.1:6379> DEL "scrapy:tasks_set:weibo"
(integer) 1
127.0.0.1:6379> SADD "scrapy:tasks_set:weibo" 130
(integer) 1
127.0.0.1:6379>
```
2. 清除调试蜘蛛存储数据
```mysql
DELETE FROM fetch_result WHERE platform_id=2;
```
3. 启动调试蜘蛛
```bash
scrapy crawl weibo
```


### 验证码识别

http://www.ruokuai.com/

http://wiki.ruokuai.com/

价格类型:
http://www.ruokuai.com/home/pricetype


### 项目说明

亮点:

1. 支持分布式, 每个蜘蛛抓取进程对应一个独立的抓取任务
2. 采用订阅发布模型的观察者模式, 处理并发场景的验证码识别任务, 避免无效的识别

备注: `mysql`中`text`最大长度为65,535(2的16次方–1)

类型 | 表达式 | 最大字节长度（bytes） | 大致容量
---: | ---: | ---: | ---:
TinyText | 2的8次方–1 | 255 | 255B
Text | 2的16次方–1 | 65,535 | 64KB
MediumText | 2的24次方–1 | 16,777,215 | 16MB
LongText | 2的32次方–1 | 4,294,967,295 | 4GB

由于微信公众号文章标签过多, 长度超过`Text`的最大值, 故建议采用`MediumText`
