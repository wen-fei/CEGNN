# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from .items import ImageItem, PageItem
from .settings import BATCH_SIZE
from .util.CUITool import CUITool


class WikipediaPipeline(object):
    def __init__(self):
        self.db = CUITool()
        self.data_list_image = []
        self.data_list_page = []

    def process_item(self, item, spider):
        if isinstance(item, ImageItem):
            sql = "INSERT INTO mrconimg(CUI, url) VALUES (%s,%s)"
            if len(self.data_list_image) == BATCH_SIZE:
                self.db.insert_batch(self.data_list_image, sql)
                self.data_list_image = []
            else:
                self.data_list_image.append((item["cui"], item["url"]))
        elif isinstance(item, PageItem):
            sql = "INSERT INTO mrcontext(CUI, pageid, title, wikitext) VALUES (%s, %s, %s, %s)"
            if len(self.data_list_page) == BATCH_SIZE:
                self.db.insert_batch(self.data_list_page, sql)
                self.data_list_page = []
            else:
                self.data_list_page.append((item["cui"], item["pageid"], item["title"], item["wikitext"]))
        return item


# TODO, 下载图片，等最后再下载也行，单独起一个爬虫
class DownImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item, 'index': item['image_urls'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']
        img_name = item['cui'] + "." + request.url.split('/')[-1].split('.')[-1]
        down_file_name = u'full/{0}'.format(img_name)
        return down_file_name