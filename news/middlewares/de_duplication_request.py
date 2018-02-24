# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


from scrapy.exceptions import IgnoreRequest

from tools.duplicate import is_dup_detail


class DeDuplicationRequestMiddleware(object):
    """
    去重 - 请求
    (数据结构：集合)
    """
    def process_request(self, request, spider):
        if not request.url:
            return None
        if spider.name in ['weixin', 'weixin_check_gh']:
            if is_dup_detail(request.url, spider.name):
                raise IgnoreRequest("Spider: %s, DeDuplicationRequest: %s" % (spider.name, request.url))
        elif is_dup_detail(request.url, spider.name):
            raise IgnoreRequest("Spider: %s, DeDuplicationRequest: %s" % (spider.name, request.url))
