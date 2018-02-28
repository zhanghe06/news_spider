#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: char.py
@time: 2018-02-10 17:48
"""


import execjs

# from HTMLParser import HTMLParser     # PY2
# from html.parser import HTMLParser    # PY3
from future.moves.html.parser import HTMLParser

html_parser = HTMLParser()


def un_escape(char_str):
    """
    反转译
    :param char_str:
    :return:
    """
    return html_parser.unescape(char_str)


def get_js_36_str(i):
    """
    整数、浮点数 js方式转36进制
    :param i:
    :return:
    """
    js_body = '''
        function get_36_str(i) {
            return i.toString(36);
        };
    '''
    ctx = execjs.compile(js_body)
    return ctx.call("get_36_str", i)


if __name__ == '__main__':
    a = '&#21152;&#20837;&#21040;&#34;&#25105;&#30340;&#20070;&#30446;&#36873;&#21333;&#34;&#20013;'
    b = '\xe5\xbd\x93\xe5\x89\x8d\xe5\xb7\xb2\xe8\xbe\xbe\xe5\x88\xb0\xe6\x8a\x93\xe5\x8f\x96\xe9\x85\x8d\xe7\xbd\xae\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe9\xa1\xb5\xe7\xa0\x81'
    c = 'https://mp.weixin.qq.com/s?timestamp=1511432702&amp;src=3&amp;ver=1&amp;signature=lAC8MtonFiHnlc5-j4z48WcPRpfP1Nn4zxCmY4ZjCjdXQscLcB5uyi5Jb395m5yaZQHTqqSlqzy*HRR0nAPZHsz0*Efu3w*Y2B8XbIL5v8pZQsGt9cwZQTuvI0GZqAsZobqzaeDptAQzHLB4QKL-qExOz0ANOTG*QAvJ7-ZurMg='
    d = 'http://mp.weixin.qq.com/mp/homepage?__biz=MzAxNzU2Mjc4NQ==&amp;hid=2&amp;sn=8177890cc7e468d3df6f3050d49951c5#wechat_redirect'
    print(un_escape(a))
    print(un_escape(b))
    print(un_escape(c))
    print(un_escape(d))
