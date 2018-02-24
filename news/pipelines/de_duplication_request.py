# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from news.items import FetchResultItem

from tools.duplicate import is_dup_detail, add_dup_detail


class DeDuplicationRequestPipeline(object):
    """
    去重 - 请求
    注意:
        1、置于数据存储 pipeline 之后
        2、与 DeDuplicationRequestMiddleware 配合使用
    """
    def process_item(self, item, spider):

        spider_name = spider.name
        if isinstance(item, FetchResultItem):
            # 详细页url 加入去重集合
            if not is_dup_detail(item['article_url'], spider_name, item['channel_id']):
                add_dup_detail(item['article_url'], spider_name, item['channel_id'])
            return item
