#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/3/3
@contact: tenyun.zhang.cs@gmail.com
"""
import logging
import os
import time
import gensim
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def load_embeddings(model, nodes_list, embedding_file, dim=200):
    embeddings_model = gensim.models.KeyedVectors.load_word2vec_format(embedding_file, binary=False,
                                                                       unicode_errors='ignore')
    logging.info("load {} embedding...".format(embedding_file))
    tic = time.time()
    logging.info('{} load done.  (time used: {:.1f}s)\n'.format(model, time.time() - tic))
    embedding_weights = []
    found = 0
    notfound = 0
    logging.info("start index word include embedding vector and store...")
    for node in tqdm(nodes_list):
        if id in embeddings_model.vocab:
            embedding_weights.append(embeddings_model.word_vec(node[2:]))
            found += 1
        else:
            embedding_weights.append(np.random.uniform(-0.25, 0.25, dim).astype(np.float32))
            notfound += 1
    logging.info("found_cnt size is :" + str(found))
    logging.info("not found_cnt size is :" + str(notfound))
    logging.info("embedding_weights size is %s " % (len(embedding_weights)))
    return embedding_weights


def node_classification(dataset_path, dataset, model, emb_path, embedding, dim=200):
    ids_labels = np.genfromtxt(os.path.join(dataset_path, dataset), delimiter=",", dtype=np.dtype(str))
    nodes = ids_labels[:, 0]
    labels = ids_labels[:, -1]
    features = load_embeddings(model, nodes, os.path.join(emb_path, embedding), dim)

    lr = LogisticRegression()
    clf = svm.SVC(decision_function_shape='ovo')
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=0)
    clf.fit(X=x_train, y=y_train)
    y_predict = clf.predict(x_test)
    precision = precision_score(y_test, y_predict, average=None)
    recall = recall_score(y_test, y_predict, average=None)
    f1 = f1_score(y_test, y_predict, average=None)
    micro_f1 = f1_score(y_true=y_test, y_pred=y_predict, labels=list(set(labels)), average="micro")
    macro_f1 = f1_score(y_true=y_test, y_pred=y_predict, labels=list(set(labels)), average="macro")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = "{} : the model of {} node classification " \
             "experiment result is : " \
             "P:{} R:{} F1:{} Micro_F1: {} Macro_F1: {}".format(now, dataset, precision,
                                                                recall, f1, micro_f1, macro_f1)
    with open("node_classification.result", "a+") as f:
        f.write(result)
        f.write("\r\n")


if __name__ == '__main__':
    # dataset_path = "/home/gp/stu/ztt/data/drugbank/"
    dataset_path = "G:\\CEGNN\\materials\\drugbank"
    # emb_path = "/home/gp/stu/ztt/data/embs/drugbank/"
    emb_path = "G:\\CEGNN\\materials\\emb\\drugbank"
    dataset = "drugbank_labels.csv"
    models = {
        # "ASNE": "drugbank_asne_200.emb",
        "deepwalk": "drugbank_deepwalk_200.embeddings",
        # "GEMSEC": "drugbank_GEMSEC_200.emb",
        "node2vec": "drugbank_node2vec_200.emb",
        "struct2vec": "drugbank_struct2vec_200.emb",
        "LINE": "vec_drugbank_all.txt"
    }
    for model_name, embedding in tqdm(models.items()):
        node_classification(dataset_path, dataset, model_name, emb_path, embedding)
