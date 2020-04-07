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
import xmlschema

# Word2Vec()
# wv_from_text = KeyedVectors.load_word2vec_format("G:\CEGNN\materials\drugbank\drugbank_node2vec_200.emb",
#                                                  binary=False, encoding="utf8",
#                                                  unicode_errors='ignore')  # C text format
# print("word2vec load succeed")
# # 所有文本构建词汇表，words_cut 为分词后的list，每个元素为以空格分隔的str.
# words_cut = []
# vocabulary = list(set([word for item in words_cut for word in item.split()]))
# # 构建词汇-向量字典
# vocabulary_vector = {}
# for word in vocabulary:
#     if word in wv_from_text:
#         vocabulary_vector[word] = wv_from_text[word]
# # 储存词汇-向量字典，由于json文件不能很好的保存numpy词向量，故使用csv保存
# pd.DataFrame(vocabulary_vector).to_csv("vocabulary_vector.csv")


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
    drug_action = []

    for drug in tqdm(root.xpath("db:drug[db:groups/db:group='approved']", namespaces=ns)):
        # for drug in tqdm(root.xpath("db:drug", namespaces=ns)):
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
        target = drug.xpath("db:targets/db:target", namespaces=ns)
        if len(target) > 0:
            t = target[0]
            action = t.find("db:actions/db:action", ns)
            if action is not None:
                action = action.text
            else:
                action = "None"
        else:
            action = None
        drug_action.append([drugbank_id, action])
        drug_content.append([drugbank_id, drugName, state, drugDescription])
        for t in drug_interactions:
            t_drugbank_id = t.find("db:drugbank-id", ns).text
            name = t.find("db:name", ns).text
            interaction = t.find("db:description", ns).text
            drug_network.append([int(drugbank_id[2:]), int(t_drugbank_id[2:]), name, interaction, "1"])
            # drug_network.append([drugbank_id, t_drugbank_id, name, interaction, "1"])
    # drug_content = np.array(drug_content, dtype=np.str)
    # drug_network = np.array(drug_network, dtype=np.str)
    drug_action = np.array(drug_action, dtype=np.str)
    # np.savetxt("drugbank_all.content", drug_content, fmt="%s", delimiter='|', encoding="utf-8")
    # np.savetxt("drugbank_all.cites", drug_network, fmt="%s", delimiter=',', encoding="utf-8")
    # np.savetxt("drugbank_all_d2d.cites", drug_network[:, [0, 1]], fmt="%s", delimiter=" ", encoding="utf-8")
    # np.savetxt("drugbank_all_d2d_LINE.cites", drug_network[:, [0, 1, 4]], fmt="%s", delimiter=" ", encoding="utf-8")
    np.savetxt("drugs_labels.csv", drug_action, fmt="%s", delimiter=",", encoding="utf-8")


def get_labels():
    data = pd.read_csv("G:\\CEGNN\\materials\\drugbank\\drugbank2.content", delimiter="|",
                       names=["drugbank_id", "drugName", "state", "desc"], index_col=False)
    ids_labels = data[["drugbank_id", "state"]]
    ids_labels.to_csv("G:\\CEGNN\\materials\\drugbank\\drugbank_labels.csv",
                      encoding="utf-8", sep=",", header=False, index=False)


def process_drugbank_attribute():
    """
    提取DrugBank属性特征
    提取关联的蛋白质
    """
    drugbank_path = "G:\\CEGNN\\materials\\drugbank_all_full_database\\drugbank.xml"
    drugbank = ET.parse(drugbank_path)
    root = drugbank.getroot()
    ns = {'db': 'http://www.drugbank.ca'}
    drug_attribute = []
    drug_uniprots = []

    for drug in tqdm(root.xpath("db:drug[db:groups/db:group='approved']", namespaces=ns)):
        drugName = drug.find("db:name", ns).text
        drugbank_id = drug.find("db:drugbank-id[@primary='true']", ns).text
        drugDescription = drug.find("db:description", ns).text
        cas_number = drug.find("db:cas-number", ns).text
        unii = drug.find("db:unii", ns).text

        if drugDescription is not None:
            drugDescription = drugDescription.replace("\n", "")
            drugDescription = drugDescription.replace("\r", "")
        state = drug.find("db:state", ns)
        if state is not None:
            state = state.text
        else:
            state = "None"

        drug_interactions = drug.xpath("db:drug-interactions/db:drug-interaction", namespaces=ns)
        interactions_count = len(drug_interactions)

        group = drug.xpath("db:groups/db:group", namespaces=ns)
        group_name = ""
        if group is not None:
            for g in group:
                group_name = group_name + "#" + g.text



        clsf = drug.find("db:classification", ns)
        direct_parent = "None"
        kingdom = "None"
        superclass = "None"
        cclass = "None"
        subclass = "None"
        if clsf is not None:
            direct_parent = clsf.find("db:direct-parent", ns).text
            kingdom = clsf.find("db:kingdom", ns).text
            superclass = clsf.find("db:superclass", ns).text
            cclass = clsf.find("db:class", ns).text
            subclass = clsf.find("db:subclass", ns).text
        drug_attribute.append([drugbank_id, drugName, state,
                               cas_number, unii, interactions_count,
                               group_name, direct_parent, kingdom,
                               superclass, cclass, subclass, drugDescription])
        uniprot_ids = drug.xpath("db:pathways/db:pathway/db:enzymes/db:uniprot-id", namespaces=ns)
        if uniprot_ids is not None:
            for uniprot_id in uniprot_ids:
                drug_uniprots.append([drugbank_id, uniprot_id.text])
    drug_attribute = np.array(drug_attribute, dtype=np.str)
    drug_uniprots = np.array(drug_uniprots, dtype=np.str)
    # 因为描述里有逗号，所以分隔符换成“|”
    drug_attribute_df = pd.DataFrame(drug_attribute, columns=["drugbank_id", "drugName", "state",
                                                              "cas_number", "unii", "interactions_count",
                                                              "group_name", "direct_parent", "kingdom",
                                                              "superclass", "cclass", "subclass", "drugDescription"])
    drug_uniprots_pd = pd.DataFrame(drug_uniprots, columns=["drugbank_id", "uniprot_id"])
    drug_attribute_df.to_csv("drugbank_attribute.csv", sep="\t", encoding="utf-8", index=False)
    drug_uniprots_pd.to_csv("drugbank_uniprots.csv", sep="\t", encoding="utf-8", index=False)
    # np.savetxt("drugbank_attribute.csv", drug_attribute, fmt="%s", delimiter='|', encoding="utf-8")
    # np.savetxt("drugbank_uniprots.csv", drug_uniprots, fmt="%s", delimiter='\t', encoding="utf-8")


# get_labels()
# data_process()
process_drugbank_attribute()
