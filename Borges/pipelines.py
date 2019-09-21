# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#
# class BorgesPipeline(object):
#     def process_item(self, item, spider):
#         return item

import json
from scrapy.exporters import JsonItemExporter


class BorgesPipeline(object):

    def __init__(self):
        self.file = open("pipline2.json", 'wb')
        self.exporter = JsonItemExporter(
            self.file,
            encoding='utf-8',
            ensure_ascii=False,
            indent=True
        )
        # content = json.dumps(dict(item),ensure_ascii = False,indent=2)+",\n"
        # self.f.write(content.encode("utf-8"))
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
