# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from util.CUITool import CUITool


class WikipediaPipeline(object):
    def __init__(self):
        self.db = CUITool()
        self.data_list = []

    def process_item(self, item, spider):
        sql = "INSERT INTO mrconimg(concept, url) VALUES (%s,%s)"
        if len(self.data_list) == 2000:
            self.db.insert_batch(self.data_list, sql)
            self.data_list = []
        else:
            self.data_list.append((item['concept'], item['url']))
        return item
