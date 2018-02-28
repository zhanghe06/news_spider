#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: toutiao.py
@time: 2018-02-28 14:14
"""

import hashlib
import math
import re
import time

import execjs

from tools.char import un_escape


def get_as_cp():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS, CP


def parse_toutiao_js_body(html_body, url=''):
    """
    解析js
    :param html_body:
    :param url:
    :return:
    """
    rule = r'<script>(var BASE_DATA = {.*?};)</script>'
    js_list = re.compile(rule, re.S).findall(html_body)
    if not js_list:
        print('parse error url: %s' % url)
    return ''.join(js_list)


class ParseJsTt(object):
    """
    解析头条动态数据
    """

    def __init__(self, js_body):
        self.js_body = js_body

        self._add_js_item_id_fn()
        self._add_js_title_fn()
        self._add_js_abstract_fn()
        self._add_js_content_fn()
        self._add_js_pub_time()
        self._add_js_tags_fn()

        self.ctx = execjs.compile(self.js_body)

    def _add_js_item_id_fn(self):
        js_item_id_fn = """
        function r_item_id() {
            return BASE_DATA.articleInfo.itemId;
        };
        """
        self.js_body += js_item_id_fn

    def _add_js_title_fn(self):
        js_title_fn = """
        function r_title() {
            return BASE_DATA.articleInfo.title;
        };
        """
        self.js_body += js_title_fn

    def _add_js_abstract_fn(self):
        js_abstract_fn = """
        function r_abstract() {
            return BASE_DATA.shareInfo.abstract;
        };
        """
        self.js_body += js_abstract_fn

    def _add_js_content_fn(self):
        js_content_fn = """
        function r_content() {
            return BASE_DATA.articleInfo.content;
        };
        """
        self.js_body += js_content_fn

    def _add_js_pub_time(self):
        js_pub_time_fn = """
                function r_pub_time() {
                    return BASE_DATA.articleInfo.subInfo.time;
                };
                """
        self.js_body += js_pub_time_fn

    def _add_js_tags_fn(self):
        js_tags_fn = """
        function r_tags() {
            return BASE_DATA.articleInfo.tagInfo.tags;
        };
        """
        self.js_body += js_tags_fn

    def parse_js_item_id(self):
        return self.ctx.call('r_item_id') or ''

    def parse_js_title(self):
        return self.ctx.call('r_title') or ''

    def parse_js_abstract(self):
        return self.ctx.call('r_abstract') or ''

    def parse_js_content(self):
        return un_escape(self.ctx.call('r_content')) or ''

    def parse_js_pub_time(self):
        return self.ctx.call('r_pub_time') or time.strftime('%Y-%m-%d %H:%M:%S')

    def parse_js_tags(self):
        return ','.join([tag['name'] or '' for tag in self.ctx.call('r_tags')])


if __name__ == '__main__':
    print(get_as_cp())
