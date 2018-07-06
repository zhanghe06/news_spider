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
import datetime
from tools.date_time import time_local_to_utc, time_utc_to_local


class DateTimeTest(unittest.TestCase):
    """
    日期时间测试
    """
    def setUp(self):
        self.time_offset = time.timezone
        self.local_time = '2018-06-06 18:12:26'
        self.utc_time = '2018-06-06 10:12:26'

    def test_local_to_utc(self):
        """
        测试
        :return:
        """
        local_time_obj = datetime.datetime.strptime(self.local_time, '%Y-%m-%d %H:%M:%S')
        utc_time_obj = time_local_to_utc(self.local_time)
        self.assertEqual(utc_time_obj, local_time_obj + datetime.timedelta(seconds=self.time_offset))

    def test_utc_to_local(self):
        """
        测试
        :return:
        """
        utc_time_obj = datetime.datetime.strptime(self.utc_time, '%Y-%m-%d %H:%M:%S')
        local_time_obj = time_utc_to_local(self.utc_time)
        self.assertEqual(utc_time_obj, local_time_obj + datetime.timedelta(seconds=self.time_offset))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
