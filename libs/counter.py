#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: counter.py
@time: 2018-02-10 15:24
"""

from redis import Redis


class CounterClient(object):
    """
    计数器
    """

    def __init__(self, redis_client, entity_name, prefix='counter'):
        """
        :param redis_client:
        :param entity_name:
        :param prefix:
        """
        self.redis_client = redis_client  # type: Redis
        self.counter_key = "%s:%s" % (prefix, entity_name)

    def increase(self, amount=1):
        """
        增加计数
        :param amount:
        :return:
        """
        return int(self.redis_client.incr(self.counter_key, amount))

    def decrease(self, amount=1):
        """
        减少计数
        :param amount:
        :return:
        """
        return int(self.redis_client.decr(self.counter_key, amount))

    def get(self):
        """
        获取计数
        :return:
        """
        return int(self.redis_client.get(self.counter_key) or 0)

    def clear(self):
        """
        清除计数
        :return:
        """
        return self.redis_client.delete(self.counter_key)
