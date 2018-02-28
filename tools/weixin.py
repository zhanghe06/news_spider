#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weixin.py
@time: 2018-02-10 17:55
"""


import os
import re
import time
import hashlib
import urlparse

import execjs
from tools.char import un_escape
from config import current_config


BASE_DIR = current_config.BASE_DIR


def get_finger(content_str):
    """
    :param content_str:
    :return:
    """
    m = hashlib.md5()
    m.update(content_str.encode('utf-8') if isinstance(content_str, unicode) else content_str)
    finger = m.hexdigest()
    return finger


def parse_weixin_js_body(html_body, url=''):
    """
    解析js
    :param html_body:
    :param url:
    :return:
    """
    rule = ur'<script type="text/javascript">.*?document.domain="qq.com";(.*?)seajs.use\("sougou/profile.js"\);.*?</script>'
    js_list = re.compile(rule, re.S).findall(html_body)
    if not js_list:
        print('parse error url: %s' % url)
    return u''.join(js_list)


def parse_weixin_article_id(html_body):
    rule = ur'<script nonce="(\d+)" type="text\/javascript">'
    article_id_list = re.compile(rule, re.I).findall(html_body)
    return article_id_list[0]


def add_img_src(html_body):
    rule = ur'data-src="(.*?)"'
    img_data_src_list = re.compile(rule, re.I).findall(html_body)
    print img_data_src_list
    for img_src in img_data_src_list:
        print img_src
        html_body = html_body.replace(img_src, u'%(img_src)s" src="%(img_src)s' % {'img_src': img_src})
    return html_body


def get_img_src_list(html_body, host_name='/', limit=None):
    rule = ur'src="(%s.*?)"' % host_name
    img_data_src_list = re.compile(rule, re.I).findall(html_body)
    if limit:
        return img_data_src_list[:limit]
    return img_data_src_list


class ParseJsWc(object):
    """
    解析微信动态数据
    """
    def __init__(self, js_body):
        self.js_body = js_body

        self._add_js_msg_list_fn()

        self.ctx = execjs.compile(self.js_body)
        print self.ctx

    def _add_js_msg_list_fn(self):
        js_msg_list_fn = u"""
        function r_msg_list() {
            return msgList.list;
        };
        """
        self.js_body += js_msg_list_fn

    def parse_js_msg_list(self):
        msg_list = self.ctx.call('r_msg_list')
        app_msg_ext_info_list = [i['app_msg_ext_info'] for i in msg_list]
        comm_msg_info_date_time_list = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['comm_msg_info']['datetime'])) for i in msg_list]
        # msg_id_list = [i['comm_msg_info']['id'] for i in msg_list]
        msg_data_list = [
            {
                # 'article_id': '%s_000' % msg_id_list[index],
                'article_id': get_finger(i['title']),
                'article_url': urlparse.urljoin('https://mp.weixin.qq.com', un_escape(i['content_url'])),
                'article_title': i['title'],
                'article_abstract': i['digest'],
                'article_pub_time': comm_msg_info_date_time_list[index],
            } for index, i in enumerate(app_msg_ext_info_list)
        ]
        msg_ext_list = [i['multi_app_msg_item_list'] for i in app_msg_ext_info_list]
        for index_j, j in enumerate(msg_ext_list):
            for index_i, i in enumerate(j):
                msg_data_list.append(
                    {
                        # 'article_id': '%s_%03d' % (msg_id_list[index_j], index_i + 1),
                        'article_id': get_finger(i['title']),
                        'article_url': urlparse.urljoin('https://mp.weixin.qq.com', un_escape(i['content_url'])),
                        'article_title': i['title'],
                        'article_abstract': i['digest'],
                        'article_pub_time': comm_msg_info_date_time_list[index_j],
                    }
                )
        return msg_data_list
