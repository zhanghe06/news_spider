# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from models.news import FetchResult
from news.items import FetchResultItem
from apps.client_db import db_session_mysql


class StoreMysqlPipeline(object):
    """
    基于 MySQL 的存储
    """

    def process_item(self, item, spider):
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
