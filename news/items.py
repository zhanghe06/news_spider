# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FetchTaskItem(scrapy.Item):
    """
    table_name: fetch_task
    primary_key: id
    """
    follow_id = scrapy.Field()
    fetch_url = scrapy.Field()
    description = scrapy.Field()
    platform_id = scrapy.Field()
    channel_id = scrapy.Field()
    avatar_url = scrapy.Field()
    flag_enabled = scrapy.Field()
    follow_name = scrapy.Field()


class FetchResultItem(scrapy.Item):
    """
    table_name: fetch_result
    primary_key: id
    """
    article_title = scrapy.Field()
    platform_name = scrapy.Field()
    task_id = scrapy.Field()
    channel_id = scrapy.Field()
    article_author_name = scrapy.Field()
    article_content = scrapy.Field()
    platform_id = scrapy.Field()
    channel_name = scrapy.Field()
    article_url = scrapy.Field()
    article_abstract = scrapy.Field()
    article_author_id = scrapy.Field()
    article_tags = scrapy.Field()
    article_id = scrapy.Field()
    article_pub_time = scrapy.Field()


class ChannelItem(scrapy.Item):
    """
    table_name: channel
    primary_key: id
    """
    code = scrapy.Field()
    description = scrapy.Field()
    name = scrapy.Field()
