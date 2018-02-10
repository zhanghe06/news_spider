#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: redis_pub_sub.py
@time: 2018-02-10 15:24
"""

import redis


class RedisPubSub(object):
    """
    Pub/Sub
        队列中存储的数据必须是序列化之后的数据
        生产消息: 入队前, 序列化
        消费消息: 出队后, 反序列化
    """

    def __init__(self, name, namespace='pub/sub', redis_client=None, **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis_client or redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def pub(self, k, v):
        """
        Pub
        :param k:
        :param v:
        :return:
        """
        ch = '%s:%s' % (self.key, k)
        self.__db.publish(ch, v)

    def sub(self, k):
        """
        Sub
        :param k:
        :return:
        """
        ps = self.__db.pubsub()
        ch = '%s:%s' % (self.key, k)
        ps.subscribe(ch)
        for item in ps.listen():
            # {'pattern': None, 'type': 'subscribe', 'channel': 'pub/sub:test:hh', 'data': 1L}
            yield item
            if item['type'] == 'message':
                yield item.get('data')

    def p_sub(self, k):
        """
        PSub
        订阅一个或多个符合给定模式的频道
        每个模式以 * 作为匹配符
        注意 psubscribe 与 subscribe 区别
        :param k:
        :return:
        """
        ps = self.__db.pubsub()
        ch = '%s:%s' % (self.key, k)
        ps.psubscribe(ch)
        for item in ps.listen():
            # {'pattern': None, 'type': 'psubscribe', 'channel': 'pub/sub:test:*:hh', 'data': 1L}
            # yield item
            if item['type'] == 'pmessage':
                # {'pattern': 'pub/sub:test:*:hh', 'type': 'pmessage', 'channel': 'pub/sub:test:aa:hh', 'data': '123'}
                yield item.get('data')

    def sub_not_loop(self, k):
        """
        Sub 非无限循环，取到结果即退出
        :param k:
        :return:
        """
        ps = self.__db.pubsub()
        ch = '%s:%s' % (self.key, k)
        ps.subscribe(ch)
        for item in ps.listen():
            if item['type'] == 'message':
                return item.get('data')

    def p_sub_not_loop(self, k):
        """
        PSub 非无限循环，取到结果即退出
        :param k:
        :return:
        """
        ps = self.__db.pubsub()
        ch = '%s:%s' % (self.key, k)
        ps.psubscribe(ch)
        for item in ps.listen():
            if item['type'] == 'pmessage':
                return item.get('data')
