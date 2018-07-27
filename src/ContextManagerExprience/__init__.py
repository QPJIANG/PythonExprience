#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager

@contextmanager
def testContext(testargs):
    try:
        if len(testargs) == 1:
            yield {"result": True}
        else:
            yield {"result": False}
    except:
        yield {"result": None}

    finally:
        print("clean")

if __name__ == '__main__':
    with testContext("12") as x:
        print(x)
