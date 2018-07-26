#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

class RedisHelper:
    def __init__(self):
        self.__conn = redis.Redis(host='localhost')
        self.chan_sub = 'test'
        self.chan_pub= 'test'

#发送消息
    def public(self,msg):
        self.__conn.publish(self.chan_pub,msg)
        return True
#订阅
    def subscribe(self):
        #打开收音机
        pub = self.__conn.pubsub()
        #调频道
        pub.subscribe(self.chan_sub)
        #准备接收
        pub.parse_response()
        return pub