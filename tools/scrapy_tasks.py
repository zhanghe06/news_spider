#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: scrapy_tasks.py
@time: 2018-02-10 17:42
"""


from apps.client_db import redis_client


def pop_task(spider_name):
    key_set = 'scrapy:tasks_set:%(spider_name)s' % {'spider_name': spider_name}
    return redis_client.spop(key_set)


def put_task(spider_name, *task_ids):
    key_set = 'scrapy:tasks_set:%(spider_name)s' % {'spider_name': spider_name}
    redis_client.sadd(key_set, *task_ids)


def get_tasks_count(spider_name):
    key_set = 'scrapy:tasks_set:%(spider_name)s' % {'spider_name': spider_name}
    cookies_len = redis_client.scard(key_set)
    return cookies_len
