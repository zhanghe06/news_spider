#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weibo.py
@time: 2018-02-13 16:20
"""


import base64
import urllib

import re
from lxml.html import fromstring


def get_su(user_name):
    return base64.b64encode(urllib.quote(user_name.strip()))


def get_login_data():
    return {
        'username': '******',
        'password': '******'
    }


def parse_article_list_js(article_list_body):
    # 页面解析(微博是JS动态数据, 无法直接解析页面)
    print(type(article_list_body))
    print(len(article_list_body))
    print(article_list_body)

    # with open('a.html', 'wb') as f:
    #     f.write(article_list_body.encode('utf-8'))
    article_list_rule = ur'<script>FM.view\({"ns":"pl.content.miniTab.index","domid":"Pl_Core_ArticleList__\d+".*?"html":"(.*?)"}\)</script>'
    article_list_re_parse = re.compile(article_list_rule, re.S).findall(article_list_body)
    if not article_list_re_parse:
        return
    article_list_html = u''.join(article_list_re_parse)
    # with open('b.html', 'wb') as f:
    #     f.write(article_list_html.encode('utf-8'))

    article_list_doc = fromstring(article_list_html)
    print(article_list_doc)

    article_list_doc_parse = article_list_doc.xpath('//div[@class="text_box"]')
    print(article_list_doc_parse)

    for article_item in article_list_doc_parse:
        print('-' * 200)
        article_detail_url = article_item.xpath('./div[@class="title W_autocut"]/a[@class="W_autocut S_txt1"]/@href')
        article_detail_title = article_item.xpath('./div[@class="title W_autocut"]/a[@class="W_autocut S_txt1"]/text()')
        article_detail_abstract = article_item.xpath('./div[@class="text"]/a[@class="S_txt1"]/text()')
        if not (article_detail_url and article_detail_title):
            continue
        article_detail_url = article_detail_url[0].strip().replace('\/', '/')
        # article_detail_url = response.urljoin(article_detail_url)
        article_detail_title = article_detail_title[0].strip()

        meta_article_item = {
            'article_url': article_detail_url,
            'article_title': article_detail_title,
            'article_abstract': article_detail_abstract,
        }
        print(meta_article_item)

if __name__ == '__main__':
    pass

