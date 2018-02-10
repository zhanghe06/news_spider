#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_finger.py
@time: 2018-02-11 00:06
"""

import hashlib
import unittest

from scrapy.http import Request
from scrapy.utils import request


class FingerTest(unittest.TestCase):
    """
    指纹测试
    """

    def setUp(self):
        self.url_01 = 'https://www.baidu.com/s?wd=openstack&rsv_spt=1'
        self.url_02 = 'https://www.baidu.com/s?rsv_spt=1&wd=openstack'

    def test_request(self):
        """
        测试请求
        :return:
        """
        req_01 = Request(url=self.url_01)
        result_01 = request.request_fingerprint(req_01)

        req_02 = Request(url=self.url_02)
        result_02 = request.request_fingerprint(req_02)

        self.assertEqual(result_01, result_02)

    def tearDown(self):
        pass


class MD5Test(unittest.TestCase):
    """
    md5测试
    """

    def setUp(self):
        self.url_01 = 'https://www.baidu.com/s?wd=openstack&rsv_spt=1'
        self.url_02 = 'https://www.baidu.com/s?rsv_spt=1&wd=openstack'

    def test_request(self):
        """
        测试请求
        :return:
        """
        m1 = hashlib.md5()
        m1.update(self.url_01)
        result_01 = m1.hexdigest()

        m2 = hashlib.md5()
        m2.update(self.url_02)
        result_02 = m2.hexdigest()

        self.assertNotEqual(result_01, result_02)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
