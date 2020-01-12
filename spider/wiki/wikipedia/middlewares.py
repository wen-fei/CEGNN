#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/12
@contact: tenyun.zhang.cs@gmail.com
"""
import logging

from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import HtmlResponse
from scrapy.utils.response import response_status_message
from twisted.internet import defer
from twisted.internet.error import DNSLookupError, ConnectionDone, ConnectError, TCPTimedOutError, ConnectionLost
from twisted.web.client import ResponseFailed


logger = logging.getLogger(__name__)


class RequestsRetryMiddleware(RetryMiddleware):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def process_response(self, request, response, spider):
        # 重试
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 在此处进行自己的操作，如删除不可用代理，打日志等
            return self._retry(request, reason, spider) or response
        # 捕获状态码为40x/50x的response
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            # 随意封装，直接返回response，spider代码中根据url==''来处理response
            response = HtmlResponse(url='4050')
            return response
        # 其他状态码不处理
        return response

    def process_exception(self, request, exception, spider):
        """
        异常处理
        :param request:
        :param exception:
        :param spider:
        :return:
        """
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            logger.debug('Got exception: %s' % exception)
            # 随意封装一个response，返回给spider
            response = HtmlResponse(url='exception')
            return response
        # 打印出未捕获到的异常
        logger.debug('not contained exception: %s' % exception)
