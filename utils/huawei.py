#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/19
@contact: tenyun.zhang.cs@gmail.com
"""

import sys

Precision = 0.891
Recall = 0.934
F1 = 2 * (Precision * Recall) / (Precision + Recall)
print(F1)
