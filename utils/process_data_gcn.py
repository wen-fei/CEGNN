#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/16
@contact: tenyun.zhang.cs@gmail.com
"""
import csv
import os
import pickle

import numpy as np

from config import DefaultConfig

opt = DefaultConfig()
DATA_PATH = "/home/gp/workhome/biyesheji/data/"


def transform_data(path=DATA_PATH, dataset="pico_1225"):
    """process pico dataset for gcn"""
    print('Loading {} dataset...'.format(dataset))
    tokens, cuis, sentences, labels = load_pico_data("{}{}".format(path, dataset))


def load_pico_data(self, path, use_shuffle=False, use_drop=False):
    files = os.listdir(path)
    sentences_tokens = []
    sentences_cuis = []
    sentences_origin = []
    labels = []
    word2cui = {}
    for file in files:
        label = file[0]
        sentences = []
        sentences2tokens = []
        sentences2cuis = []
        file_labels = []
        with open(os.path.join(path, file)) as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                sentences.append(row[0])
                tokens = row[1].split(" ")
                sentences2tokens.append(tokens)
                cuis1 = row[2].split("|")
                sentences2cuis.append(cuis1)
                file_labels.append(label)
                for word, cui in zip(tokens, cuis1):
                    word2cui[word] = cui
                if use_shuffle:
                    np.random.seed(1)
                    sentence2 = tokens.copy()
                    np.random.shuffle(sentence2)
                    sentences2tokens.append(sentence2)
                    cuis2 = cuis1.copy()
                    np.random.shuffle(cuis2)
                    sentences2cuis.append(cuis2)
                    file_labels.append(label)
                if use_drop:
                    sentence3 = self.drop_word(tokens, "<PAD/>")
                    sentences2tokens.append(sentence3)
                    cuis3 = self.drop_word(cuis1, "C0000000")
                    sentences2cuis.append(cuis3)
                    file_labels.append(label)

        sentences_tokens = sentences_tokens + sentences2tokens
        sentences_cuis = sentences_cuis + sentences2cuis
        sentences_origin = sentences_origin + sentences
        labels = labels + file_labels
    word2cui["</PAD>"] = "C0000000"
    with open(opt.word2cui, 'wb') as f:
        pickle.dump(word2cui, f)
    d = {"P": 0, "I": 1, "O": 2, "N": 3}
    labels = [d[x] for x in labels]
    return sentences_tokens, sentences_cuis, sentences_origin, labels
