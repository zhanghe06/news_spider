#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_job_optical_modem_china_net.py
@time: 2018-05-28 19:35
"""

import time

import schedule

from tasks.job_reboot_net_china_net import job_reboot_net_china_net
from tools import catch_keyboard_interrupt


# 电信光猫重启
schedule.every(15).minutes.do(job_reboot_net_china_net)


@catch_keyboard_interrupt
def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
