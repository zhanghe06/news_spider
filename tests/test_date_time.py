#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_date_time.py
@time: 2018-06-25 17:55
"""


from __future__ import unicode_literals

import unittest

import time
from tools.date_time import time_local_to_utc, time_utc_to_local


class DateTimeTest(unittest.TestCase):
    """
    日期时间测试
    """

    def setUp(self):
        # 假设当前时区在东8区
        self.assertEqual(time.timezone, -60*60*8)

    def test_local_to_utc(self):
        """
        测试
        :return:
        """
        local_time = '2018-06-06 18:12:26'
        utc_time = time_local_to_utc(local_time).strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(utc_time, '2018-06-06 10:12:26')

    def test_utc_to_local(self):
        """
        测试
        :return:
        """
        utc_time = '2018-06-06 10:12:26'
        local_time = time_utc_to_local(utc_time).strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(local_time, '2018-06-06 18:12:26')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

