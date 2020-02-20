#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/2/19
@contact: tenyun.zhang.cs@gmail.com
"""

import sys


def process(man, woman, child):
    score = 0.0
    success = True
    if child > 0:
        if man > 0:
            if woman > 0:
                family = min(man, woman, child)
                score += 5 * family
                man -= family
                woman -= family
                child -= family
                if child > 0:
                    if man > 0:
                        if child != 1 and man != 1:
                            success = False
                        else:
                            score += 5
                    else:
                        c_w = min(child, woman)
                        score += c_w * 3.5
            else:
                if child == 1 and man == 1:
                    score += 5
                else:
                    success = False
        else:
            c_w = min(child, woman)
            score += c_w * 3.5
    else:
        if man != 1 and woman != 1:
            score = -1.0
    if score >= 10:
        score = 10.0
    return success, score


if __name__ == "__main__":
    # 读取第一行的n
    line = sys.stdin.readline().split(" ")
    man = int(line[0])
    woman = int(line[1])
    child = int(line[2])
    result = process(man, woman, child)
    if result[0]:
        if result[1] > 10.0:
            print(10.0)
        else:
            print(result[1])
    else:
        print(0.0)
