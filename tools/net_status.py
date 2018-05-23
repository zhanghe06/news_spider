#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: net_status.py
@time: 2018-05-28 20:45
"""

import time
from apps.client_db import redis_client


def get_reboot_net_status(net_name='optical_modem_china_net'):
    key_reboot_net = 'scrapy:reboot_net:%s' % net_name
    reboot_net_status = redis_client.get(key_reboot_net)
    return reboot_net_status


def set_reboot_net_status(net_name='optical_modem_china_net'):
    key_reboot_net = 'scrapy:reboot_net:%s' % net_name
    reboot_net_status = time.strftime('%Y-%m-%d %H:%M:%S')
    redis_client.set(key_reboot_net, reboot_net_status)


def del_reboot_net_status(net_name='optical_modem_china_net'):
    key_reboot_net = 'scrapy:reboot_net:%s' % net_name
    redis_client.delete(key_reboot_net)
