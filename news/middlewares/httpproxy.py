# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


from scrapy.exceptions import NotConfigured
from tools.proxies import get_proxy, del_proxy


class HttpProxyMiddleware(object):
    """
    代理中间件
    """
    def __init__(self, settings):
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST') or 1

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
        # 当前请求代理（保证重试过程，代理一致）
        request_proxy = request.meta.get('proxy') or get_proxy(spider.name)
        request.meta['proxy'] = request_proxy
        spider.log(request.meta)

    def process_exception(self, request, exception, spider):
        error_proxy = request.meta.get('proxy')
        if not error_proxy:
            return None
        # 重试失败（默认重试2次，共请求3次），删除代理
        if request.meta.get('retry_times', 0) >= self.max_retry_times:
            del_proxy(spider.name, error_proxy)
            spider.log('%s del proxy: %s, error reason: %s' % (spider.name, error_proxy, exception))
            return None
