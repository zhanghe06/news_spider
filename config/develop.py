#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: develop.py
@time: 2018-02-10 15:07
"""


import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# requests 超时设置
REQUESTS_TIME_OUT = (30, 30)

HOST_IP = '192.168.4.1'

# 数据库 MySQL
DB_MYSQL = {
    'host': HOST_IP,
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'news_spider'
}

SQLALCHEMY_DATABASE_URI_MYSQL = \
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % \
    (DB_MYSQL['user'], DB_MYSQL['passwd'], DB_MYSQL['host'], DB_MYSQL['port'], DB_MYSQL['db'])

SQLALCHEMY_POOL_SIZE = 5  # 默认 pool_size=5

# 缓存，队列
REDIS = {
    'host': HOST_IP,
    'port': 6379,
    # 'password': '123456'  # redis-cli AUTH 123456
}

# 若快验证码识别
RK_CONFIG = {
    'username': '******',
    'password': '******',
    'soft_id': '93676',
    'soft_key': '5d0e00b196c244cb9d8413809c62f9d5',
}

# 熔断机制 每天请求限制（200元==500000快豆）
RK_LIMIT_COUNT_DAILY = 925

# 队列保留 cookies 数量
COOKIES_QUEUE_COUNT = 5

# 分布式文件系统
WEED_FS_URL = 'http://%s:9333' % HOST_IP

# 优先级配置（深度优先）
PRIORITY_CONFIG = {
    'list': 600,
    'next': 500,
    'detail': 800,
}
