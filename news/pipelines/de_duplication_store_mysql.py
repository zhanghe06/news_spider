# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from models.news import FetchResult
from news.items import FetchResultItem
from apps.client_db import db_session_mysql
from tools.weixin import get_finger
from maps.platform import WEIXIN, WEIBO

from scrapy.exceptions import DropItem


class DeDuplicationStoreMysqlPipeline(object):
    """
    去重 - 入库
    注意:
        1、置于数据存储 pipeline 之前
    """
    def process_item(self, item, spider):

        session = db_session_mysql()
        try:
            if isinstance(item, FetchResultItem):
                if spider.name == 'weixin':
                    # 标题（微信只能通过标题去重, 因为链接带过期签名）
                    article_id_count = session.query(FetchResult) \
                        .filter(FetchResult.platform_id == WEIXIN, FetchResult.article_id == get_finger(item['article_title'])) \
                        .count()
                    if article_id_count:
                        raise DropItem('%s Has been duplication of article_title: %s' % (spider.name, item['article_title']))

                if spider.name == 'weibo':
                    # 详细链接（微博可以直接通过链接去重）
                    article_url_count = session.query(FetchResult)\
                        .filter(FetchResult.platform_id == WEIBO, FetchResult.article_id == get_finger(item['article_url']))\
                        .count()
                    if article_url_count:
                        raise DropItem('%s Has been duplication of article_url: %s' % (spider.name, item['article_url']))

            return item
        except Exception as e:
            raise e
        finally:
            session.close()
