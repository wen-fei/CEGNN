#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""
import click
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello flask!</h1>"


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
