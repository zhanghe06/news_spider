#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: job_reboot_net_china_net.py
@time: 2018-05-28 19:40
"""


import time
from libs.optical_modem import OpticalModemChinaNet
from tools.net_status import get_reboot_net_status, del_reboot_net_status

net_name = 'optical_modem_china_net'


def job_reboot_net_china_net():
    """
    重启中国电信光猫
    :return:
    """
    # reboot_net_status = get_reboot_net_status(net_name)
    # if not reboot_net_status:
    #     return

    om_cn = OpticalModemChinaNet()
    om_cn.net_ip_o = om_cn.get_net_ip()
    om_cn.login()  # 默认用户名、密码
    om_cn.reboot()
    time.sleep(10)
    om_cn.net_ip_n = om_cn.get_net_ip()
    om_cn.check_reboot_status()

    del_reboot_net_status(net_name)
