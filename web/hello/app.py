#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello flask!</h1>"


@app.route("/hi")
@app.route("/hello")
def say_hello():
    return "<h1>hello</h1>"
