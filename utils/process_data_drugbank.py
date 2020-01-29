#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/29
@contact: tenyun.zhang.cs@gmail.com
"""

import lxml.etree as ET
from tqdm import tqdm

drugbank_path = "G:\\CEGNN\\materials\\drugbank_all_full_database\\drugbank.xml"
drugbank = ET.parse(drugbank_path)
root = drugbank.getroot()
# nodes = root.xpath("//drugbank-id[@primary='true']")
# for node in nodes:
#     print(node.text)
ns = {'db': 'http://www.drugbank.ca'}
for drug in tqdm(root.xpath("db:drug[db:groups/db:group='approved']", namespaces=ns)):
    drugName = drug.find("db:name", ns).text
    drugbank_id = drug.find("db:drugbank-id[@primary='true']", ns).text
    drugDescription = drug.find("db:description", ns).text
    state = drug.find("db:state", ns).text
    drug_interactions = drug.findall("db:drug-interactions/db:drug-interaction/db:drugbank-id", ns)
    interactions = list(set(map(lambda x: x.text, drug_interactions)))
    for id in interactions:
        entity1 = drugbank_id
        entity2 = id
        # TODO write to csv
        pass