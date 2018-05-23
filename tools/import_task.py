#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: import_csv.py
@time: 2018-05-17 18:46
"""

from __future__ import print_function
from __future__ import unicode_literals

import sys
import csv
import json
from apps.client_db import add_item
from models.news import FetchTask


def read_csv(filename):
    """
    读取csv
    :param filename:
    :return:
    """
    count = 0
    with open(filename) as f:
        reader = csv.DictReader(f)
        for line in reader:
            print(json.dumps(line, indent=4, ensure_ascii=False))
            count += 1
            yield line
    print('读取数量: %s' % count)


def import_csv(filename):
    """
    导入csv
    :param filename:
    :return:
    """
    count = 0
    for item in read_csv(filename):
        result = add_item(FetchTask, item)
        print(result)
        count += 1
    print('导入数量: %s' % count)


def usage():
    print('''
导入 csv
注意 csv 格式, 表头与数据库任务表的字段对应（去掉主键）
$ python tools/import_task.py example.csv
''')


def run():
    """
    入口
    """
    # print sys.argv
    try:
        if len(sys.argv) < 2:
            raise Exception('缺失参数\n')
        import_csv(sys.argv[1])
    except Exception as e:
        print('导入异常')
        print(e)
        usage()


if __name__ == '__main__':
    run()
