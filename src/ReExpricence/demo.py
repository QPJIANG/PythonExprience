#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


"""

prog = re.compile(pattern)
result = prog.match(string)
等效于
result = re.match(pattern, string)
但使用re.compile()和保存所产生的正则表达式对象重用效率更高时该表达式会在单个程序中多次使用。
"""
if __name__ == "__main__":
    req = "rusage[xxx_23=4 && xxx_45=4]"
    p1 = re.compile(r'rusage.*xxx_.*')
    p2 = re.compile(r'rusage\[xxx_(.*)=')
    p3 = re.compile(r'rusage\[(.*)\]')

    x = p2.match(req).group(1)
    print x.split("&&")

    print p3.match(req).groups()

    pass