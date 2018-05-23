#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: optical_modem.py
@time: 2018-05-27 00:24
"""

import base64
import json
import time

import requests
from scrapy.selector import Selector


class OpticalModemChinaNet(object):
    """
    电信光猫
    """
    s = requests.session()

    def __init__(self, host='192.168.1.1', username='useradmin', password='crcun'):

        self.host = host
        self.username = username
        self.password = password

        self.url_login = 'http://%s/login.cgi' % self.host
        self.url_get_wan_wifi_status = 'http://%s/gatewayManage.cmd' % self.host
        self.url_reboot = 'http://%s/gatewayManage.cmd' % self.host

        self.timeout = 180

        self.net_ip_o = None
        self.net_ip_n = None

    @staticmethod
    def _get_tc():
        tc = str('%13d' % (time.time() * 1000))
        return tc

    def login(self):
        """
        登录
        :return:
        """
        params = {
            'username': self.username,
            'psd': self.password,
        }
        res = self.s.get(self.url_login, params=params, timeout=self.timeout)
        print(res.status_code, res.url)

    def get_wan_wifi_status(self):
        """
        获取wifi状态
        :return:
        """
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'timeStamp': self._get_tc(),
        }
        json_cfg = {
            'RPCMethod': 'Post1',
            'ID': '123',
            'Parameter': base64.urlsafe_b64encode("{'CmdType':'GET_WAN_WIFI_STATUS'}")
        }
        data = "jsonCfg=%s" % json.dumps(json_cfg)
        res = self.s.post(self.url_get_wan_wifi_status, headers=headers, params=params, data=data, timeout=self.timeout)
        print(res.status_code, res.url)
        return_parameter = json.loads(base64.decodestring(res.json().get('return_Parameter', '')))
        print(return_parameter)
        print(return_parameter.get('ipAddr'))
        wan_ip = return_parameter.get('ipAddr')
        return wan_ip

    def reboot(self):
        """
        重启
        :return:
        """
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        params = {
            'timeStamp': self._get_tc(),
        }
        json_cfg = {
            'RPCMethod': 'Post1',
            'ID': '123',
            'Parameter': base64.urlsafe_b64encode("{'CmdType':'HG_COMMAND_REBOOT'}")
        }
        data = "jsonCfg=%s" % json.dumps(json_cfg)
        res = self.s.post(self.url_reboot, headers=headers, params=params, data=data, timeout=self.timeout)
        print(res.status_code, res.url)
        return_parameter = json.loads(base64.decodestring(res.json().get('return_Parameter', '')))
        print(return_parameter)

    def get_net_ip(self):
        """
        获取网络IP，这里使用requests不用session，因为重启之后，session会断开
        :return:
        """
        url = 'https://ip.cn/'
        res = requests.get(url, timeout=self.timeout)
        response = Selector(res)
        info = response.xpath('//div[@class="well"]//code/text()').extract()
        ip_info = dict(zip(['ip', 'address'], info))
        net_ip = ip_info['ip']
        print(net_ip)
        return net_ip

    def check_reboot_status(self):
        reboot_status = self.net_ip_o != self.net_ip_n
        print(reboot_status)
        return reboot_status


def test():
    om_cn = OpticalModemChinaNet()

    om_cn.net_ip_o = om_cn.get_net_ip()

    om_cn.login()  # 默认用户名、密码
    om_cn.reboot()

    time.sleep(10)
    c = 3
    while 1:
        if c <= 0:
            break
        try:
            om_cn.net_ip_n = om_cn.get_net_ip()
            break
        except Exception as e:
            c -= 1
            print(e)

    om_cn.check_reboot_status()


if __name__ == '__main__':
    test()
