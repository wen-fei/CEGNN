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
from collections import Counter

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


def load_embeddings(nodes_list, embedding_file, dim=200):
    """
    针对gensim Word2vec模型保存的embedding文件进行读取
    """
    embeddings_model = gensim.models.KeyedVectors.load_word2vec_format(embedding_file, binary=False,
                                                                       unicode_errors='ignore')
    tic = time.time()
    # print('{} load done.  (time used: {:.1f}s)\n'.format(model, time.time() - tic))
    embedding_weights = []
    found = 0
    notfound = 0
    # print("start index word include embedding vector and store...")
    for node in nodes_list:
        node = int(node[2:])
        if str(node) in embeddings_model.vocab:
            embedding_weights.append(embeddings_model.word_vec(str(node)))
            found += 1
        else:
            embedding_weights.append(np.random.uniform(-0.25, 0.25, dim).astype(np.float32))
            notfound += 1
    # print("found_cnt size is :" + str(found))
    # print("not found_cnt size is :" + str(notfound))
    # print("embedding_weights size is %s " % (len(embedding_weights)))
    return embedding_weights


def load_embedding_asne(nodes_list, embedding_file, dim=200):
    """
    针对asne模型的输出文件读取embedding
    """
    emb = pd.read_csv(embedding_file, index_col=False)
    n2i = {}
    index2node = pd.read_csv("G:\\CEGNN\\materials\\drugbank\\drugbank_index2id_edges.csv",
                             delimiter="\t", encoding="utf-8", names=["index", "node"], dtype=str)
    for index, row in index2node.iterrows():
        n2i[row["node"]] = row["index"]
    embedding_weights = []
    emb["id"] = emb["id"].apply(lambda x: str(int(x)))
    indexes = {x: 1 for x in list(emb["id"])}
    for node in nodes_list:
        node = str(int(node[2:]))
        if node in n2i:
            if n2i[node] in indexes:
                vector = emb[emb["id"] == n2i[node]].values.tolist()[0][1:]
                embedding_weights.append(vector)
            else:
                embedding_weights.append(np.random.uniform(-0.25, 0.25, dim).astype(np.float32))
        else:
            embedding_weights.append(np.random.uniform(-0.25, 0.25, dim).astype(np.float32))
    return embedding_weights


def load_embedding_gemsec(nodes_list, embedding_file, dim=200):
    """
    针对gemsec模型的输出文件读取embedding
    """
    emb = pd.read_csv(embedding_file, index_col=False)
    n2i = {}
    index2node = pd.read_csv("G:\\CEGNN\\materials\\drugbank\\drugbank_index2id_edges.csv",
                             delimiter="\t", encoding="utf-8", names=["index", "node"], dtype=str)
    for index, row in index2node.iterrows():
        n2i[row["node"]] = row["index"]
    embedding_weights = []
    # emb["id"] = emb["id"].apply(lambda x: str(int(x)))
    indexes = {str(x): 1 for x in list(emb.index)}
    for node in nodes_list:
        node = str(int(node[2:]))
        if node in n2i:
            if n2i[node] in indexes:
                vector = emb.iloc[int(n2i[node])].tolist()
                embedding_weights.append(vector)
            else:
                embedding_weights.append(np.random.uniform(-0.25, 0.25, dim).astype(np.float32))
        else:
            embedding_weights.append(np.random.uniform(-0.25, 0.25, dim).astype(np.float32))
    return embedding_weights


def node_classification(model, emb_path, embedding, dim=200):
    if model == "ASNE":
        features = load_embedding_asne(nodes, os.path.join(emb_path, embedding), dim)
    elif model == "GEMSEC":
        features = load_embedding_gemsec(nodes, os.path.join(emb_path, embedding), dim)
    else:
        features = load_embeddings(nodes, os.path.join(emb_path, embedding), dim)
    results = []
    for labeled_part in np.arange(0.3, 0.9, 0.3):
        labeled_part = round(labeled_part, 1)
        clf = LogisticRegression()
        # clf = svm.SVR(decision_function_shape='ovo')
        # clf = svm.LinearSVR()
        x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=labeled_part, random_state=0)
        clf.fit(X=x_train, y=y_train)
        y_predict = clf.predict(x_test)
        precision = precision_score(y_test, y_predict, average="weighted")
        recall = recall_score(y_test, y_predict, average="weighted")
        f1 = f1_score(y_test, y_predict, average="weighted")
        micro_f1 = f1_score(y_true=y_test, y_pred=y_predict, labels=list(set(labels)), average="micro")
        macro_f1 = f1_score(y_true=y_test, y_pred=y_predict, labels=list(set(labels)), average="macro")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = "{} : model: {} node-classification : " \
                 "labeled nodes(%): {} " \
                 "P:{:.4f} R:{:.4f} F1:{:.4f} " \
                 "Micro_F1: {:.4f} " \
                 "Macro_F1: {:.4f}".format(now, model_name, str(labeled_part * 100) + "%",
                                           precision, recall, f1, micro_f1,
                                           macro_f1)
        results.append(result)
    with open("node_classification.result", "a+") as f:
        for line in results:
            f.write(line)
            f.write("\n")
        f.write("\n")


if __name__ == '__main__':
    # dataset_path = "/home/gp/stu/ztt/data/drugbank/"
    dataset_path = "G:\\CEGNN\\materials\\umls"
    # emb_path = "/home/gp/stu/ztt/data/embs/drugbank/"
    emb_path = "G:\\CEGNN\\materials\\emb\\umls"
    # Counter({'solid': 2200, 'None': 1496, 'liquid': 284, 'gas': 8})
    # dataset = "drugsbank_action_labels.csv"
    dataset = "umls_sty_samples.csv"
    drugbank_models = {
        "ASNE": "drugbank_asne_200.emb",
        "deepwalk": "drugbank_deepwalk_200.embeddings",
        "GEMSEC": "drugbank_GEMSEC_200.emb",
        "node2vec": "drugbank_node2vec_200.emb",
        "struct2vec": "drugbank_struct2vec_200.emb",
        "LINE": "vec_drugbank_all.txt"
    }

    umls_models = {
        "deepwalk": "umls_deepwalk_200.embeddings",
    }

    ids_labels = pd.read_csv(os.path.join(dataset_path, dataset), delimiter=",", dtype=np.dtype(str),
                             names=["ids", "labels"])
    ids_labels = ids_labels[ids_labels["labels"] != "None"]
    nodes = ids_labels["ids"].tolist()
    labels = ids_labels["labels"].tolist()
    # s = Counter(labels)
    for model_name, embedding in tqdm(drugbank_models.items()):
        if model_name == "LINE":
            node_classification(model_name, emb_path, embedding, dim=400)
        else:
            node_classification(model_name, emb_path, embedding)
