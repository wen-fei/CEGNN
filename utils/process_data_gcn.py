#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/16
@contact: tenyun.zhang.cs@gmail.com
"""
import csv
import itertools
import logging
import os
import pickle
import time
from collections import Counter

import gensim as gensim
import numpy as np

from config import DefaultConfig

logger = logging.getLogger(__name__)
opt = DefaultConfig()
DATA_PATH = "/home/gp/workhome/biyesheji/data/"


def transform_data(path=DATA_PATH, dataset="pico_1225"):
    """process pico dataset for gcn"""
    print('Loading {} dataset...'.format(dataset))
    tokens, cuis, sentences, labels = load_pico_data("{}{}".format(path, dataset))
    # just word embedding
    tokens_new = pad_sentences_or_cuis(tokens, padding_str="<PAD/>", maxlen=30)
    cuis = pad_sentences_or_cuis(cuis, padding_str="C0000000", maxlen=150)
    cuis_new = [[int(cui[1:]) if (cui != "NULL" and cui != "") else 0 for cui in line] for line in cuis]
    vocabulary, vocabulary_inv = build_vocab(tokens_new, cuis_new)
    word_embeddings = customize_word_embeddings(opt.word_embeddings, opt.word_embeddings_dim)
    # TODO, 需要的是句子向量
    # references https://blog.csdn.net/asialee_bird/article/details/100124565
    # 根据vocabulary_inv生成句子向量
    tokens_embedding = tokens_to_embeddings(tokens_new, vocabulary, word_embeddings)


def tokens_to_embeddings(tokens, vocabulary, embeddings):
    """ build sentence embedding"""
    sentences_vec = []
    for line in tokens:
        sen_vec = np.zeros(opt.word_embeddings_dim).reshape((1, opt.word_embeddings_dim))
        count = 0
        for token in line:
            word_embedding = embeddings[vocabulary[token]]
            sen_vec += word_embedding
            count += 1
        sen_vec /= count
        sentences_vec.append(sen_vec)
    return sentences_vec


def customize_word_embeddings(path, dim):
    tic = time.time()
    logger.info(
        'Please wait ... (it could take a while to load the word embedding file : {})'.format(path))
    model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    logger.info('Done.  (time used: {:.1f}s)\n'.format(time.time() - tic))
    embedding_weights = {}
    found_cnt = 0
    notfound_cnt = 0
    words = []
    if not os.path.exists(opt.vocabulary_store):
        logging.error("vocabulary file is not found")
        return
    with open(opt.vocabulary_store, 'rb') as data_f:
        vocabulary, vocabulary_inv = pickle.load(data_f)
    for idx, word in vocabulary_inv.items():
        words.append(word)
        if word in model.vocab:
            embedding_weights[idx] = model.word_vec(word)
            found_cnt += 1
        else:
            embedding_weights[idx] = np.random.uniform(-0.25, 0.25, dim).astype(np.float32)
            notfound_cnt += 1
    logger.info("found_cnt size is :" + str(found_cnt),
                "not found_cnt size is :" + str(notfound_cnt),
                "embedding_weights size is %s " % (len(embedding_weights)))
    with open(opt.word_embeddings, 'wb') as f:
        pickle.dump(embedding_weights, f)
    return embedding_weights


def build_vocab(sentences=None):
    """
    Builds a vocabulary mapping from word to index based on the sentences.
    Returns vocabulary mapping and inverse vocabulary mapping.
    """
    # Build vocabulary
    if os.path.exists(opt.vocabulary_store):
        with open(opt.vocabulary_store, 'rb') as f:
            return pickle.load(f)
    else:
        word_counts = Counter(itertools.chain(*sentences))
        # Mapping from index to word
        word_dict = word_counts.most_common()
        vocabulary_inv = [x[0] for x in word_dict]  # {index:str}
        vocabulary_inv.append("UNKNOWN")
        # Mapping from word to index
        vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}  # {str:index}
        vocabulary_inv = {i: x for x, i in vocabulary.items()}
        with open(opt.vocabulary_store, "wb") as f:
            pickle.dump((vocabulary, vocabulary_inv), f)
        return vocabulary, vocabulary_inv


def pad_sentences_or_cuis(sources, padding_token="", maxlen=100):
    """
    Pads all cuis to the same length. The length is 150.（90% of cuis is shorter than 150 ）
    Pads all sentences to the same length. The length is 35.（92% of cuis is shorter than 150 ）
    Returns padded cuis.
    """
    num_samples = len(sources)
    padded_sources = []
    for i in range(num_samples):
        source = sources[i]
        if len(source) > maxlen:
            new_source = source[:maxlen]
        else:
            num_padding = maxlen - len(source)
            new_source = source + [padding_token] * num_padding
        padded_sources.append(new_source)
    return padded_sources


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
