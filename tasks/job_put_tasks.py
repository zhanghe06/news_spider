#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: job_put_tasks.py
@time: 2018-02-10 17:16
"""

import sys

from models.news import FetchTask, FetchResult, LogTaskScheduling
from apps.client_db import get_group, get_all
from maps.platform import WEIXIN, WEIBO, TOUTIAO
from tools.scrapy_tasks import put_task, get_tasks_count


def job_put_tasks(spider_name):
    # 如果任务队列没有消耗完毕, 不处理
    tasks_count = get_tasks_count(spider_name)
    if tasks_count:
        return True

    spider_map = {
        'weixin': WEIXIN,
        'weibo': WEIBO,
        'toutiao': TOUTIAO,
        'toutiao_m': TOUTIAO,
    }

    # TODO 稳定运行之后需要去掉
    # task_exclude = [i.task_id for i in get_group(FetchResult, 'task_id', min_count=1)]

    task_list = get_all(FetchTask, FetchTask.platform_id == spider_map.get(spider_name))

    c = 0
    for task in task_list:
        # 排除任务
        # if task.id in task_exclude:
        #     continue
        put_task(spider_name, task.id)
        c += 1
        if c % 100 == 0:
            print(c)
    print('put %s tasks count: %s' % (spider_name, c))
    return True


def usage():
    contents = [
        'Example:',
        '\tpython job_put_tasks.py wx  # 微信',
        '\tpython job_put_tasks.py wb  # 微博',
        '\tpython job_put_tasks.py tm  # 头条(M)',
        '\tpython job_put_tasks.py tt  # 头条(PC)',
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
        'tm': 'toutiao_m',
    }
    try:
        if len(sys.argv) > 1:
            spider_name = spider_name_maps.get(sys.argv[1])
            if not spider_name:
                raise Exception('参数错误')
            job_put_tasks(spider_name)
        else:
            raise Exception('缺失参数')
    except Exception as e:
        print(e.message)
        usage()


if __name__ == '__main__':
    run()
