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


@app.route("/goback/<int:year>")
def go_back(year):
    return "<p>welcome to %d!</p>".format(2018 - year)


colors = ["blue", "white", "red"]


# @app.route("/color/<any(blue, white, red):color>")
@app.route("/color/<any(%s):color" % str(colors)[1:-1])
def three_color(color):
    return "Love is patient and kind. Love is not jealousor boastful or proud or rude."
