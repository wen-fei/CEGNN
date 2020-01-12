# -*- coding: utf-8 -*-
__author__ = 'xiyuanbupt'

# e-mail : xywbupt@gmail.com

import collections
import json
import logging
from urllib.parse import urlencode
import scrapy
from scrapy.http import Request
from items import PageItem
from settings import HEADERS

logger = logging.getLogger(__name__)


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    wiki_base = "https://en.wikipedia.org/wiki/"
    api_url = "https://en.wikipedia.org/w/api.php"
    # start_urls = [
    #     api_url + "?action=query&list=search&format=json&" + \
    #     "prop=categories|images|pageimages|revisions&" + \
    #     "formatversion=2&rvprop=content&utf8&srsearch="
    # ]
    start_url = [api_url]
    meta_proxy = "http://127.0.0.1:1080"
    visited = set()

    querystring = {
        "action": "query",
        "list": "search",
        "format": "json",
        "prop": "categories|images|pageimages|revisions",
        "formatversion": 2,
        "rvprop": "content",
    }
    parsestring = {
        "action": "parse",
        "list": "search",
        "format": "json",
        "prop": "wikitext|images",
        "formatversion": 2,
    }

    def start_requests(self):

        # key = "cemeterties"
        concept_def = []
        for concept, key in concept_def:
            url = self.start_urls[0] + "?" + urlencode(self.querystring) + "&srsearch=" + key
            yield Request(url,
                          callback=self.parse,
                          headers=self.headers,
                          meta={'proxy': self.meta_proxy, 'concept': concept}
                          )

    def parse(self, response):
        if response.url == 'exception':
            logger.debug('concept %s crawl process meets exception' % response.meta["concept"])
        if response.url == '4050':
            logger.debug('concept %s crawl process meets exception' % response.meta["concept"])
        res = json.loads(response.body_as_unicode())
        search_list = res["query"]["search"]
        if len(search_list) > 0:
            title = search_list[0]["title"]
            true_url = self.api_url + "?" + urlencode(self.parsestring) + "&page=" + title
            yield Request(true_url,
                          callback=self.sub_parse,
                          headers=HEADERS,
                          meta={'proxy': self.meta_proxy, 'concept': response.meta["concept"]}
                          )
        else:
            # 查询不到结果
            logger.debug('concept %s crawl process meets exception' % response.meta["concept"])

    def sub_parse(self, response):
        res = json.loads(response.body_as_unicode())
        item = PageItem()
        item["title"] = res["title"]
        item["pageid"] = res["pageid"]
        # TODO,得到的只是图片名字，还不是url
        item["images"] = res["images"]
        item["wikitext"] = res["wikitext"]
        yield item
