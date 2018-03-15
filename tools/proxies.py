#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: proxies.py
@time: 2018-03-13 16:37
"""


import json
import requests
from apps.client_db import redis_client
from tools.url import get_update_url

from config import current_config


REQUESTS_TIME_OUT = current_config.REQUESTS_TIME_OUT


def add_proxy(spider_name, *proxy):
    key_set = 'scrapy:proxies_set:%(spider_name)s' % {'spider_name': spider_name}
    return redis_client.sadd(key_set, *proxy)


def del_proxy(spider_name, proxy):
    key_set = 'scrapy:proxies_set:%(spider_name)s' % {'spider_name': spider_name}
    return redis_client.srem(key_set, proxy)


def get_proxy(spider_name):
    key_set = 'scrapy:proxies_set:%(spider_name)s' % {'spider_name': spider_name}
    return redis_client.srandmember(key_set)


def len_proxy(spider_name):
    key_set = 'scrapy:proxies_set:%(spider_name)s' % {'spider_name': spider_name}
    return redis_client.scard(key_set)


def fetch_proxy(country='China', scheme='http'):
    """
    获取代理
    :param country:
    :param scheme:
    :return:
    """
    data = {}
    if country:
        data['country'] = country
    if scheme:
        data['type'] = scheme
    url = 'http://proxy.nghuyong.top/'
    url = get_update_url(url, data)
    res = requests.get(url, timeout=REQUESTS_TIME_OUT).json()
    return ['%s://%s' % (i['type'], i['ip_and_port']) for i in res.get('data', [])]


if __name__ == '__main__':
    proxy_result = fetch_proxy()
    print(json.dumps(proxy_result, indent=4))
