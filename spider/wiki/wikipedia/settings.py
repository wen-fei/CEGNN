# -*- coding: utf-8 -*-

# Scrapy settings for wikipedia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import datetime

BOT_NAME = 'wikipedia'

SPIDER_MODULES = ['wikipedia.spiders']
NEWSPIDER_MODULE = 'wikipedia.spiders'

# databases setting
# TODO

# log setting
LOG_LEVEL = 'DEBUG'
to_day = datetime.datetime.now()
log_file_path = 'log/scrapy_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day)
LOG_FILE = log_file_path

# middleware
DOWNLOADER_MIDDLEWARES = {
    'wikipedia.middlewares.RequestsRetryMiddleware': 543,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    'wikipedia.middlewares.UserAgentMiddleware': 400,
}
# Retry setting
RETRY_ENABLED = True
# 需要重试的错误码列表
RETRY_HTTP_CODES = [429]
RETRY_TIMES = 1

# pipelines
ITEM_PIPELINES = {
    'wikipedia.pipelines.WikipediaPipeline': 300,
}
# ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
# IMAGES_STORE = "images/"
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
    # User-Agent使用了中间件
}

# 反爬虫策略
COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = True  # 自动限速
DOWNLOAD_DELAY = 1  # 爬取速度，单位s
REDIRECT_ENABLED = False  # 关闭重定向
AUTOTHROTTLE_MAX_DELAY = 10  # 默认60


# MySQL connect setting
HOST = "localhost"
USER = "root"
PASSWORD = "123456"
DATABASE_NAME = "umls_subset"
BATCH_SIZE_PAGE = 50  # batch sql size
BATCH_SIZE_IMAGE = 3000

LOG_LEVEL= 'INFO'