#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
singleton for wapper
"""


def singleton(cls):
    _instance = {}  # 单线访问

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
