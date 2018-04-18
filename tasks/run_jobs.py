#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_jobs.py
@time: 2018-04-18 11:10
"""


import schedule
import time
from functools import wraps

from tasks import job_put_tasks
from tasks.jobs_sogou import job_sogou_cookies
from tasks.jobs_weixin import job_weixin_cookies
from apps.client_rk import counter_clear as job_counter_clear


def catch_keyboard_interrupt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('\n强制退出')

    return wrapper


# sogou 反爬任务
schedule.every(5).minutes.do(job_sogou_cookies, spider_name='weixin')
# weixin 反爬任务
schedule.every(5).minutes.do(job_weixin_cookies, spider_name='weixin')
# 分布式任务调度 - 微信
schedule.every(5).minutes.do(job_put_tasks, spider_name='weixin')
# 分布式任务调度 - 微博
schedule.every(5).minutes.do(job_put_tasks, spider_name='weibo')
# 分布式任务调度 - 头条
schedule.every(5).minutes.do(job_put_tasks, spider_name='toutiao')
# 计数清零
schedule.every().day.at('00:00').do(job_counter_clear)


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
