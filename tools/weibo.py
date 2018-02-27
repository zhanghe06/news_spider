#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weibo.py
@time: 2018-02-13 16:20
"""


import base64
import urllib


def get_su(user_name):
    return base64.b64encode(urllib.quote(user_name.strip()))


def get_login_data():
    return {
        'username': '******',
        'password': '******'
    }


if __name__ == '__main__':
    pass

