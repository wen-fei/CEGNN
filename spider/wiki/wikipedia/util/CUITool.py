#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/12
@contact: tenyun.zhang.cs@gmail.com
"""
import logging

import pymysql

from ..settings import HOST, USER, PASSWORD, DATABASE_NAME

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
        results = {}
        try:
            sql = "SELECT CUI, STR FROM `mrconso_eng` where CUI=%s"
            # 弃用，有Bug，当返回结果只有一行的时候返回empty
            # TODO, 本质还是调用循环，效率没有变高，而且有Bug
            # self.cursor.executemany(sql, cuis)
            # return self.cursor.fetchall()
            for cui in cuis:
                self.cursor.execute(sql, cui)
                result = self.cursor.fetchone()
                if result is not None:
                    results[result[0]] = result[1]
            return results
        except:
            logger.error("query_batch function error!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def insert_batch(self, data, sql):
        """
        :param sql:
        :param data: ((cui, url), (cui, url), ...)
        :return:
        """
        try:
            self.cursor.executemany(sql, data)
            self.connection.commit()
        except:
            logger.error("insert data into db error.")
