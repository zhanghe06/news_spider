#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: cookies.py
@time: 2018-02-10 17:49
"""


import json
import hashlib

from apps.client_db import redis_client


def _get_cookies_str(cookies_dict):
    """
    In [1]: import json

    In [2]: sd = {'c':1, 'b':2, 'a':3}

    In [3]: sd
    Out[3]: {'a': 3, 'b': 2, 'c': 1}

    In [4]: items = sd.items()

    In [5]: items
    Out[5]: [('a', 3), ('c', 1), ('b', 2)]

    In [6]: sorted(items)
    Out[6]: [('a', 3), ('b', 2), ('c', 1)]

    In [7]: sorted(items, reverse=True)
    Out[7]: [('c', 1), ('b', 2), ('a', 3)]

    In [8]: json.dumps(sorted(items))
    Out[8]: '[["a", 3], ["b", 2], ["c", 1]]'

    In [9]: json.loads(json.dumps(sorted(items)))
    Out[9]: [[u'a', 3], [u'b', 2], [u'c', 1]]

    In [10]: dict(json.loads(json.dumps(sorted(items))))
    Out[10]: {u'a': 3, u'b': 2, u'c': 1}
    :param cookies_dict:
    :return:
    """
    cookies_str = json.dumps(sorted(cookies_dict.items()))
    return cookies_str


def _get_finger(cookies_str):
    """
    :param cookies_str:
    :return:
    """
    m = hashlib.md5()
    m.update(cookies_str.encode('utf-8') if isinstance(cookies_str, unicode) else cookies_str)
    finger = m.hexdigest()
    return finger


def get_cookies(spider_name):
    """
    获取 cookies
    兼容 redis 没有 cookies 池的情况
    :param spider_name:
    :return:
    """
    key_set = 'scrapy:cookies_set:%(spider_name)s' % {'spider_name': spider_name}
    cookies_id = redis_client.srandmember(key_set)

    key_id = 'scrapy:cookies_id:%(cookies_id)s' % {'cookies_id': cookies_id}
    cookies_str = redis_client.get(key_id)
    cookies_obj = dict(json.loads(cookies_str or '[]'))

    return cookies_id, cookies_obj


def add_cookies(spider_name, cookies_obj):
    """
    添加 cookies
    :param spider_name:
    :param cookies_obj:
    :return:
    """
    cookies_str = _get_cookies_str(cookies_obj)
    cookies_id = _get_finger(cookies_str)

    key_id = 'scrapy:cookies_id:%(cookies_id)s' % {'cookies_id': cookies_id}
    key_set = 'scrapy:cookies_set:%(spider_name)s' % {'spider_name': spider_name}

    if redis_client.sismember(key_set, cookies_id):
        return False

    redis_client.set(key_id, cookies_str)
    redis_client.sadd(key_set, cookies_id)
    return True


def del_cookies(spider_name, cookies_id):
    """
    删除 cookies
    :param spider_name:
    :param cookies_id:
    :return:
    """
    key_id = 'scrapy:cookies_id:%(cookies_id)s' % {'cookies_id': cookies_id}
    key_set = 'scrapy:cookies_set:%(spider_name)s' % {'spider_name': spider_name}

    redis_client.delete(key_id)
    redis_client.srem(key_set, cookies_id)


def len_cookies(spider_name):
    """
    获取 cookies 长度
    :param spider_name:
    :return:
    """
    key_set = 'scrapy:cookies_set:%(spider_name)s' % {'spider_name': spider_name}
    cookies_len = redis_client.scard(key_set)
    return cookies_len


"""
集合
key: cookies_id

字符串
cookies_id_key: cookies_obj
"""
