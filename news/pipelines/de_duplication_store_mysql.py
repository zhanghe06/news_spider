# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from models.news import FetchResult
from news.items import FetchResultItem
from apps.client_db import db_session_mysql
from tools.weixin import get_finger

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
                # 标题
                article_id_count = session.query(FetchResult) \
                    .filter(FetchResult.article_id == get_finger(item['article_title'])) \
                    .count()
                if article_id_count:
                    raise DropItem("Has been duplication of article_title: %s" % item['article_title'])

                # 详细链接
                article_url_count = session.query(FetchResult)\
                    .filter(FetchResult.article_url == item['article_url'])\
                    .count()
                if article_url_count:
                    raise DropItem("Has been duplication of article_url: %s" % item['article_url'])

                return item
        except Exception as e:
            raise e
        finally:
            session.close()
