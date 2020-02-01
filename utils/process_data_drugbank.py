#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/29
@contact: tenyun.zhang.cs@gmail.com
"""

import lxml.etree as ET
from tqdm import tqdm
import numpy as np
from gensim.models import KeyedVectors
import pandas as pd
from gensim.models import Word2Vec

Word2Vec()
wv_from_text = KeyedVectors.load_word2vec_format("G:\CEGNN\materials\drugbank\drugbank_node2vec_200.emb",
                                                 binary=False, encoding="utf8",
                                                 unicode_errors='ignore')  # C text format
print("word2vec load succeed")
# 所有文本构建词汇表，words_cut 为分词后的list，每个元素为以空格分隔的str.
words_cut = []
vocabulary = list(set([word for item in words_cut for word in item.split()]))
# 构建词汇-向量字典
vocabulary_vector = {}
for word in vocabulary:
    if word in wv_from_text:
        vocabulary_vector[word] = wv_from_text[word]
# 储存词汇-向量字典，由于json文件不能很好的保存numpy词向量，故使用csv保存
pd.DataFrame(vocabulary_vector).to_csv("vocabulary_vector.csv")


def data_process():
    drugbank_path = "G:\\CEGNN\\materials\\drugbank_all_full_database\\drugbank.xml"
    drugbank = ET.parse(drugbank_path)
    root = drugbank.getroot()
    # nodes = root.xpath("//drugbank-id[@primary='true']")
    # for node in nodes:
    #     print(node.text)
    ns = {'db': 'http://www.drugbank.ca'}
    drug_content = []
    drug_network = []

    for drug in tqdm(root.xpath("db:drug[db:groups/db:group='approved']", namespaces=ns)):
        drugName = drug.find("db:name", ns).text
        drugbank_id = drug.find("db:drugbank-id[@primary='true']", ns).text
        drugDescription = drug.find("db:description", ns).text
        if drugDescription is not None:
            drugDescription = drugDescription.replace("\n", "")
            drugDescription = drugDescription.replace("\r", "")
        state = drug.find("db:state", ns)
        if state is not None:
            state = state.text
        else:
            state = "None"
        drug_interactions = drug.xpath("db:drug-interactions/db:drug-interaction", namespaces=ns)
        drug_content.append([drugbank_id, drugName, state, drugDescription])
        for t in drug_interactions:
            t_drugbank_id = t.find("db:drugbank-id", ns).text
            name = t.find("db:name", ns).text
            interaction = t.find("db:description", ns).text
            drug_network.append([int(drugbank_id[2:]), int(t_drugbank_id[2:]), name, interaction, "1"])
            # drug_network.append([drugbank_id, t_drugbank_id, name, interaction, "1"])
    drug_content = np.array(drug_content, dtype=np.str)
    drug_network = np.array(drug_network, dtype=np.str)
    # np.savetxt("drugbank.content", drug_content, fmt="%s", delimiter=',', encoding="utf-8")
    # np.savetxt("drugbank.cites", drug_network, fmt="%s", delimiter=',', encoding="utf-8")
    # np.savetxt("drugbank_d2d.cites", drug_network[:, [0, 1]], fmt="%s", delimiter=" ", encoding="utf-8")
    np.savetxt("drugbank_d2d_LINE.cites", drug_network[:, [0, 1, 4]], fmt="%s", delimiter=" ", encoding="utf-8")
