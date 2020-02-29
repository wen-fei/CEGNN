#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/hello")
def hello():
    # 获取查询参数name的值，并设置默认值
    name = request.args.get("name", "Flask")
    return "<h1>Hello, %s</h1>".format(name)


@app.route("/hello2", methods=["GET", "POST"])
def hello2():
    return "<h1>Hello, Flask!</h1>"
