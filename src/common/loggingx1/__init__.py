#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import os

from common.pathlibx import pathlibx


def setup_logging():
    conf = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {'format': '%(asctime)s | %(name)s | %(levelname)s | %(message)s'}
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple'
            },
            'info_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'filename': 'test.log',
                'maxBytes': 1024,
                'backupCount': 2,
                'encoding': 'utf8'}
        },
        'loggers': {
            'default': {
                'level': 'DEBUG', 'handlers': ['console', 'info_file_handler'],
                'propagate': False}
        },
        'roots': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True}
    }

    logging_path = os.path.join(pathlibx.getRootPath(), "logs")
    if not pathlibx.isExists(logging_path):
        os.mkdir(logging_path)

    logging_filename = os.path.join(logging_path, "default_log.log")
    conf["handlers"]["info_file_handler"]["filename"] = logging_filename
    logging.config.dictConfig(conf)


setup_logging()

logger = logging.getLogger("default")
