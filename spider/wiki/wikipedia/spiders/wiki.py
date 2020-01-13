# -*- coding: utf-8 -*-
import json
import logging
import re
from urllib.parse import urlencode
import scrapy
from tqdm import tqdm
from scrapy.http import Request
from ..items import PageItem, ImageItem
from ..settings import HEADERS
from ..util.CUITool import CUITool

logger = logging.getLogger(__name__)


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    wiki_base = "https://en.wikipedia.org/wiki/"
    api_url = "https://en.wikipedia.org/w/api.php"
    start_urls = [api_url]
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
        # prepare keys format as cui:concept_name
        print("crawl start...")
        db = CUITool()
        # TODO 考虑可扩展性，因为不只一个UMLS数据库
        # cui 最大G4551440
        for i in tqdm(range(1, 2277)):
            cuis = [tuple(["C" + str(i).zfill(7)]) for i in range(i, i + 2000)]
            concept_def = db.query_batch(cuis)
            for concept, key in concept_def.items():
                url = self.start_urls[0] + "?" + urlencode(self.querystring) + "&srsearch=" + key
                yield Request(url,
                              callback=self.parse,
                              headers=HEADERS,
                              meta={'proxy': self.meta_proxy, 'concept': concept}
                              )

    def parse(self, response):
        if response.url == 'exception':
            logger.info('concept %s crawl process meets exception' % response.meta["concept"])
        if response.url == '4050':
            logger.info('concept %s crawl process meets exception' % response.meta["concept"])
        res = json.loads(response.body_as_unicode())
        try:
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
                logger.info('concept %s crawl process meets exception' % response.meta["concept"])
        except Exception as e:
            logger.info("parse error: ", e)

    def sub_parse(self, response):
        res = json.loads(response.body_as_unicode())
        try:
            if res:
                item = PageItem()
                item["cui"] = response.meta["concept"]
                item["title"] = res["parse"]["title"]
                item["pageid"] = res["parse"]["pageid"]
                # TODO,得到的只是图片名字，还不是url, 根据图片名字去找对应的图片URL
                img_api = "https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles=Image:"
                img_urls = []
                for img_name in res["parse"]["images"]:
                    yield Request(img_api + img_name,
                                  callback=self.img_parse,
                                  headers=HEADERS,
                                  meta={'proxy': self.meta_proxy, 'concept': response.meta["concept"]}
                                  )
                item["images"] = img_urls
                wikitext = res["parse"]["wikitext"]
                item["wikitext"] = self.clean_text(wikitext)
                yield item
        except Exception as e:
            logger.info("sub_parse error: ", e)

    def img_parse(self, response):
        text = response.body_as_unicode()
        item = ImageItem()
        try:
            if text:
                res = json.loads(text)
                item["cui"] = response.meta["concept"]
                pages = res["query"]["pages"]
                pageid = ""
                for key in pages.keys():
                    pageid = key
                page = pages[pageid]
                if "imageinfo" in page.keys():
                    item["url"] = page["imageinfo"][0]["url"]
                    item["image_urls"] = page["imageinfo"][0]["url"]
                    yield item
        except Exception as e:
            logger.info("img_parse error: ", e)

    def clean_text(self, wikitext):
        wikitext = self.removeNonWordChar(wikitext)
        return wikitext

    # remove non-word chars
    def removeNonWordChar(self, inputString):
        return re.sub(r"[^\w]", "", inputString)  # non [a-zA-Z0-9_]
