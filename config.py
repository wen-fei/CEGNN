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


class DefaultConfig(object):
    """ default parameters and settings """
    path = os.path.dirname(os.path.abspath(__file__))
    words_save = path + "/materials/words.dat"
    cuis_save = path + "/materials/cuis.dat"
    word2cui = path + "/materials/word2cui.dat"
    vocabulary_store = path + "/materials/vocabulary_store.dat"
    cuis_all = path + "/materials/cuis_all.csv"
    mrcuis = path + "/materials/mrcuis.csv"

    pred_PubMed_vector = path + "/materials/PubMed-shuffle-win-30.bin"
    word_embeddings = path + "/materials/PubMed_extracted.pl"
    word_embeddings_dim = 200
