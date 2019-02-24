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
import re
import random
import hashlib
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


class OpticalModemChinaMobile(object):
    """
    移动光猫
    登录密码表单SHA256加密
    """
    s = requests.session()
    pid = 1002
    session_token = 0

    def __init__(self, host='192.168.1.1', username='user', password='gkw4p3uv'):

        self.host = host
        self.username = username
        self.password = password

        self.pwd_random = self._get_pwd_random()
        self.encryption_pwd = self._get_encryption_pwd(self.password, self.pwd_random)
        self.token = self._get_token()

        self.url_login = 'http://%s/' % self.host

        self.timeout = 180

        self.net_ip_o = None
        self.net_ip_n = None

    @staticmethod
    def _get_pwd_random():
        pwd_random = str(int(round(random.random() * 89999999)) + 10000000)
        return pwd_random

    @staticmethod
    def _get_encryption_pwd(pwd, r):
        encryption_pwd = hashlib.sha256(''.join([pwd, r])).hexdigest()
        return encryption_pwd

    def _get_token(self):
        url = 'http://%s' % self.host
        res = self.s.get(url)
        html_body = res.text
        token_re = re.compile(r'getObj\("Frm_Logintoken"\)\.value = "(\d+)";')
        token_list = re.findall(token_re, html_body)
        return int(token_list[0]) if token_list else 0

    def _get_pid(self):
        url = 'http://%s/template.gch' % self.host
        res = self.s.get(url, timeout=self.timeout)
        html_body = res.text
        pid_re = re.compile(r'"getpage\.gch\?pid=(\d+)&nextpage="')
        pid_list = re.findall(pid_re, html_body)
        self.pid = int(pid_list[0]) if pid_list else self.pid
        return self.pid

    def _get_session_token(self):
        url = 'http://%s/getpage.gch?pid=%s&nextpage=manager_dev_restart_t.gch' % (self.host, self.pid)
        res = self.s.get(url, timeout=self.timeout)
        html_body = res.text
        session_token_re = re.compile(r'var session_token = "(\d+)";')
        session_token_list = re.findall(session_token_re, html_body)
        self.session_token = int(session_token_list[0]) if session_token_list else self.session_token
        return self.session_token

    def login(self):
        """
        登录
        :return:
        """
        payload = {
            'frashnum': '',
            'action': 'login',
            'Frm_Logintoken': self.token,
            'UserRandomNum': self.pwd_random,
            'Username': self.username,
            'Password': self.encryption_pwd,
        }
        res = self.s.post(self.url_login, data=payload, timeout=self.timeout)
        return 'mainFrame' in res.text

    def reboot(self):
        url = 'http://%s/getpage.gch?pid=%s&nextpage=manager_dev_restart_t.gch' % (self.host, self._get_pid())
        payload = {
            'IF_ACTION': 'devrestart',
            'IF_ERRORSTR': 'SUCC',
            'IF_ERRORPARAM': 'SUCC',
            'IF_ERRORTYPE': -1,
            'flag': 1,
            '_SESSION_TOKEN': self._get_session_token(),
        }

        res = self.s.post(url, data=payload, timeout=self.timeout)
        return '设备重启需要2~3分钟，请耐心等待。' in res.text

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


def test_china_net():
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


def test_china_mobile():
    om_cm = OpticalModemChinaMobile()

    om_cm.net_ip_o = om_cm.get_net_ip()

    om_cm.login()
    om_cm.reboot()

    time.sleep(10)
    c = 3
    while 1:
        if c <= 0:
            break
        try:
            om_cm.net_ip_n = om_cm.get_net_ip()
            break
        except Exception as e:
            c -= 1
            print(e)

    om_cm.check_reboot_status()


if __name__ == '__main__':
    # test_china_net()
    test_china_mobile()
