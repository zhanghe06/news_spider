# -*- coding: utf-8 -*-
import scrapy


class IpSpider(scrapy.Spider):
    """
    IP代理测试 蜘蛛
    重试3次，每次超时10秒
    使用：
    进入项目目录
    $ scrapy crawl ip
    """
    name = "ip"
    allowed_domains = ["ip.cn"]
    start_urls = (
        'https://ip.cn',
    )

    custom_settings = dict(
        COOKIES_ENABLED=True,
        DEFAULT_REQUEST_HEADERS={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
        },
        USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        DOWNLOADER_MIDDLEWARES={
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'news.middlewares.useragent.UserAgentMiddleware': 500,
            'news.middlewares.httpproxy.HttpProxyMiddleware': 720,  # 代理（cookie需要与代理IP关联）
        },
        ITEM_PIPELINES={
            'news.pipelines.store_mysql.StoreMysqlPipeline': 450,
        },
        DOWNLOAD_TIMEOUT=10
    )

    def parse(self, response):
        info = response.xpath('//div[@class="well"]//code/text()').extract()
        ip_info = dict(zip(['ip', 'address'], info))
        yield ip_info
