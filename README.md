## 项目说明

项目演示

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
# 模拟单次抓取任务
python tasks/job_put_tasks.py       # 初次创建任务
python tasks/jobs_sogou.py          # 初次应对反爬
scrapy crawl weixin                 # 开启微信爬虫
```

- env_develop.sh   # 开发环境
- env_product.sh   # 生产环境

## 项目创建过程记录

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


创建项目
```bash
scrapy startproject news .
scrapy genspider weixin mp.weixin.qq.com
```

启动蜘蛛
```bash
scrapy crawl weixin
```

## 验证码识别

http://www.ruokuai.com/
http://wiki.ruokuai.com/

价格类型:
http://www.ruokuai.com/home/pricetype
