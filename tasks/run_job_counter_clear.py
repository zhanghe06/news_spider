#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_job_counter_clear.py
@time: 2018-05-02 10:24
"""

import time

import schedule

from apps.client_rk import counter_clear as job_counter_clear
from tools import catch_keyboard_interrupt

# 计数清零
schedule.every().day.at('00:00').do(job_counter_clear)


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
