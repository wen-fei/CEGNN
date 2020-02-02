#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/2
@contact: tenyun.zhang.cs@gmail.com
"""
import pandas as pd

umls_rel = pd.read_csv("../materials/umls/umls1.rel", delimiter="\t", encoding="GB2312", names=["CUI1", "CUI2", "REL"])
umls_rel = umls_rel.applymap(lambda x: x.split("\"", ""))
cuis = list(pd.read_csv("../materials/umls/cuis_all.csv", names=["CUI"])["CUI"])
umls_rel = umls_rel[(umls_rel["CUI1"].isin(cuis)) & (umls_rel["CUI2"].isin(cuis))]
umls_rel["weight"] = 1
umls_rel1 = umls_rel[["CUI1", "CUI2", "weight"]]
umls_rel1.to_csv("../materials/umls/umls_rel_new.csv", sep="\t", encoding="utf-8", header=None, index=False)
umls_rel.to_csv("../materials/umls/umls_rel_2.csv", sep="\t", encoding="utf-8", header=None, index=False)
print("done")
