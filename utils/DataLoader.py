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
import time

import gensim
import numpy as np
from tqdm import tqdm

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

    def load_data(self, path, dataset, use_shuffle=False, use_drop=False):
        """
        load PICO related files data
        """
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

    def load_embedding(self, path, file_name, vocab, dim=200):
        """
        load embedding file and store word include only to save memory
        """
        emb_path = path + "/" + file_name
        emb_store = path + "/" + os.path.splitext(file_name)[0] + ".pl"
        if os.path.exists(emb_store):
            with open(emb_store, 'rb') as f:
                return pickle.load(f)
        logging.info("load {} embedding...".format(file_name))
        tic = time.time()
        model = gensim.models.KeyedVectors.load_word2vec_format(emb_path, binary=True)
        logging.info('{} load done.  (time used: {:.1f}s)\n'.format(file_name, time.time() - tic))
        embedding_weights = {}
        found = 0
        notfound = 0
        logging.info("start index word include embedding vector and store...")
        for index, word in tqdm(vocab.items()):
            if word in model.vocab:
                embedding_weights[index] = model.word_vec(word)
                found += 1
            else:
                embedding_weights[index] = np.random.uniform(-0.25, 0.25, dim).astype(np.float32)
                notfound += 1
        logging.info("found_cnt size is :" + str(found))
        logging.info("not found_cnt size is :" + str(notfound))
        logging.info("embedding_weights size is %s " % (len(embedding_weights)))
        with open(emb_store, 'wb') as f:
            pickle.dump(embedding_weights, f)
        return embedding_weights
