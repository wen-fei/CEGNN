#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""
import os

import click
from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename

from forms import LoginForm

app = Flask(__name__)

# file store location
UPLOAD_FOLDER = 'G://'
# file type allowed
ALLOWED_EXTENSIONS = set(['pdf', "PDF"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    check file type
    :param filename
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    """
    upload pdf file and store it.
    """
    if request.method == "POST":
        file = request.files['pdf']
        print(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return url_for('page_not_found')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    show file content
    :param filename
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/login")
def basic():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route("/")
def index():
    return render_template("index.html")


app.secret_key = 'secret string'


@app.route("/flash")
def just_flash():
    flash(" I am flash, who is looking for me!")
    # flash(u"你好，我是闪电")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)