#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_rk.py
@time: 2018-02-10 17:34
"""


from libs.rk import RClient
from libs.counter import CounterClient
from apps.client_db import redis_client
from tools.cookies import len_cookies

from config import current_config

RK_CONFIG = current_config.RK_CONFIG
BASE_DIR = current_config.BASE_DIR
RK_LIMIT_COUNT_DAILY = current_config.RK_LIMIT_COUNT_DAILY
COOKIES_QUEUE_COUNT = current_config.COOKIES_QUEUE_COUNT

rc_client = RClient(**RK_CONFIG)

rk_counter_client = CounterClient(redis_client, 'rk')

# 正常图形验证码
# 'im_type_id': 1000     # 任意长度数字
# 'im_type_id': 2000     # 任意长度字母
# 'im_type_id': 3000     # 任意长度英数混合
# 'im_type_id': 4000     # 任意长度汉字
# 'im_type_id': 5000     # 任意长度中英数三混


def get_img_code(im, im_type_id):
    """
    获取验证码
    :param im:
    :param im_type_id:
    :return:
    """
    rc_result = rc_client.rk_create(im, im_type_id)
    print(rc_result)
    if 'Error_Code' in rc_result:
        print(rc_result.get('Error'))
        return None, None
    # {u'Result': u'6dx2t8', u'Id': u'c8a897f0-9825-41a1-b19e-6195ba8559ed'}
    return rc_result['Id'], rc_result['Result']


def img_report_error(im_id):
    rc_client.rk_report_error(im_id)


def check_counter_limit():
    """
    检查是否超过限制（True: 没有超过; False: 超过限制）
    :return:
    """
    rk_counter = rk_counter_client.get()
    return rk_counter < RK_LIMIT_COUNT_DAILY


def check_cookies_count(spider_name):
    """
    检查 cookies 长度是否达到要求（True: 没有达到; False: 达到要求）
    :param spider_name:
    :return:
    """
    return len_cookies(spider_name) < COOKIES_QUEUE_COUNT


def counter_clear():
    """
    计数器清零（每天0点）
    :return:
    """
    rk_counter_client.clear()
