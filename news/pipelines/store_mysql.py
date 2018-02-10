# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from models.news import FetchResult
from news.items import FetchResultItem
from apps.client_db import db_session_mysql
from tools.duplicate import is_dup_detail, add_dup_detail

from scrapy.exceptions import DropItem


class StoreMysqlPipeline(object):
    """
    基于 MySQL 的存储
    """

    def process_item(self, item, spider):

        spider_name = spider.name
        session = db_session_mysql()
        try:
            if isinstance(item, FetchResultItem):
                fetch_result = FetchResult(**item)
                # 数据入库
                session.add(fetch_result)
                session.flush()
                # session.commit()
                return item
        except Exception as e:
            raise e
        finally:
            session.close()
