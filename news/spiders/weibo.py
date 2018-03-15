# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

import json
import re
import time
from datetime import datetime

import scrapy
import six
from lxml.html import fromstring, tostring

from apps.client_db import get_item
from maps.channel import channel_name_map
from maps.platform import platform_name_map
from models.news import FetchTask
from news.items import FetchResultItem
from tools.scrapy_tasks import pop_task
from tools.url import get_update_url, get_request_finger
from tools.weibo import get_su, get_login_data


class WeiboSpider(scrapy.Spider):
    """
    微博蜘蛛
    """
    name = 'weibo'
    allowed_domains = ['weibo.com', 'weibo.cn', 'sina.com.cn', 'sina.cn']

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

    passport_weibo_login_url = 'https://passport.weibo.cn/signin/login'

    start_urls = ['http://weibo.cn/']

    uid = 0

    login_form_data = {
        'username': '',
        'password': '',
        'savestate': '1',
        'r': '',
        'ec': '0',
        'pagerefer': '',
        'entry': 'mweibo',
        'wentry': '',
        'loginfrom': '',
        'client_id': '',
        'code': '',
        'qq': '',
        'mainpageflag': '1',
        'hff': '',
        'hfp': ''
    }

    def parse(self, response):
        return self.passport_weibo_login()

    def passport_weibo_login(self):
        yield scrapy.Request(url=self.passport_weibo_login_url, callback=self.login_sina_sso_prelogin)

    def login_sina_sso_prelogin(self, response):
        login_data = get_login_data()
        self.login_form_data.update(login_data)
        login_sina_sso_prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php'
        query_payload = {
            'checkpin': '1',
            'entry': 'mweibo',
            'su': get_su(login_data.get('username', '')),
            'callback': 'jsonpcallback%13d' % (time.time()*1000),
        }
        request_url = get_update_url(login_sina_sso_prelogin_url, query_payload)

        yield scrapy.Request(url=request_url, callback=self.passport_weibo_sso_login)

    def passport_weibo_sso_login(self, response):
        passport_weibo_sso_login_url = 'https://passport.weibo.cn/sso/login'

        yield scrapy.FormRequest(
            url=passport_weibo_sso_login_url,
            formdata=self.login_form_data,
            callback=self.after_login
        )

    def after_login(self, response):
        data = {
            'savestate': '1',
            'callback': 'jsonpcallback%13d' % (time.time()*1000),
        }

        res = response.body_as_unicode()
        info = json.loads(res)

        crossdomainlist = info['data']['crossdomainlist']
        self.uid = info['data']['uid']

        url_weibo_com = get_update_url(crossdomainlist['weibo.com'], data)
        url_sina_com_cn = get_update_url(crossdomainlist['sina.com.cn'], data)
        url_weibo_cn = get_update_url(crossdomainlist['weibo.cn'], data)

        url_items = {
            'url_weibo_com': url_weibo_com,
            'url_sina_com_cn': url_sina_com_cn,
            'url_weibo_cn': url_weibo_cn,
        }

        meta = dict(response.meta, **url_items)

        # 跨域处理 weibo.com
        yield scrapy.Request(url=url_weibo_com, callback=self.crossdomain_weibo_com, meta=meta)

    def crossdomain_weibo_com(self, response):
        """
        跨域处理 weibo.com
        :param response:
        :return:
        """
        # 跨域处理 sina.com.cn
        url_sina_com_cn = response.meta['url_sina_com_cn']
        yield scrapy.Request(url=url_sina_com_cn, callback=self.crossdomain_sina_com_cn, meta=response.meta)

    def crossdomain_sina_com_cn(self, response):
        """
        跨域处理 sina.com.cn
        :param response:
        :return:
        """
        # 跨域处理 weibo.cn
        url_weibo_cn = response.meta['url_weibo_cn']
        yield scrapy.Request(url=url_weibo_cn, callback=self.crossdomain_weibo_cn, meta=response.meta)

    def crossdomain_weibo_cn(self, response):
        """
        跨域处理 weibo.cn
        :param response:
        :return:
        """
        # 获取登录状态 weibo.cn
        yield scrapy.Request(url='https://weibo.cn/', callback=self.weibo_cn_index)

    def weibo_cn_index(self, response):
        """
        获取登录状态
        :param response:
        :return:
        """
        print(response.url)
        title = response.xpath('//title/text()').extract_first()
        if title == '我的首页':
            print('登录成功')
            # follow_url = 'https://weibo.cn/%s/follow' % self.uid
            # yield scrapy.Request(url=follow_url, callback=self.parse_follow_list)
            # 获取登录状态 weibo.com
            yield scrapy.Request(url='https://weibo.com/', callback=self.weibo_com_index)
        else:
            print('登录失败')

    def weibo_com_index(self, response):
        """
        获取登录状态
        :param response:
        :return:
        """
        print(response.url)
        title = response.xpath('//title/text()').extract_first()
        if '我的首页' in title:
            print('登录成功')
            # follow_url = 'https://weibo.cn/%s/follow' % self.uid
            # yield scrapy.Request(url=follow_url, callback=self.parse_follow_list)
            return self.get_article_task()
        else:
            print('登录失败')

    def parse_follow_list(self, response):
        """
        已关注列表
        """
        print(response.url)
        # 进入关注用户页面
        follows = response.xpath('//table//tr/td/a[1]/@href').extract()
        for follow in follows:
            yield scrapy.Request(url=follow, callback=self.follow_home_list)

        # 关注列表翻页
        next_url = response.xpath('//div[@id="pagelist"]//a[contains(text(), "下页")]/@href').extract_first(default='')
        next_url = response.urljoin(next_url)
        if next_url == response.url:
            print('当前条件列表页最后一页：%s' % response.url)
        else:
            yield scrapy.Request(url=next_url, callback=self.parse_follow_list)

    def follow_home_list(self, response):
        """
        已关注用户首页列表
        """
        contents = response.xpath('//div[@class="c"]//span[@class="ctt"]/text()').extract()
        for content in contents:
            print(content)

    def get_article_task(self):
        """
        文章抓取入口
        :return:
        """
        task_id = pop_task(self.name)

        if not task_id:
            print('%s task is empty' % self.name)
            return
        print('%s task id: %s' % (self.name, task_id))

        task_item = get_item(FetchTask, task_id)

        article_id = task_item.follow_id

        article_list_url = 'https://weibo.com/p/%s/wenzhang' % article_id

        meta = {
            'task_id': task_item.id,
            'platform_id': task_item.platform_id,
            'channel_id': task_item.channel_id,
            'follow_id': task_item.follow_id,
            'follow_name': task_item.follow_name,
        }

        yield scrapy.Request(url=article_list_url, callback=self.parse_article_list, meta=meta)

    @staticmethod
    def replace_all(input_html, replace_dict):
        """
        用字典实现批量替换
        """
        for k, v in six.iteritems(replace_dict):
            input_html = input_html.replace(k, v)
        return input_html

    def parse_article_list(self, response):
        """
        文章列表解析
        没有翻页特征 <a class=\"page next S_txt1 S_line1 page_dis\"><span>下一页<\/span>
        解析链接 href=\"\/p\/1005051627825392\/wenzhang?pids=Pl_Core_ArticleList__61&cfs=600&Pl_Core_ArticleList__61_filter=&Pl_Core_ArticleList__61_page=6#Pl_Core_ArticleList__61\"
        """
        print('task_url: %s' % response.url)
        # 页面解析(微博是JS动态数据, 无法直接解析页面)
        article_list_body = response.body_as_unicode()

        article_list_rule = r'<script>FM.view\({"ns":"pl.content.miniTab.index","domid":"Pl_Core_ArticleList__\d+".*?"html":"(.*?)"}\)</script>'
        article_list_re_parse = re.compile(article_list_rule, re.S).findall(article_list_body)
        if not article_list_re_parse:
            return
        article_list_html = ''.join(article_list_re_parse)

        # 转义字符处理
        article_list_html = article_list_html.replace('\\r', '')
        article_list_html = article_list_html.replace('\\t', '')
        article_list_html = article_list_html.replace('\\n', '')
        article_list_html = article_list_html.replace('\\"', '"')
        article_list_html = article_list_html.replace('\\/', '/')

        article_list_doc = fromstring(article_list_html)
        article_list_doc_parse = article_list_doc.xpath('//div[@class="text_box"]')

        for article_item in article_list_doc_parse:
            article_detail_url = article_item.xpath('./div[@class="title W_autocut"]/a[@class="W_autocut S_txt1"]/@href')
            article_detail_title = article_item.xpath('./div[@class="title W_autocut"]/a[@class="W_autocut S_txt1"]/text()')
            article_detail_abstract = article_item.xpath('./div[@class="text"]/a[@class="S_txt1"]/text()')
            if not (article_detail_url and article_detail_title):
                continue
            article_detail_url = article_detail_url[0].strip()
            article_detail_url = response.urljoin(article_detail_url)
            article_detail_title = article_detail_title[0].strip()

            article_detail_abstract = article_detail_abstract[0].strip() if article_detail_abstract else ''

            meta_article_item = {
                'article_url': article_detail_url,
                'article_title': article_detail_title,
                'article_abstract': article_detail_abstract,
                'article_id': get_request_finger(article_detail_url),
            }

            meta = dict(response.meta, **meta_article_item)

            # 两种不同类型页面
            if '/ttarticle/p/show?id=' in article_detail_url:
                yield scrapy.Request(url=article_detail_url, callback=self.parse_article_detail_html, meta=meta)
            else:
                yield scrapy.Request(url=article_detail_url, callback=self.parse_article_detail_js, meta=meta)

        # 翻页处理
        next_url_parse = article_list_doc.xpath('//a[@class="page next S_txt1 S_line1"]/@href')
        if not next_url_parse:
            print('当前条件列表页最后一页：%s' % response.url)
        else:
            next_url = next_url_parse[0]
            next_url = response.urljoin(next_url)
            print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_article_list, meta=response.meta)

    def parse_article_detail_html(self, response):
        """
        文章详情解析 html 版
        :param response:
        :return:
        """
        article_title = response.xpath('//div[@class="title"]/text()').extract_first(default='')
        article_pub_time = response.xpath('//span[@class="time"]/text()').extract_first(default='')
        article_content = response.xpath('//div[@class="WB_editor_iframe"]').extract_first(default='')
        fetch_result_item = FetchResultItem()
        fetch_result_item['task_id'] = response.meta['task_id']
        fetch_result_item['platform_id'] = response.meta['platform_id']
        fetch_result_item['platform_name'] = platform_name_map.get(response.meta['platform_id'], '')
        fetch_result_item['channel_id'] = response.meta['channel_id']
        fetch_result_item['channel_name'] = channel_name_map.get(response.meta['channel_id'], '')
        fetch_result_item['article_id'] = response.meta['article_id']
        fetch_result_item['article_title'] = article_title
        fetch_result_item['article_author_id'] = response.meta['follow_id']
        fetch_result_item['article_author_name'] = response.meta['follow_name']
        fetch_result_item['article_pub_time'] = article_pub_time
        fetch_result_item['article_url'] = response.url
        fetch_result_item['article_tags'] = ''
        fetch_result_item['article_abstract'] = response.meta['article_abstract']
        fetch_result_item['article_content'] = article_content
        yield fetch_result_item

    @staticmethod
    def trans_time(time_str):
        """
        时间转换
        :param time_str:
        :return:
        """
        time_rule = r'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)'
        time_parse = re.compile(time_rule, re.S).findall(time_str)
        if not time_parse:
            return time.strftime('%Y-%m-%d %H:%M:%S')
        return datetime(*[int(i) for i in time_parse[0]]).strftime('%Y-%m-%d %H:%M:%S')

    def parse_article_detail_js(self, response):
        """
        文章详情解析 js 版
        :param response:
        :return:
        """
        article_detail_body = response.body_as_unicode()
        article_detail_rule = r'<script>FM.view\({"ns":.*?"html":"(.*?)"}\)</script>'
        article_detail_re_parse = re.compile(article_detail_rule, re.S).findall(article_detail_body)
        if not article_detail_re_parse:
            return
        article_detail_html = ''.join(article_detail_re_parse)

        # 转义字符处理
        article_detail_html = article_detail_html.replace('\\r', '')
        article_detail_html = article_detail_html.replace('\\t', '')
        article_detail_html = article_detail_html.replace('\\n', '')
        article_detail_html = article_detail_html.replace('\\"', '"')
        article_detail_html = article_detail_html.replace('\\/', '/')

        article_detail_doc = fromstring(article_detail_html)

        article_title_parse = article_detail_doc.xpath('//h1[@class="title"]/text()')
        article_title = article_title_parse[0].strip() if article_title_parse else ''

        article_pub_time_parse = article_detail_doc.xpath('//span[@class="time"]/text()')
        article_pub_time = self.trans_time(article_pub_time_parse[0].strip()) if article_pub_time_parse else time.strftime('%Y-%m-%d %H:%M:%S')

        article_content_parse = article_detail_doc.xpath('//div[@class="WBA_content"]')
        article_content = tostring(article_content_parse[0], encoding='unicode').strip() if article_content_parse else ''

        fetch_result_item = FetchResultItem()
        fetch_result_item['task_id'] = response.meta['task_id']
        fetch_result_item['platform_id'] = response.meta['platform_id']
        fetch_result_item['platform_name'] = platform_name_map.get(response.meta['platform_id'], '')
        fetch_result_item['channel_id'] = response.meta['channel_id']
        fetch_result_item['channel_name'] = channel_name_map.get(response.meta['channel_id'], '')
        fetch_result_item['article_id'] = response.meta['article_id']
        fetch_result_item['article_title'] = article_title
        fetch_result_item['article_author_id'] = response.meta['follow_id']
        fetch_result_item['article_author_name'] = response.meta['follow_name']
        fetch_result_item['article_pub_time'] = article_pub_time
        fetch_result_item['article_url'] = response.url
        fetch_result_item['article_tags'] = ''
        fetch_result_item['article_abstract'] = response.meta['article_abstract']
        fetch_result_item['article_content'] = article_content
        yield fetch_result_item
