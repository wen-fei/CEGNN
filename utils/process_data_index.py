#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/11
@contact: tenyun.zhang.cs@gmail.com
"""
import pandas as pd
import numpy as np
import json
import networkx as nx

"""
transform data from node1, node2 to node1_index, node2_index
"""


def drugbank():
    data = pd.read_csv("G:\\CEGNN\\materials\\umls\\umls_rel_RLRQSIBCHD.csv", delimiter=" ",
                       encoding="utf-8", names=["node_1", "node_2"])
    node_1 = data["node_1"].values.tolist()
    node_2 = data["node_2"].values.tolist()
    all = set(node_1) | set(node_2)
    nodes = pd.Series(list(all))
    index_node = pd.DataFrame()
    index_node["index"] = pd.Series(nodes.index.tolist())
    index_node["node"] = nodes
    index_node.to_csv("drugbank_index2id_edges.csv", sep="\t", encoding="utf-8", header=None, index=False)


def umls():
    data = pd.read_csv("G:\\CEGNN\\materials\\umls\\cuis_all.csv", delimiter=" ",
                       encoding="utf-8", names=["node_1"])
    nodes = data["node_1"].apply(lambda x: int(x[1:]))
    data["index"] = nodes.index
    data["node_1"] = nodes
    data = data[["index", "node_1"]]
    data.to_csv("umls_index2id_edges.csv", sep="\t",
                encoding="utf-8", header=None, index=False)


def drugbank_renode():
    node_node = pd.read_csv("G:\\CEGNN\\utils\\drugbank_d2d.cites", delimiter=" ",
                            encoding="utf-8", names=["node_1", "node_2"])
    index_node = pd.read_csv("G:\\CEGNN\\utils\\drugbank_index2id_edges.csv",
                             delimiter="\t", encoding="utf-8",
                             names=["index", "node"])
    node2index = {str(row["node"]): str(row["index"]) for _, row in index_node.iterrows()}
    node_node = node_node[["node_1", "node_2"]].astype(str)
    index2index = node_node[["node_1", "node_2"]].applymap(lambda x: node2index[x])
    index2index.to_csv("drugbank_index2index_edges.csv", sep=",",
                       encoding="utf-8", header=["node_1", "node_2"],
                       index=False)


def umls_renode():
    node_node = pd.read_csv("G:\\CEGNN\\materials\\umls\\umls_rel_7600w.csv", delimiter="\t",
                            encoding="utf-8", names=["node_1", "node_2"])
    index_node = pd.read_csv("G:\\CEGNN\\utils\\umls_index2id_edges.csv",
                             delimiter="\t", encoding="utf-8",
                             names=["index", "node"])
    node2index = {str(row["node"]): str(row["index"]) for _, row in index_node.iterrows()}
    node_node = node_node[["node_1", "node_2"]].astype(str)
    index2index = node_node[["node_1", "node_2"]].applymap(lambda x: node2index[x])
    index2index.to_csv("umls_index2index_edges.csv", sep=",",
                       encoding="utf-8", header=["node_1", "node_2"],
                       index=False)


def drugbank_json():
    graph = nx.read_edgelist(path="drugbank_index2index_edges_nohead.csv", delimiter=",",
                             encoding="utf-8")
    nodes = graph.nodes()
    adjs = {node: [n for n in graph.neighbors(node)] for node in nodes}
    with open("drugbank_features.json", "w", encoding='utf-8') as f:
        json.dump(adjs, f)


drugbank_json()
