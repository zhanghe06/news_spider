#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_job_sogou_cookies.py
@time: 2018-05-02 10:21
"""

import time

import schedule

from tasks.jobs_sogou import job_sogou_cookies
from tools import catch_keyboard_interrupt

# sogou 反爬任务
schedule.every(5).minutes.do(job_sogou_cookies, spider_name='weixin')


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
