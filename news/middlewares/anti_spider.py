# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import time
from scrapy.exceptions import IgnoreRequest
from scrapy.exceptions import NotConfigured

from tools.cookies import del_cookies
from tasks.jobs_weixin import set_anti_spider_task, sub_anti_spider


class AntiSpiderMiddleware(object):
    """
    反爬中间件
    配置说明:
        RETRY_ENABLED 默认: True
        RETRY_TIMES 默认: 2
        RETRY_HTTP_CODES 默认: [500, 502, 503, 504, 400, 408]
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
        # 处理微信反爬(反爬机制一, sogou)
        if spider.name in ['weixin'] and 'antispider' in request.url:
            # 获取来源链接
            redirect_urls = request.meta['redirect_urls']

            # 清理失效 cookies
            cookies_id = request.meta['cookiejar']
            del_cookies(spider.name, cookies_id)

            # spider.log(message='AntiSpider cookies_id: %s; url: %s' % (cookies_id, redirect_urls[0]))
            raise IgnoreRequest("Spider: %s, AntiSpider cookies_id: %s; url: %s" % (spider.name, cookies_id, redirect_urls[0]))

    def process_response(self, request, response, spider):
        # 处理微信反爬(反爬机制二, weixin)
        if spider.name in ['weixin']:
            title = response.xpath('//title/text()').extract_first(default=u'').strip()
            if title == u'请输入验证码':
                # 设置反爬处理任务
                msg = {
                    'url': response.url,
                    'time': time.strftime("%Y-%m-%d %H:%M:%S")
                }
                set_anti_spider_task(spider.name, msg)

                # 订阅处理结果
                anti_spider_result = sub_anti_spider(spider.name)
                if not anti_spider_result.get('status'):
                    return response

                # 请求重试
                retry_req = request.copy()
                retry_req.dont_filter = True  # 必须设置(禁止重复请求被过滤掉)
                retry_req.priority = request.priority + self.priority_adjust
                return retry_req
        return response
