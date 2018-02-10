#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: jobs_sogou.py
@time: 2018-02-10 18:05
"""


from tools.cookies import add_cookies
from tools.anti_spider_sogou import auto_cookies as sogou_cookies
from apps.client_rk import rk_counter_client, check_counter_limit, check_cookies_count


def job_sogou_cookies(spider_name):
    """
    sogou cookies
    :return:
    """
    # 判断每天限制额度
    if not check_counter_limit():
        print('spider_name: %s, There is not enough available quantity' % spider_name)
        return False

    # 判断 cookie 队列长度
    if not check_cookies_count(spider_name):
        print('spider_name: %s, The quantity of cookies is enough' % spider_name)
        return False

    sogou_cookies_obj = sogou_cookies()

    if not sogou_cookies_obj:
        return False

    add_cookies(spider_name, sogou_cookies_obj)
    rk_counter_client.increase(1)
    return True


if __name__ == '__main__':
    job_sogou_cookies('weixin')
