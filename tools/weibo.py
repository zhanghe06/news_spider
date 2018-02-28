#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weibo.py
@time: 2018-02-13 16:20
"""


import base64

# from urllib import quote                      # PY2
# from urllib.parse import quote                # PY3
from future.moves.urllib.parse import quote
from future.builtins import input               # PY2(raw_input)


def get_su(user_name):
    return base64.b64encode(quote(user_name.strip()))


def get_login_data():
    print('Please type username and password!')
    username = input('username < ')
    password = input('password < ')
    if not(username and password):
        raise Exception('Method or function hasn\'t been implemented yet.')
    return {
        'username': username,
        'password': password
    }


if __name__ == '__main__':
    pass

