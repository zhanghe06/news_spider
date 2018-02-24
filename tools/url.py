#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: url.py
@time: 2018-02-10 17:38
"""


import urllib
import urlparse

from scrapy.utils import request
from scrapy.http import Request


def get_update_url(url, data):
    """
    获取更新后的url
    :param url:
    :param data:
    :return:
    """
    result = urlparse.urlparse(url)
    query_payload = dict(urlparse.parse_qsl(result.query), **data)
    query_param = urllib.urlencode(query_payload)
    return urlparse.urlunparse((result.scheme, result.netloc, result.path, result.params, query_param, result.fragment))


def get_url_query_param(url, param):
    """
    获取url参数值
    :param url:
    :param param:
    :return:
    """
    result = urlparse.urlparse(url)
    return dict(urlparse.parse_qsl(result.query)).get(param)


def get_request_finger(url):
    """
    获取 url 指纹（允许参数无序）
    :param url:
    :return:
    """
    req = Request(url=url)
    return request.request_fingerprint(req)


if __name__ == '__main__':
    print(get_update_url('http://www.abc.com/def/?a=1', {'b': 2}))
    print(get_update_url('http://www.abc.com/def/?a=1', {'a': 2}))
    print(get_url_query_param('http://www.abc.com/def/?a=1&b=2', 'a'))
