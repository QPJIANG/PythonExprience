#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redishelper import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()

while True:
    msg = redis_sub.parse_response()
    print('接收：',msg)