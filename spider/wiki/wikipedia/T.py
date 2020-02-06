#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/13
@contact: tenyun.zhang.cs@gmail.com
"""
import pymysql

from settings import HOST, USER, PASSWORD, DATABASE_NAME

connection = pymysql.connect(host=HOST,
                                              user=USER,
                                              password=PASSWORD,
                                              db=DATABASE_NAME,
                                              port=3306,
                                              charset="utf8mb4"
                                              )
cursor = connection.cursor()
cursor.execute("select cui from mrconimg limit 0, 10")
result = cursor.fetchmany()
print(result)
