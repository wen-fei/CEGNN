#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/12
@contact: tenyun.zhang.cs@gmail.com
"""
import logging

import pymysql

from settings import HOST, USER, PASSWORD, DATABASE_NAME

logger = logging.getLogger(__name__)


class CUITool:
    """
    MySQL related tool
    """

    def __init__(self):
        try:
            self.connection = pymysql.connect(host=HOST,
                                              user=USER,
                                              password=PASSWORD,
                                              db=DATABASE_NAME,
                                              port=3306,
                                              charset="utf8"
                                              )
        except:
            logger.info("MySQL database connect error... please check CUITool.py")
        self.cursor = self.connection.cursor()

    def query_one(self, cui):
        self.cursor.execute("SELECT CUI, STR FROM `mrconso_eng` where CUI=%s" % cui)
        self.connection.commit()
        return self.cursor.fetchone()

    def query_batch(self, cuis):
        """
        批量查询，效率更高
        :param cuis: cui tuple，format as ((cui1), (cui2), ...)
        :return:
        """
        try:
            sql = "SELECT CUI, STR FROM `mrconso_eng` where CUI=%s"
            self.cursor.executemany(sql, cuis)
        except:
            logger.error("query_batch function error!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def insert_batch(self, data):
        """
        :param data: ((cui, url), (cui, url), ...)
        :return:
        """
        try:
            sql = "INSERT INTO mrconimg(concept, url) VALUES (%s,%s)"
            self.cursor.executemany(sql, data)
            self.connection.commit()
        except Exception as e:
            logger.error("insert data into db error.", e)
        return self.cursor.fetchone()
