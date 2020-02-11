#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/11
@contact: tenyun.zhang.cs@gmail.com
"""
import pandas as pd
import numpy as np

"""
transform data from node1, node2 to node1_index, node2_index
"""

data = pd.read_csv("G:/CEGNN/utils/drugbank_d2d.cites", delimiter=" ",
                   encoding="utf-8", names=["node_1", "node_2"])
node_1 = data["node_1"].values.tolist()
node_2 = data["node_2"].values.tolist()
all = set(node_1) | set(node_2)
nodes = pd.Series(list(all))
index_node = pd.DataFrame()
index_node["index"] = pd.Series(nodes.index.tolist())
index_node["node"] = nodes
index_node.to_csv("drugbank_index2id_edges.csv", sep="\t", encoding="utf-8", header=None, index=False)
