# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WikipediaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PageItem(scrapy.Item):
    title = scrapy.Field()
    pageid = scrapy.Field()
    images = scrapy.Field()
    wikitext = scrapy.Field()


class ImageItem(scrapy.Item):
    concept = scrapy.Field()
    url = scrapy.Field()