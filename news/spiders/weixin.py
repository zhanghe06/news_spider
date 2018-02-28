# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

import scrapy

from models.news import FetchTask
from news.items import FetchResultItem
from apps.client_db import get_item
from maps.platform import platform_name_map
from maps.channel import channel_name_map
from tools.url import get_update_url
from tools.weixin import parse_weixin_js_body, ParseJsWc
from tools.cookies import get_cookies
from tools.scrapy_tasks import pop_task


class WeixinSpider(scrapy.Spider):
    """
    微信公众号蜘蛛
    因微信公众号详情链接是带有效期签名的动态链接, 故无法使用请求去重中间件
    """
    name = 'weixin'
    allowed_domains = ['mp.weixin.qq.com', 'weixin.qq.com', 'qq.com', 'sogou.com']

    custom_settings = dict(
        COOKIES_ENABLED=True,
        DEFAULT_REQUEST_HEADERS={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
        },
        USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        DOWNLOADER_MIDDLEWARES={
            # 'news.middlewares.de_duplication_request.DeDuplicationRequestMiddleware': 140,  # 去重请求
            'news.middlewares.anti_spider.AntiSpiderMiddleware': 160,  # 反爬处理
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'news.middlewares.useragent.UserAgentMiddleware': 500,
        },
        ITEM_PIPELINES={
            'news.pipelines.de_duplication_store_mysql.DeDuplicationStoreMysqlPipeline': 400,  # 去重存储
            # 'news.pipelines.img_remote_to_local_fs.ImgRemoteToLocalFSPipeline': 440,
            'news.pipelines.store_mysql.StoreMysqlPipeline': 450,
            # 'news.pipelines.de_duplication_request.DeDuplicationRequestPipeline': 500,  # 去重请求
        },
        DOWNLOAD_DELAY=0.5
    )
    cookies = {}

    def start_requests(self):
        """
        入口准备
        :return:
        """
        boot_url = 'http://weixin.sogou.com/weixin'

        task_id = pop_task(self.name)

        if not task_id:
            print('%s task is empty' % self.name)
            return
        print('%s task id: %s' % (self.name, task_id))

        task_item = get_item(FetchTask, task_id)

        cookies_id, cookies = get_cookies(self.name)
        url_params = {
            'type': 1,
            # 'query': task_item.follow_id,
            'query': task_item.follow_name.encode('utf-8'),
        }
        url_profile = get_update_url(boot_url, url_params)
        meta = {
            'cookiejar': cookies_id,
            'task_id': task_item.id,
            'platform_id': task_item.platform_id,
            'channel_id': task_item.channel_id,
            'follow_id': task_item.follow_id,
            'follow_name': task_item.follow_name,
        }

        yield scrapy.Request(url=url_profile, cookies=cookies, callback=self.parse_account_search_list, meta=meta)

    def parse_article_search_list(self, response):
        """
        解析微信文章 搜索列表页面 (废弃)
        :param response:
        :return:
        """
        news_links = response.xpath('//div[@class="txt-box"]/h3/a/@href').extract()
        for new_link in news_links:
            yield scrapy.Request(url=new_link, callback=self.parse_detail)

    def parse_account_search_list(self, response):
        """
        解析公众账号 搜索列表页面
        :param response:
        :return:
        """
        account_link = response.xpath('//div[@class="txt-box"]//a/@href').extract_first()
        if account_link:
            yield scrapy.Request(url=account_link, callback=self.parse_account_article_list, meta=response.meta)

    def parse_account_article_list(self, response):
        """
        解析公众账号 文章列表页面
        :param response:
        :return:
        """
        article_list_body = response.body_as_unicode()
        js_body = parse_weixin_js_body(article_list_body)
        if not js_body:
            return
        pj = ParseJsWc(js_body=js_body)
        article_list = pj.parse_js_msg_list()

        for article_item in article_list:
            meta = dict(response.meta, **article_item)
            yield scrapy.Request(url=article_item['article_url'], callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):
        """
        详细页面
        :param response:
        :return:
        """
        article_content = ''.join([i.strip() for i in response.xpath('//div[@id="js_content"]/*').extract()])

        # 原创内容处理（处理内容为空）
        if not article_content:
            share_source_url = response.xpath('//a[@id="js_share_source"]/@href').extract_first()
            yield scrapy.Request(url=share_source_url, callback=self.parse_detail, meta=response.meta)
            return

        fetch_result_item = FetchResultItem()
        fetch_result_item['task_id'] = response.meta['task_id']
        fetch_result_item['platform_id'] = response.meta['platform_id']
        fetch_result_item['platform_name'] = platform_name_map.get(response.meta['platform_id'], '')
        fetch_result_item['channel_id'] = response.meta['channel_id']
        fetch_result_item['channel_name'] = channel_name_map.get(response.meta['channel_id'], '')
        fetch_result_item['article_id'] = response.meta['article_id']
        fetch_result_item['article_title'] = response.meta['article_title']
        fetch_result_item['article_author_id'] = response.meta['follow_id']
        fetch_result_item['article_author_name'] = response.meta['follow_name']
        fetch_result_item['article_pub_time'] = response.meta['article_pub_time']
        fetch_result_item['article_url'] = response.meta['article_url']
        fetch_result_item['article_tags'] = ''
        fetch_result_item['article_abstract'] = response.meta['article_abstract']
        fetch_result_item['article_content'] = article_content

        yield fetch_result_item
