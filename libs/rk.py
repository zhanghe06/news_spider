#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: rk.py
@time: 2018-02-10 15:25
"""

from hashlib import md5

import requests


class RKClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post(
            'http://api.ruokuai.com/create.json',
            data=params,
            files=files,
            headers=self.headers,
            timeout=timeout
        )
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post(
            'http://api.ruokuai.com/reporterror.json',
            data=params,
            headers=self.headers,
            timeout=30
        )
        return r.json()


if __name__ == '__main__':
    rc = RKClient('username', 'password', 'soft_id', 'soft_key')
    im = open('a.jpg', 'rb').read()
    print(rc.rk_create(im, 3040))
