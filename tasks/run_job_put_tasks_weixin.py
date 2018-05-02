#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_job_put_tasks_weixin.py
@time: 2018-05-02 10:23
"""

import time

import schedule

from tasks.job_put_tasks import job_put_tasks
from tools import catch_keyboard_interrupt


# 分布式任务调度 - 微信
schedule.every(5).minutes.do(job_put_tasks, spider_name='weixin')


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
