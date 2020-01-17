#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/16
@contact: tenyun.zhang.cs@gmail.com
"""
import datetime
import os

today = datetime.date.today()
path = os.path.abspath("..")


class DefaultConfig(object):
    """ default parameters and settings """
    words_save = "materials/words.dat"
    cuis_save = "materials/cuis.dat"
    word2cui = "materials/word2cui.dat"
    vocabulary_store = "materials/vocabulary_store.dat"

    word_embeddings = "materials/PubMed_extracted.pl"
