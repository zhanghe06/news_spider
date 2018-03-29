#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: img.py
@time: 2018-03-20 14:24
"""


from __future__ import print_function
from __future__ import unicode_literals

import imghdr

import requests
from PIL import Image
from six import BytesIO

from config import current_config

REQUESTS_TIME_OUT = current_config.REQUESTS_TIME_OUT


def filter_img_size(min_width=0, min_height=0, *img_url):
    """
    过滤尺寸不符要求的图片
    :param min_width:
    :param min_height:
    :param img_url:
    :return:
    """
    result = []
    for i in img_url:
        try:
            img_res = requests.get(i, stream=True, timeout=REQUESTS_TIME_OUT)
            if img_res.status_code == 200:
                orig_image = Image.open(BytesIO(img_res.content))
                img_width, img_height = orig_image.size
                if img_width >= min_width and img_height >= min_height:
                    result.append(i)
        except Exception as e:
            print('check images error: %s' % img_url)
            print(e.message)
            continue
    return result


def filter_local_img_type(ignore_type='gif', *img_path):
    """
    过滤指定类型本地图片
    :param ignore_type:
    :param img_path:
    :return:
    """
    result = []
    for i in img_path:
        img_type = imghdr.what(i)
        # print(img_type, i)
        if img_type == ignore_type:
            continue
        result.append(i)
    return result


def filter_remote_img_type(ignore_type='gif', *img_url):
    """
    过滤指定类型远程图片
    :param ignore_type:
    :param img_url:
    :return:
    """
    result = []
    for i in img_url:
        img_type = imghdr.what(None, requests.get(i).content)
        # print(img_type, i)
        if img_type == ignore_type:
            continue
        result.append(i)
    return result


if __name__ == '__main__':
    pass
