#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""

from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify
from urllib.parse import urlparse, urljoin

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


@app.before_request
def o_something():
    # this code will run before every request
    pass


@app.route("/hello")
def hello():
    # 设置状态码302，重定向，主体内容为空
    return "", 302, {"Location": "http://www.example.com"}


@app.route("/hello")
def hello3():
    return redirect("http://ww.example.com")


@app.route("/hi")
def hi():
    # redirect to /hello
    return redirect(url_for("hello"))


@app.route("/404")
def not_found():
    abort(404)


@app.route("/foo")
def foo():
    response = make_response("hello world!")
    response.mimetype = "text/plain"
    return response


@app.route("/foo")
def foo2():
    data = {
        "name": "li ming",
        "gender": "male"
    }
    # response = make_response(json.dump(data))
    # response.mimetype = "application/json"
    # return response
    # return jsonify(name="li ming", gender="male")
    return jsonify(data)


@app.route("/")
@app.route("/hello")
def hello4():
    name = request.args.get("name")
    if name is None:
        name = request.cookies.get("name", "Human")
    return "<h1>Hello, %s</h1>" % name


# 重定向到上一个页面
def redirect_back(default="hello", **kwargs):
    for target in request.args.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route("/do_something_and_redirect")
def do_something():
    # do something
    return redirect_back()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
