#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/29
@contact: tenyun.zhang.cs@gmail.com
"""
import os
import time

import click
from flask import Flask, render_template, flash, redirect, \
    url_for, request, send_from_directory, g, jsonify
from werkzeug.utils import secure_filename

from extractPDF import ExtractPDF
from forms import LoginForm

app = Flask(__name__)

# file store location
UPLOAD_FOLDER = 'G:\\CEGNN\\web\\hello\\resource\\'
# file type allowed
ALLOWED_EXTENSIONS = set(['pdf', "PDF"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER + "\\pdfs"
app.config['docs_pkl'] = "G:\\CEGNN\\web\\hello\\resource\\docs.pkl"
app.config["abstract_result"] = UPLOAD_FOLDER + "\\abstracts"


def allowed_file(filename):
    """
    check file type
    :param filename
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def read_abstract(path):
    """
    read abstract result
    """
    files = os.listdir(path)
    result = {}
    for file in files:
        with open(os.path.join(path, file), encoding="utf-8") as f:
            result["file"] = f.read()
    return result


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    """
    upload pdf file and store it.
    # TODO: parse multi files
    """
    extractPDF = ExtractPDF()
    response = {}
    if request.method == "POST":
        file = request.files['pdf']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save file
            now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            pdf_path = app.config['UPLOAD_FOLDER'] + "/" + now
            abstract_result_path = app.config['abstract_result'] + "/" + now
            os.mkdir(pdf_path)
            os.mkdir(abstract_result_path)
            path = os.path.join(pdf_path, filename)
            file.save(path)
            # # parse pdf file
            # extractPDF.parse(pdf_path, abstract_result_path, app.config['docs_pkl'])
            # # get pdf file result
            # pdf_sentences = read_abstract(abstract_result_path)
            # # 1. PICO classification
            # # pico = model(pdf_sentences)
            # # 2. 信息量计算、去冗余
            # # pico = pico_filter(pico)
            # # 3. 摘要分类可视化
            # response["ok"] = "True"
            # response["msg"] = pdf_sentences
            response["msg"] = "success"
        else:
            # response["ok"] = "False"
            # response["msg"] = "file is invalid. please re-upload pdf file."
            response["msg"] = "error"
    else:
        response["msg"] = "error"
    return jsonify(response)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    show medical abstract content
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
