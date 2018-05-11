#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import os
import yaml
from logging.handlers import RotatingFileHandler

from common.pathlibx import pathlibx


class LogManager(object):
    loggers = {}
    config_ed = False
    log_level = {
        "CRITICAL": 50,
        "FATAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "WARN": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0
    }
    def logging_conf(self):
        config_file = os.path.join(pathlibx.getConfPath(), "logging.yaml")
        with open(config_file, 'r', encoding='utf-8') as f:
            cont = f.read()
            x = yaml.load(cont)
            return x

    def _check_log_path(self):
        logging_path = os.path.join(pathlibx.getRootPath(), "logs")
        if not pathlibx.isExists(logging_path):
            os.mkdir(logging_path)
        pass

    def getLogger(self, name):
        _logger = LogManager.loggers.get(name, None)
        if _logger is not None:
            return _logger
        else:
            self._check_log_path()
            logging_confs= self.logging_conf()

            _logger = logging.getLogger(name)
            formatter_str = '%(asctime)s : %(name)s : %(levelname)s: %(message)s'
            formatter = logging.Formatter(formatter_str)
            level = LogManager.log_level.get(logging_confs.get("logging_level"))

            logging.basicConfig(level=level, format=formatter_str)
            logging_path = os.path.join(pathlibx.getRootPath(), "logs")
            logging_filename = os.path.join(logging_path, name + ".log")

            r_handler = RotatingFileHandler(logging_filename, maxBytes=30 * 1024, backupCount=3)
            r_handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setFormatter(formatter)

            _logger.addHandler(r_handler)
            # _logger.addHandler(console)
            _logger.setLevel(logging.INFO)

            LogManager.loggers[name] = _logger
            return _logger


logging_manager = LogManager()