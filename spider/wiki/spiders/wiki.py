# -*- coding: utf-8 -*-
__author__ = 'xiyuanbupt'

# e-mail : xywbupt@gmail.com

import collections
import json
from urllib.parse import urlencode
import scrapy
from scrapy.http import Request

from items import PageItem


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
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        # "HOST": 'm.byr.cn'
    }
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
        for key in concept_def:
            url = self.start_urls[0] + "?" + urlencode(self.querystring) + "&srsearch=" + key
            yield Request(url,
                          callback=self.parse,
                          headers=self.headers,
                          meta={'proxy': self.meta_proxy}
                          )

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        search_list = res["query"]["search"]
        if len(search_list) > 0:
            title = search_list[0]["title"]
            true_url = self.api_url + "?" + urlencode(self.parsestring) + "&page=" + title
            yield Request(true_url,
                          callback=self.sub_parse,
                          headers=self.headers,
                          meta={'proxy': self.meta_proxy}
                          )
        else:
            # 查询不到结果
            pass

    def sub_parse(self, response):
        res = json.loads(response.body_as_unicode())
        item = PageItem()
        item["title"] = res["title"]
        item["pageid"] = res["pageid"]
        # TODO,得到的只是图片名字，还不是url
        item["images"] = res["images"]
        item["wikitext"] = res["wikitext"]
        yield item
