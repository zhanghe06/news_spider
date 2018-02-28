#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: anti_spider_weixin.py
@time: 2018-02-10 17:24
"""


from __future__ import print_function
from __future__ import unicode_literals
from future.builtins import input               # PY2(raw_input)

import random
import time
import json

from lxml.html import fromstring

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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
}


def _get_tc():
    tc = str('%13d' % (time.time() * 1000))
    return tc


def _save_img(res):
    # 保存验证码图片
    img_name = 'weixin_%s.jpg' % _get_tc()
    print('图片名称: %s' % img_name)
    img_content = res.content
    with open(img_name, b'w') as f:
        f.write(img_content)
    time.sleep(1)


def anti_spider(url):
    # url = 'https://mp.weixin.qq.com/profile?src=3&timestamp=1512923946&ver=1&signature=RZh61VIthXnp4HUsow1pgQXJbGxi*v-n4Pr1W6e5PVkmJSbRknd6LMT-EFoQqX4gaM6uGyHREmDPsN6lXkeYfg=='

    request_headers = headers.copy()
    request_headers['Host'] = 'mp.weixin.qq.com'

    res = s.get(url, headers=request_headers, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    print('.', end='')

    doc = fromstring(res.text)
    title = u''.join(i.strip() for i in doc.xpath('//title/text()'))
    print(title)
    return title == '请输入验证码'


def code_img_save():
    url = 'https://mp.weixin.qq.com/mp/verifycode'

    request_headers = headers.copy()
    request_headers['Host'] = 'mp.weixin.qq.com'

    request_cookie = cookies.copy()

    params = {
        'cert': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)

    # 保存图片
    _save_img(res)

    cookies.update(res.cookies)
    print('.', end='')
    # print cookies


def code_img_obj():
    url = 'https://mp.weixin.qq.com/mp/verifycode'

    request_headers = headers.copy()
    request_headers['Host'] = 'mp.weixin.qq.com'

    request_cookie = cookies.copy()

    params = {
        'cert': _get_tc(),
    }
    res = s.get(url, params=params, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    print('.', end='')
    return res.content


def verify_code(input_code):
    url = 'https://mp.weixin.qq.com/mp/verifycode'
    request_headers = headers.copy()
    request_headers['Host'] = 'mp.weixin.qq.com'
    request_headers['X-Requested-With'] = 'XMLHttpRequest'

    request_cookie = cookies.copy()

    data = {
        'cert': _get_tc(),
        'input': input_code,
        'appmsg_token': '',
    }

    res = s.post(url, data=data, headers=request_headers, cookies=request_cookie, timeout=REQUESTS_TIME_OUT)
    cookies.update(res.cookies)
    # print cookies

    json_msg = json.loads(res.content)
    print(json_msg)
    return json_msg
    # {u'cookie_count': 0, u'errmsg': u'', u'ret': 0}
    # {u'cookie_count': 0, u'errmsg': u'', u'ret': 501} 验证码有误


def _get_cookies():
    print(cookies)
    return cookies


def manual_cookies():
    url = input('url << ')
    anti_spider(url)
    code_img_save()

    input_code = input('code << ')

    verify_code(input_code)

    return _get_cookies()


def auto_cookies(url):
    need_status = anti_spider(url)
    if not need_status:
        return True

    im = code_img_obj()
    # 4位纯英文字母 白天:10快豆 夜间:12.5快豆 超时:60秒
    img_id, img_code = get_img_code(im, im_type_id=2040)
    print(img_id, img_code)

    # 重试3次
    c = 3
    while c > 0:
        c -= 1
        res = verify_code(img_code)
        if res.get('ret') == 0:
            # 识别成功
            break
        elif res.get('ret') == 501:
            # 报告错误识别
            img_report_error(img_id)

            # 出错随机等待后重试
            time.sleep(random.randint(1, 5))

            # 换张图片再来一次
            im = code_img_obj()
            # 4位纯英文字母 白天:10快豆 夜间:12.5快豆 超时:60秒
            img_id, img_code = get_img_code(im, im_type_id=2040)
            print(img_id, img_code)
        else:
            print('Error')
            print(res)
            return False

    return True if c > 0 else False


if __name__ == '__main__':
    # manual_cookies()
    anti_spider_url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1513650933&ver=1&signature=zzgwSdnYIm68Nu5eFz1X8-Heqjojhy4ozHmg4cUz*hEo*QuXma9-qkMrOFxzOGDfzJHHfyechg0AVCFPpsXpuA=='
    print(auto_cookies(anti_spider_url))
