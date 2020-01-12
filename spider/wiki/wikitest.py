#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/11
@contact: tenyun.zhang.cs@gmail.com
"""

import urllib.request

proxy_addrs = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
wiki_url = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&prop=categories|images|pageimages|revisions&formatversion=2&rvprop=content&utf8&srsearch=cemeteries"
proxy_handler = urllib.request.ProxyHandler(proxy_addrs)  # 设置对应的代理服务器信息
opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPHandler)  # 创建一个自定义的opener对象
urllib.request.install_opener(opener)  # 创建全局默认的opener对象
req = urllib.request.Request(wiki_url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
