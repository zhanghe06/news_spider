# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


class ContentTypeGb2312Middleware(object):
    """
    处理不规范的页面（优先级降低至580之后才能生效）
    原因:
        默认配置的 DOWNLOADER_MIDDLEWARES 包含 MetaRefreshMiddleware
        当请求页面存在如 Content-Location 类似的 header 时, 会触发重定向请求
    指定 Content-Type 为 gb2312
    """
    def process_response(self, request, response, spider):
        response.headers['Content-Type'] = 'text/html; charset=gb2312'
        return response
