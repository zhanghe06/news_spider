#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: jobs_weixin.py
@time: 2018-02-10 18:06
"""


import json
import time
import sys

from libs.redis_pub_sub import RedisPubSub
from libs.redis_queue import RedisQueue
from tools.anti_spider_weixin import auto_cookies as weixin_cookies
from apps.client_db import redis_client
from apps.client_rk import rk_counter_client, check_counter_limit


def set_anti_spider_task(spider_name, msg):
    """
    设置任务队列
    msg = {
        'url': url,
        'time': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    :param spider_name:
    :param msg:
    :return:
    """
    key = 'anti_spider_task_weixin:%s' % spider_name
    q_task = RedisQueue(key, redis_client=redis_client)
    q_msg = json.dumps(msg) if isinstance(msg, dict) else msg
    # 因为微信反爬策略是通过IP限制, 这里仅仅处理一个任务
    if q_task.empty():
        q_task.put(q_msg)


def _get_anti_spider_task(spider_name):
    """获取任务队列"""
    key = 'anti_spider_task_weixin:%s' % spider_name
    q_task = RedisQueue(key, redis_client=redis_client)
    result = q_task.get(timeout=60)
    return json.loads(result) if result else {}


def _set_anti_spider_result(spider_name, msg):
    """设置结果队列"""
    key = 'anti_spider_result_weixin:%s' % spider_name
    q_result = RedisQueue(key, redis_client=redis_client)
    q_msg = json.dumps(msg) if isinstance(msg, dict) else msg
    q_result.put(q_msg)


def _get_anti_spider_result(spider_name):
    """获取任务队列"""
    key = 'anti_spider_result_weixin:%s' % spider_name
    q_result = RedisQueue(key, redis_client=redis_client)
    result = q_result.get(timeout=60)
    return json.loads(result) if result else {}


def sub_anti_spider(spider_name):
    """
    蜘蛛订阅验证码处理结果
    :param spider_name:
    :return:
    """
    q = RedisPubSub('anti_spider', redis_client=redis_client)
    r = q.sub_not_loop(spider_name)
    return json.loads(r) if r else {}


def _pub_anti_spider(spider_name, msg):
    """
    将对应蜘蛛的验证码处理结果发布给对应订阅者
    :param spider_name:
    :return:
    """
    q = RedisPubSub('anti_spider', redis_client=redis_client)
    msg = json.dumps(msg) if isinstance(msg, dict) else msg
    q.pub(spider_name, msg)


def job_weixin_cookies(spider_name):
    """
    weixin cookies
    :return:
    """
    # 判断每天限制额度
    if not check_counter_limit():
        print('spider_name: %s, There is not enough available quantity' % spider_name)
        return False

    # 读取验证码任务队列(超时1分钟)
    task = _get_anti_spider_task(spider_name)
    if not task:
        return False

    # 设置验证码结果队列
    url = task.get('url')
    msg = {
        'url': url,
        'status': False,
        'time': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        weixin_cookies_status = weixin_cookies(url)
        msg['status'] = weixin_cookies_status

        _set_anti_spider_result(spider_name, msg)

        # 读取验证码结果队列(超时1分钟)
        msg = _get_anti_spider_result(spider_name)

        _pub_anti_spider(spider_name, msg)
        rk_counter_client.increase(1)
        return True
    except Exception as e:
        print(e.message)
        _pub_anti_spider(spider_name, msg)


def usage():
    print('python tasks/jobs_weixin.py <function> <spider_name>')
    print('\tpython tasks/jobs_weixin.py job_weixin_cookies weixin')


def run():
    """
    启动入口
    """
    # print sys.argv
    try:
        if len(sys.argv) >= 3:
            fun_name = globals()[sys.argv[1]]
            fun_name(sys.argv[2])
        else:
            usage()
    except NameError, e:
        print e


if __name__ == '__main__':
    job_weixin_cookies('weixin')
    # run()
    # python tasks/jobs_weixin.py job_weixin_cookies weixin
