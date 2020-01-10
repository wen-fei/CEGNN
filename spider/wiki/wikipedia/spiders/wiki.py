# -*- coding: utf-8 -*-
__author__ = 'xiyuanbupt'

# e-mail : xywbupt@gmail.com

import collections
import urllib

import scrapy
from scrapy.http import Request


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]

    visited = set()

    def __init__(self, stats, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.stats = stats

    # 重写了父类的from_crawler 方法
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.stats, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def start_requests(self):
        wiki_base = "https://en.wikipedia.org/wiki/"
        api_url = "https://en.wikipedia.org/w/api.php"
        start_urls = [
            api_url + "?action=query&list=search&" + \
            "format=json&prop=categories|images|pageimages|revisions&formatversion=2&" + \
            "rvprop=content&utf8&rvparse=true&titles="
        ]

        querystring = {
            "action": "query",
            "list": "search",
            "format": "json",
            "redirects": "True",
            "prop": "categories|images|pageimages|revisions",
            "formatversion": 2,
            "rvprop": "content",
            "rvparse": "True"
        }
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            "HOST": 'm.byr.cn'
        }

        for url in start_urls:
            key = "cemeteries"
            url = urllib.parse.urljoin(url, key)
            yield Request(url,
                          callback=self.parse,
                          headers=headers
                          )

    def parse(self, response):
        print(response)
