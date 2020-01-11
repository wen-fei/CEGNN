# coding=utf-8
import string
import json

import requests


class UrlGenerator:
    wiki_base = "https://en.wikipedia.org/wiki/"
    api_url = "https://en.wikipedia.org/w/api.php"
    querystring = {
        "action": "query",
        "list": "search",
        "format": "json",
        "redirects": True,
        "prop": "categories|images|pageimages|revisions",
        "formatversion": 2,
        "rvprop": "content",
        "rvparse": True
    }

    def get_next(self):
        pass
