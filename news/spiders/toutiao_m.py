# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

import json
import time

import scrapy

from apps.client_db import get_item
from maps.channel import channel_name_map
from maps.platform import platform_name_map
from models.news import FetchTask
from news.items import FetchResultItem
from tools.scrapy_tasks import pop_task
from tools.toutiao_m import get_as_cp, ParseJsTt, parse_toutiao_js_body
from tools.url import get_update_url


class ToutiaoMSpider(scrapy.Spider):
    """
    头条蜘蛛
    """
    name = 'toutiao_m'
    allowed_domains = ['toutiao.com', 'snssdk.com']

    custom_settings = dict(
        COOKIES_ENABLED=True,
        DEFAULT_REQUEST_HEADERS={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
        },
        USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        DOWNLOADER_MIDDLEWARES={
            'news.middlewares.de_duplication_request.DeDuplicationRequestMiddleware': 140,  # 去重请求
            # 'news.middlewares.anti_spider.AntiSpiderMiddleware': 160,  # 反爬处理
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'news.middlewares.useragent.UserAgentMiddleware': 500,
            # 'news.middlewares.httpproxy.HttpProxyMiddleware': 720,
        },
        ITEM_PIPELINES={
            'news.pipelines.de_duplication_store_mysql.DeDuplicationStoreMysqlPipeline': 400,  # 去重存储
            'news.pipelines.store_mysql.StoreMysqlPipeline': 450,
            'news.pipelines.de_duplication_request.DeDuplicationRequestPipeline': 500,  # 去重请求
        },
        DOWNLOAD_DELAY=0.5
    )

    # start_urls = ['http://toutiao.com/']
    # start_urls = ['https://www.toutiao.com/ch/news_finance/']

    def start_requests(self):
        """
        入口准备
        :return:
        """
        url_params = {
            'version_code': '6.4.2',
            'version_name': '',
            'device_platform': 'iphone',
            'tt_from': 'weixin',
            'utm_source': 'weixin',
            'utm_medium': 'toutiao_ios',
            'utm_campaign': 'client_share',
            'wxshare_count': '1',
        }

        task_id = pop_task(self.name)

        if not task_id:
            print('%s task is empty' % self.name)
            return
        print('%s task id: %s' % (self.name, task_id))

        task_item = get_item(FetchTask, task_id)
        fetch_url = 'http://m.toutiao.com/profile/%s/' % task_item.follow_id
        url_profile = get_update_url(fetch_url, url_params)
        meta = {
            'task_id': task_item.id,
            'platform_id': task_item.platform_id,
            'channel_id': task_item.channel_id,
            'follow_id': task_item.follow_id,
            'follow_name': task_item.follow_name,
        }
        yield scrapy.Request(url=url_profile, callback=self.get_profile, meta=meta)

    def get_profile(self, response):
        userid = response.xpath('//button[@itemid="topsharebtn"]/@data-userid').extract_first(default='')
        mediaid = response.xpath('//button[@itemid="topsharebtn"]/@data-mediaid').extract_first(default='')

        meta = dict(response.meta, userid=userid, mediaid=mediaid)

        url = 'http://open.snssdk.com/jssdk_signature/'
        url_params = {
            'appid': 'wxe8b89be1715734a6',
            'noncestr': 'Wm3WZYTPz0wzccnW',
            'timestamp': '%13d' % (time.time() * 1000),
            'callback': 'jsonp2',
        }
        url_jssdk_signature = get_update_url(url, url_params)
        yield scrapy.Request(url=url_jssdk_signature, callback=self.jssdk_signature, meta=meta)

    def jssdk_signature(self, response):
        AS, CP = get_as_cp()
        jsonp_index = 3

        url = 'https://www.toutiao.com/pgc/ma/'
        url_params = {
            'page_type': 1,
            'max_behot_time': '',
            'uid': response.meta['userid'],
            'media_id': response.meta['mediaid'],
            'output': 'json',
            'is_json': 1,
            'count': 20,
            'from': 'user_profile_app',
            'version': 2,
            'as': AS,
            'cp': CP,
            'callback': 'jsonp%d' % jsonp_index,
        }
        url_article_list = get_update_url(url, url_params)

        meta = dict(response.meta, jsonp_index=jsonp_index)

        yield scrapy.Request(url=url_article_list, callback=self.parse_article_list, meta=meta)

    def parse_article_list(self, response):
        """
        文章列表
        :param response:
        :return:
        """
        body = response.body_as_unicode()
        jsonp_text = 'jsonp%d' % response.meta.get('jsonp_index', 0)
        result = json.loads(body.lstrip('%s(' % jsonp_text).rstrip(')'))
        # 翻页
        has_more = result.get('has_more')
        if has_more:
            max_behot_time = result['next']['max_behot_time']
            AS, CP = get_as_cp()
            jsonp_index = response.meta.get('jsonp_index', 0) + 1

            url_params_next = {
                'max_behot_time': max_behot_time,
                'as': AS,
                'cp': CP,
                'callback': 'jsonp%d' % jsonp_index,
            }

            url_article_list_next = get_update_url(response.url, url_params_next)

            meta = dict(response.meta, jsonp_index=jsonp_index)
            yield scrapy.Request(url=url_article_list_next, callback=self.parse_article_list, meta=meta)
        # 详情
        data_list = result.get('data', [])
        for data_item in data_list:
            detail_url = data_item.get('source_url')
            meta = dict(response.meta, detail_url=detail_url)
            yield scrapy.Request(url=detail_url, callback=self.parse_article_detail, meta=meta)

    def parse_article_detail(self, response):
        """
        文章详情
        :param response:
        :return:
        """
        toutiao_body = response.body_as_unicode()
        js_body = parse_toutiao_js_body(toutiao_body, response.meta['detail_url'])
        if not js_body:
            return
        pj = ParseJsTt(js_body=js_body)

        article_id = pj.parse_js_item_id()
        article_title = pj.parse_js_title()
        article_abstract = pj.parse_js_abstract()
        article_content = pj.parse_js_content()
        article_pub_time = pj.parse_js_pub_time()
        article_tags = pj.parse_js_tags()

        fetch_result_item = FetchResultItem()
        fetch_result_item['task_id'] = response.meta['task_id']
        fetch_result_item['platform_id'] = response.meta['platform_id']
        fetch_result_item['platform_name'] = platform_name_map.get(response.meta['platform_id'], '')
        fetch_result_item['channel_id'] = response.meta['channel_id']
        fetch_result_item['channel_name'] = channel_name_map.get(response.meta['channel_id'], '')
        fetch_result_item['article_id'] = article_id
        fetch_result_item['article_title'] = article_title
        fetch_result_item['article_author_id'] = response.meta['follow_id']
        fetch_result_item['article_author_name'] = response.meta['follow_name']
        fetch_result_item['article_pub_time'] = article_pub_time
        fetch_result_item['article_url'] = response.url or response.meta['detail_url']
        fetch_result_item['article_tags'] = article_tags
        fetch_result_item['article_abstract'] = article_abstract
        fetch_result_item['article_content'] = article_content

        yield fetch_result_item
