#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import os
import pathlib


class pathlibx(object):
    @classmethod
    def getCommenPath(cls):
        return os.path.split(os.path.abspath(__file__))[0]

    @classmethod
    def getRootPath(cls):
        return os.path.split(pathlibx.getCommenPath())[0]

    @classmethod
    def getConfPath(cls):
        return os.path.split(pathlibx.getCommenPath())[0] + os.path.sep + "conf"

    @classmethod
    def getCurrentPath(cls):
        return os.getcwd()

    @classmethod
    def isExists(cls, file_or_path=None):
        if file_or_path is None:
            return False
        return os.path.exists(file_or_path)

    @classmethod
    def isFile(cls, file=None):
        if file is None:
            return False
        path = pathlib.Path(file)
        return path.is_file()


if __name__ == "__main__":
    print(pathlibx.getCommenPath())
    print(pathlibx.getRootPath())
    print(pathlibx.getConfPath())
    print(pathlibx.getCurrentPath())
    print(pathlibx.isExists())
    print(pathlibx.isExists(pathlibx.getCurrentPath()))
    print(pathlibx.isFile(pathlibx.getCurrentPath()))
    path = pathlib.Path("file")
    print(path.is_file())
    pass
