#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/16
@contact: tenyun.zhang.cs@gmail.com
"""
import csv
import logging
import os
import pickle

import numpy as np

from config import DefaultConfig

"""
加载数据、处理数据
"""
opt = DefaultConfig()
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO,
                    filename=opt.env + ".log",
                    filemode='a+')
path = os.path.split(os.path.abspath(__file__))[0]
csv.field_size_limit(100000000)


class DataLoader:

    def __init__(self, path):
        self.path = path

    def load_data(self, path, dataset="umls", use_shuffle=False, use_drop=False):
        datapath = path + "/" + dataset
        files = os.listdir(datapath)
        tokens = []
        cuis = []
        sentences = []
        labels = []
        word2cui = {}
        for file in files:
            label = file[0]
            sentence = []
            sentences2tokens = []
            sentences2cuis = []
            file_labels = []
            with open(os.path.join(datapath, file)) as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    sentence.append(row[0])
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

            tokens = tokens + sentences2tokens
            cuis = cuis + sentences2cuis
            sentences = sentences + sentence
            labels = labels + file_labels
        word2cui["</PAD>"] = "C0000000"
        with open(opt.word2cui, 'wb') as f:
            pickle.dump(word2cui, f)

        d = {"P": 0, "I": 1, "O": 2, "N": 3}
        labels = [d[x] for x in labels]
        return tokens, cuis, sentences, labels

    def drop_word(self, line, c):
        np.random.seed(1)
        random_list = np.random.randint(0, len(line), size=len(line) // 10)
        for i in random_list:
            line[i] = c
        return line
