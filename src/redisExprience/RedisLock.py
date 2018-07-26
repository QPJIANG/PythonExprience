#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import redis


"""
https://blog.csdn.net/Dennis_ukagaka/article/details/78072274
redis能用的的加锁命令分表是INCR、SETNX、SET
INCR:
这种加锁的思路是， key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作进行加一。
然后其它用户在执行 INCR 操作进行加一时，如果返回的数大于 1 ，说明这个锁正在被使用当中。
1、 客户端A请求服务器获取key的值为1表示获取了锁
2、 客户端B也去请求服务器获取key的值为2表示获取锁失败
3、 客户端A执行代码完成，删除锁
4、 客户端B在等待一段时间后在去请求的时候获取key的值为1表示获取锁成功
5、 客户端B执行代码完成，删除锁

$redis->incr($key);
$redis->expire($key, $ttl); //设置生成时间为1秒


SETNX
如果 key 不存在，将 key 设置为 value
如果 key 已存在，则 SETNX 不做任何动作
1、 客户端A请求服务器设置key的值，如果设置成功就表示加锁成功
2、 客户端B也去请求服务器设置key的值，如果返回失败，那么就代表加锁失败
3、 客户端A执行代码完成，删除锁
4、 客户端B在等待一段时间后在去请求设置key的值，设置成功
5、 客户端B执行代码完成，删除锁

$redis->setNX($key, $value);
$redis->expire($key, $ttl);

set：
1、 客户端A请求服务器设置key的值，如果设置成功就表示加锁成功
2、 客户端B也去请求服务器设置key的值，如果返回失败，那么就代表加锁失败
3、 客户端A执行代码完成，删除锁
4、 客户端B在等待一段时间后在去请求设置key的值，设置成功
5、 客户端B执行代码完成，删除锁


"""


class RedisLock(object):
    def __init__(self, key):
        self.rdcon = redis.Redis(host='localhost', port=6379, password="", db=1)
        self._lock = 0
        self.lock_key = "%s_dynamic_test" % key

    @staticmethod
    def get_lock(cls, timeout=10):
        while cls._lock != 1:
            timestamp = time.time() + timeout + 1
            cls._lock = cls.rdcon.setnx(cls.lock_key, timestamp)
            if cls._lock == 1 or (
                    time.time() > cls.rdcon.get(cls.lock_key) and time.time() > cls.rdcon.getset(cls.lock_key,
                                                                                                 timestamp)):
                print "get lock"
                break
            else:
                time.sleep(0.3)

    @staticmethod
    def release(cls):
        if time.time() < cls.rdcon.get(cls.lock_key):
            print "release lock"
            cls.rdcon.delete(cls.lock_key)


def deco(cls):
    def _deco(func):
        def __deco(*args, **kwargs):
            print "before %s called [%s]." % (func.__name__, cls)
            cls.get_lock(cls)
            try:
                return func(*args, **kwargs)
            finally:
                cls.release(cls)

        return __deco

    return _deco


@deco(RedisLock("112233"))
def myfunc():
    print "myfunc() called."
    time.sleep(1)


if __name__ == "__main__":

    myfunc()