# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import pandas as pd
from .items import ImageItem, PageItem
from .settings import BATCH_SIZE_PAGE, BATCH_SIZE_IMAGE
from .util.CUITool import CUITool


class WikipediaPipeline(object):
    def __init__(self):
        self.db = CUITool()
        # self.data_df_image = pd.DataFrame(columns=['cui', 'url'])
        # self.data_df_page = pd.DataFrame(columns=['cui', 'pageid', 'title', 'wikitext'])
        self.data_list_image = []
        self.data_list_page = []

    def process_item(self, item, spider):
        if isinstance(item, ImageItem):
            sql = "INSERT INTO mrconimg(CUI, url) VALUES (%s,%s)"
            if len(self.data_list_image) == BATCH_SIZE_IMAGE:
                self.db.insert_batch(self.data_list_image, sql)
                self.data_list_image = []
                # self.data_df_image.to_csv('images_url.csv', mode='a', header=False)
                # self.data_df_image = pd.DataFrame(columns=['cui', 'url'])
            else:
                self.data_list_image.append((item["cui"], item["url"]))
                # self.data_list_image.append({'cui': item["cui"], 'url': item["url"]})
        elif isinstance(item, PageItem):
            sql = "INSERT INTO mrcontext(CUI, pageid, title, wikitext) VALUES (%s, %s, %s, %s)"
            if len(self.data_list_page) == BATCH_SIZE_PAGE:
                self.db.insert_batch(self.data_list_page, sql)
                self.data_list_page = []
                # self.data_df_page.to_csv('cui_text.csv', mode='a', header=False)
                # self.data_df_page = pd.DataFrame(columns=['cui', 'pageid', 'title', 'wikitext'])

            else:
                # self.data_df_page.append({'cui': item["cui"], 'pageid': item["pageid"], 'title': item["title"],
                #                           'wikitext': item["wikitext"]})
                self.data_list_page.append((item["cui"], item["pageid"], item["title"], item["wikitext"]))
        return item

    def save_to_csv(self, l):
        pass


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
