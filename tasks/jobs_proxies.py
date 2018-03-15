#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: jobs_proxies.py
@time: 2018-03-13 17:22
"""


from __future__ import print_function

import sys

from tools.proxies import add_proxy, len_proxy, fetch_proxy


def job_proxies(spider_name, mix_num=0):
    if len_proxy(spider_name) <= mix_num:
        proxy_list = fetch_proxy()
        if not proxy_list:
            return
        add_proxy(spider_name, *proxy_list)
        print('%s add proxies: %s' % (spider_name, len(proxy_list)))


def usage():
    contents = [
        'Example:',
        '\tpython jobs_proxies.py ip  # 测试',
        '\tpython jobs_proxies.py wx  # 微信',
        '\tpython jobs_proxies.py wb  # 微博',
        '\tpython jobs_proxies.py tt  # 头条',
    ]
    print('\n'.join(contents))


def run():
    """
    入口
    """
    # print(sys.argv)
    spider_name_maps = {
        'wx': 'weixin',
        'wb': 'weibo',
        'tt': 'toutiao',
    }
    try:
        if len(sys.argv) > 1:
            spider_name = spider_name_maps.get(sys.argv[1], sys.argv[1])
            if not spider_name:
                raise Exception('参数错误')
            job_proxies(spider_name)
        else:
            raise Exception('缺失参数')
    except Exception as e:
        print(e.message)
        usage()


if __name__ == '__main__':
    run()
