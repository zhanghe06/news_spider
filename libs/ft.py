#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: ff.py
@time: 2019-05-26 14:26
"""

import base64
import hashlib
import time
import requests


URL = "http://pred.fateadm.com"


class FTClient(object):
    def __init__(self, pd_id, pd_key, app_id='', app_key=''):
        self.pd_id = pd_id
        self.pd_key = pd_key
        self.app_id = app_id
        self.app_key = app_key
        self.host = URL
        self.s = requests.session()
        self.timeout = 30

    @staticmethod
    def calc_sign(pd_id, pd_key, timestamp):
        md5 = hashlib.md5()
        md5.update(timestamp + pd_key)
        sign_a = md5.hexdigest()

        md5 = hashlib.md5()
        md5.update(pd_id + timestamp + sign_a)
        sign_b = md5.hexdigest()
        return sign_b

    @staticmethod
    def calc_card_sign(card_id, card_key, timestamp, pd_key):
        md5 = hashlib.md5()
        md5.update(pd_key + timestamp + card_id + card_key)
        return md5.hexdigest()

    def query_balance(self):
        """查询余额"""
        tm = str(int(time.time()))
        sign = self.calc_sign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign
        }
        url = self.host + "/api/custval"
        rsp = self.s.post(url, param, timeout=self.timeout).json()
        return rsp

    def query_tts(self, predict_type):
        """查询网络延迟"""
        tm = str(int(time.time()))
        sign = self.calc_sign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            "predict_type": predict_type,
        }
        if self.app_id != "":
            asign = self.calc_sign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = self.host + "/api/qcrtt"
        rsp = self.s.post(url, param, timeout=self.timeout).json()
        return rsp

    def predict(self, predict_type, img_data):
        """识别验证码"""
        tm = str(int(time.time()))
        sign = self.calc_sign(self.pd_id, self.pd_key, tm)
        img_base64 = base64.b64encode(img_data)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            "predict_type": predict_type,
            "img_data": img_base64,
        }
        if self.app_id != "":
            asign = self.calc_sign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = self.host + "/api/capreg"
        rsp = self.s.post(url, param, timeout=self.timeout).json()
        return rsp

    def predict_from_file(self, predict_type, file_name):
        """从文件进行验证码识别"""
        with open(file_name, "rb+") as f:
            data = f.read()
        return self.predict(predict_type, data)

    def justice(self, request_id):
        """识别失败，进行退款请求"""
        if request_id == "":
            return
        tm = str(int(time.time()))
        sign = self.calc_sign(self.pd_id, self.pd_key, tm)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            "request_id": request_id
        }
        url = self.host + "/api/capjust"
        rsp = self.s.post(url, param, timeout=self.timeout).json()
        return rsp

    def charge(self, card_id, card_key):
        """充值接口"""
        tm = str(int(time.time()))
        sign = self.calc_sign(self.pd_id, self.pd_key, tm)
        card_sign = self.calc_card_sign(card_id, card_key, tm, self.pd_key)
        param = {
            "user_id": self.pd_id,
            "timestamp": tm,
            "sign": sign,
            'cardid': card_id,
            'csign': card_sign
        }
        url = self.host + "/api/charge"
        rsp = self.s.post(url, param, timeout=self.timeout).json()
        return rsp


def test_ft():
    """
    测试
    {u'RspData': u'{"cust_val":1010}', u'RetCode': u'0', u'ErrMsg': u'succ', u'RequestId': u''}
    {u'RspData': u'{"result": "8x4g"}', u'RetCode': u'0', u'ErrMsg': u'', u'RequestId': u'2019052615005042ad98b2000518d493'}
    :return:
    """
    pd_id = "xxxxxx"
    pd_key = "xxxxxx"
    app_id = "312451"
    app_key = "5YuN+6isLserKBZti4hoaI6UR2N5UT2j"
    predict_type = "30400"
    api = FTClient(pd_id, pd_key, app_id, app_key)
    # 查询余额接口
    res = api.query_balance()
    print(res)
    file_name = "img.jpg"
    rsp = api.predict_from_file(predict_type, file_name)
    print(rsp)

if __name__ == "__main__":
    test_ft()
