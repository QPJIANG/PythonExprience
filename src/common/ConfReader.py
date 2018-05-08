#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import platform
from common.pathlibx import pathlibx
import os
import yaml


class YamlConfRreader():
    def __init__(self, file):
        self.config = {}
        self.load(file)

    def load(self, file):
        self.filename = os.path.join(pathlibx.getConfPath(), file)
        if pathlibx.isFile(self.filename):
            f = open(self.filename, 'r', encoding='utf-8')
            _filecontent = f.read()
            self.config = yaml.load(_filecontent)

    pass


def test():
    yamlreader = YamlConfRreader("conf.yaml")
    config = yamlreader.config
    print(config)
    print(config.get("x", None))
    pass


if __name__ == '__main__':
    test()
