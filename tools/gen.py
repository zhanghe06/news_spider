#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: gen.py
@time: 2018-02-10 17:19
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.inspection import inspect
from config import current_config


BASE_DIR = current_config.BASE_DIR
SQLALCHEMY_DATABASE_URI = current_config.SQLALCHEMY_DATABASE_URI_MYSQL


def gen_models():
    """
    创建 models
    $ python gen.py gen_models
    """
    file_path = os.path.join(BASE_DIR, 'models/news.py')
    cmd = 'sqlacodegen %s --noinflect --outfile %s' % (SQLALCHEMY_DATABASE_URI, file_path)

    output = os.popen(cmd)
    result = output.read()
    print(result)

    # 更新 model 文件
    with open(file_path, b'r') as f:
        lines = f.readlines()
    # 新增 model 转 dict 方法
    with open(file_path, b'w') as f:
        lines.insert(9, b'def to_dict(self):\n')
        lines.insert(10, b'    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}\n')
        lines.insert(11, b'\n')
        lines.insert(12, b'Base.to_dict = to_dict\n')
        lines.insert(13, b'\n\n')
        f.write(b''.join(lines))


def gen_items():
    """
    创建 items
    $ python gen.py gen_items
    字段规则： 去除自增主键，非自增是需要的。
    """
    from models import news

    file_path = os.path.join(BASE_DIR, 'news/items.py')

    model_list = [(k, v) for k, v in news.__dict__.items() if isinstance(v, DeclarativeMeta) and k != 'Base']

    with open(file_path, b'w') as f:
        f.write(b'# -*- coding: utf-8 -*-\n\n')
        f.write(b'# Define here the models for your scraped items\n#\n')
        f.write(b'# See documentation in:\n')
        f.write(b'# http://doc.scrapy.org/en/latest/topics/items.html\n\n')
        f.write(b'import scrapy\n')

        for model_name, model_class in model_list:
            result = model_class().to_dict()
            table_name = model_class().__tablename__
            model_pk = inspect(model_class).primary_key[0].name
            f.write(b'\n\nclass %sItem(scrapy.Item):\n' % model_name)
            f.write(b'    """\n')
            f.write(b'    table_name: %s\n' % table_name)
            f.write(b'    primary_key: %s\n' % model_pk)
            f.write(b'    """\n')
            for field_name in list(result.keys()):
                if field_name in [model_pk, 'create_time', 'update_time']:
                    continue
                f.write(b'    %s = scrapy.Field()\n' % field_name)


def run():
    """
    入口
    """
    # print sys.argv
    try:
        if len(sys.argv) > 1:
            fun_name = globals()[sys.argv[1]]
            fun_name()
        else:
            print('缺失参数\n')
            usage()
    except NameError as e:
        print(e)
        print('未定义的方法[%s]' % sys.argv[1])


def usage():
    print("""
创建 models
$ python gen.py gen_models

创建 items
$ python gen.py gen_items
""")


if __name__ == '__main__':
    run()
    # print BASE_DIR
    # print SQLALCHEMY_DATABASE_URI
