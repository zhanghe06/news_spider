#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: anti_spider_sogou.py
@time: 2018-02-10 17:24
"""


from __future__ import print_function
from __future__ import unicode_literals

from future.builtins import input               # PY2(raw_input)

import random
import time
import json

import requests

from apps.client_rk import get_img_code, img_report_error

from config import current_config


REQUESTS_TIME_OUT = current_config.REQUESTS_TIME_OUT


cookies = {}


s = requests.session()


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    # 'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
}


def _get_tc():
    tc = str('%13d' % (time.time() * 1000))
    return tc


def _save_img(res):
    # 保存验证码图片
    img_name = 'sogou_%s.jpg' % _get_tc()
    print('图片名称: %s' % img_name)
    img_content = res.content
    with open(img_name, b'w') as f:
        f.write(img_content)
    time.sleep(1)


def anti_spider():
    url = 'http://weixin.sogou.com/antispider/?from=/weixin?type=2&query=chuangbiandao'

    request_headers = headers.copy()
    request_headers['Host'] = 'weixin.sogou.com'

    request_cookie = {
        'refresh': '1'
    }

    res = s.get(url, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')
    # print cookies


def code_img_save():
    url = 'http://weixin.sogou.com/antispider/util/seccode.php'

    request_headers = headers.copy()
    request_headers['Host'] = 'weixin.sogou.com'

    request_cookie = cookies.copy()

    params = {
        'tc': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)

    # 保存图片
    _save_img(res)

    cookies.update(res.cookies)
    print('.', end='')
    # print cookies


def code_img_obj():
    url = 'http://weixin.sogou.com/antispider/util/seccode.php'

    request_headers = headers.copy()
    request_headers['Host'] = 'weixin.sogou.com'

    request_cookie = cookies.copy()

    params = {
        'tc': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    print('.', end='')
    return res.content


def pv_refresh():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
    }
    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'refresh',
        'domain': 'weixin',
        'suv': '',
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_index():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
    }
    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'index',
        'domain': 'weixin',
        'suv': '',
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_img_cost():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'imgCost',
        'domain': 'weixin',
        'suv': '',
        'snuid': '',
        't': _get_tc(),
        'cost': '27',
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_mouse():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'mouse',
        'domain': 'weixin',
        'suv': cookies['SUV'],
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_img_success():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'imgSuccess',
        'domain': 'weixin',
        'suv': cookies['SUV'],
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_real_index():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'realIndex',
        'domain': 'weixin',
        'suv': cookies['SUV'],
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_seccode_focus():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'seccodeFocus',
        'domain': 'weixin',
        'suv': cookies['SUV'],
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_seccode_input():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'seccodeInput',
        'domain': 'weixin',
        'suv': cookies['SUV'],
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def pv_seccode_blur():
    url = 'http://pb.sogou.com/pv.gif'

    request_headers = headers.copy()
    request_headers['Host'] = 'pb.sogou.com'

    request_cookie = {
        'IPLOC': cookies['IPLOC'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    params = {
        'uigs_productid': 'webapp',
        'type': 'antispider',
        'subtype': 'seccodeBlur',
        'domain': 'weixin',
        'suv': cookies['SUV'],
        'snuid': '',
        't': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')


def thank(code_anti_spider):
    url = 'http://weixin.sogou.com/antispider/thank.php'

    request_headers = headers.copy()
    request_headers['X-Requested-With'] = 'XMLHttpRequest'

    request_cookie = {
        'ABTEST': cookies['ABTEST'],
        'IPLOC': cookies['IPLOC'],
        'SUID': cookies['SUID'],
        'PHPSESSID': cookies['PHPSESSID'],
        'SUIR': cookies['SUIR'],
        'SUV': cookies['SUV'],
    }

    data = {
        'c': code_anti_spider,
        'r': '%2Fweixin%3Ftype%3D2',
        'v': '5',
    }

    res = s.post(url, data=data, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    # print cookies

    json_msg = json.loads(res.content)
    print(json_msg)
    return json_msg
    # {"code": 0,"msg": "解封成功，正在为您跳转来源地址...", "id": "ECB542781D1B4105B09FB4461E0587D4"}
    # {"code": 2,"msg": "未知访问来源"}
    # {"code": 3,"msg": "验证码输入错误, 请重新输入！"}


def _get_cookies():
    print(cookies)
    return cookies


def check_n():
    url = 'http://weixin.sogou.com/weixin?query=chuangbiandao&type=1'
    res = requests.get(url, headers=headers, timeout=REQUESTS_TIME_OUT)
    print(res.content)


def check_y():
    url = 'http://weixin.sogou.com/weixin?query=chuangbiandao&type=1'
    res = s.get(url, headers=headers, cookies=cookies, timeout=REQUESTS_TIME_OUT)
    print(res.content)


def manual_cookies():
    """
    获取 cookies - 手动填验证码
    :return:
    """
    anti_spider()
    code_img_save()

    # 模拟用户行为
    pv_refresh()
    pv_index()
    pv_img_cost()

    # 模拟鼠标滑过
    pv_mouse()
    pv_img_success()
    pv_real_index()

    # 模拟表单输入
    pv_seccode_focus()
    pv_seccode_input()
    pv_seccode_blur()

    input_code = input('code << ')

    thank(input_code)

    return _get_cookies()


def auto_cookies():
    """
    获取 cookies - 第三方识别验证码
    :return:
    """
    anti_spider()

    im = code_img_obj()
    # 6位英数混合 白天:15快豆 夜间:18.75快豆 超时:60秒
    img_id, img_code = get_img_code(im, im_type_id=3060)
    if not img_id:
        return None
    print(img_id, img_code)

    # 模拟用户行为
    pv_refresh()
    pv_index()
    pv_img_cost()

    # 模拟鼠标滑过
    pv_mouse()
    pv_img_success()
    pv_real_index()

    # 模拟表单输入
    pv_seccode_focus()
    pv_seccode_input()
    pv_seccode_blur()

    # 重试3次
    c = 3
    while c > 0:
        c -= 1
        res = thank(img_code)
        if res.get('code') == 0:
            # 识别成功
            cookies['SNUID'] = res.get('id', '')
            break
        elif res.get('code') == 3:
            # 报告错误识别
            img_report_error(img_id)

            # 出错随机等待后重试
            time.sleep(random.randint(1, 5))

            # 换张图片再来一次
            im = code_img_obj()
            # 6位英数混合 白天:15快豆 夜间:18.75快豆 超时:60秒
            img_id, img_code = get_img_code(im, im_type_id=3060)
            print(img_id, img_code)
        else:
            print('Error')
            print(res)
            return None

    return _get_cookies() if c > 0 else None


if __name__ == '__main__':
    # manual_cookies()
    auto_cookies()
    # check_n()
    # check_y()
