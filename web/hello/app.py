#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""
import click
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hi")
@app.route("/hello")
def say_hello():
    return "<h1>hello</h1>"


# 动态路由
@app.route("/greet/<name>")
def greet(name):
    return "<h1>Hello, %s</h1>" % name


@app.route("/greet", defaults={"name": "Programmer"})
@app.route("/greet/<name>")
def greet2(name):
    return "<h1>Hello, %s</h1>" % name


@app.cli.command()
def hello():
    click.echo("hello, Human!")


user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}
movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route("/watchlist")
def watchlist():
    return render_template("watchlist.html", user=user, movies=movies)


def inject_foo():
    """
    当我们调用render_template 函数渲染任意一个模板时， 所有使用
    app.context_processor装饰器注册的模板上下文处理函数（ 包括Flask内置的上
    下文处理函数） 都会被执行， 这些函数的返回值会被添加到模板中， 因此我们可以
    在模板中直接使用foo变量。
    :return:
    """
    foo = "i am foo."
    # equal to return {'foo': foo}
    return dict(foo=foo)


# 自定义上下文
app.context_processor(inject_foo)


@app.template_global()
def bar():
    return "I am a bar"


app.jinja_env.globals["bar"] = bar
app.jinja_env.globals["user"] = user
