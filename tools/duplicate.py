#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: duplicate.py
@time: 2018-02-10 17:39
"""

from __future__ import print_function
from __future__ import unicode_literals

from apps.client_db import redis_client
from tools.url import get_request_finger


def is_dup_detail(detail_url, spider_name, channel_id=0):
    """
    检查详细页是否重复
    :param detail_url:
    :param spider_name:
    :param channel_id:
    :return:
    """
    detail_dup_key = 'scrapy:dup:%s:%s' % (spider_name, channel_id)
    detail_url_finger = get_request_finger(detail_url)
    return redis_client.sismember(detail_dup_key, detail_url_finger)


def add_dup_detail(detail_url, spider_name, channel_id=0):
    """
    把当前详细页加入集合
    :param detail_url:
    :param spider_name:
    :param channel_id:
    :return:
    """
    detail_dup_key = 'scrapy:dup:%s:%s' % (spider_name, channel_id)
    detail_url_finger = get_request_finger(detail_url)
    return redis_client.sadd(detail_dup_key, detail_url_finger)
