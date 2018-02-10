# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from scrapy.exporters import CsvItemExporter


class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file_csv = open('%s_items.csv' % spider.name, 'w+b')
        self.files[spider] = file_csv
        self.exporter = CsvItemExporter(file_csv)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file_csv = self.files.pop(spider)
        file_csv.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
