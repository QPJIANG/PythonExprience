#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from redis import client

from common.Singleton import Singleton

_config = {
    "maxcon": 20,
    "timeout": 10,
    "host": "localhost",
    "port": 6379,
    "password": "",
    "sctimeout": 0,
    "stimeout": 300

}


class RedisPoolHolder(object):
    """
        redis pool holder
    """
    __metaclass__ = Singleton
    pool = None
    isPoolOk = False

    def __init__(self,config):
        self.initPool(config)
        pass


    def initPool(self,config):
        try:
            self.__class__.pool = redis.BlockingConnectionPool(max_connections=config['maxcon'],
                                                 timeout=config['maxcon'],
                                                 host=config['host'],
                                                 port=config['port'],
                                                 password=config['password'],
                                                 socket_connect_timeout=config['sctimeout'],
                                                 socket_timeout=config['stimeout'])
            _pool = self.__class__.pool
            conn = None
            try:
                conn = redis.StrictRedis(connection_pool=_pool)
                conn.ping()  # test connect
                self.__class__.isPoolOk = True
            except Exception as ex:
                self.__class__.isPoolOk = False
                print(ex)
            finally:
                # conn 在执行操作时会调用 execute_command
                # execute_command  会根据连接池配置获取连接，执行完操作后释放连接
                # conn 不需要关注连接池释放
               pass
        except Exception as e:
            self.__class__.isPoolOk = False
            print(e)


class RedisTest(object):

    def __init__(self,rph):
        self.rph = rph
        self.conn = None
        _pool = rph.__class__.pool
        try:
            self.conn = redis.StrictRedis(connection_pool=_pool)
        except:
            self.conn = None

    def testString(self):
        """
        set(name, value, ex=None, px=None, nx=False, xx=False)
         ex，过期时间（秒）
         px，过期时间（毫秒）
         nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
         xx，如果设置为True，则只有name存在时，当前set操作才执行'''
        setex(name, value, time) #设置过期时间（秒）
        psetex(name, time_ms, value) #设置过期时间（豪秒）
        """
        _r = self.conn
        _r.set('name', 'zhangsan')
        print(self.conn.get("name"))

        # 批量添加key
        _r.mset(name1='zhangsan', name2='lisi',name3='wangwu')

        # 批量获取
        print(_r.mget(["name1", "name2", "name3"]))

        # 设置新值，返回原值
        print(_r.getset("name", "value"))

        # getrange(key, start, end) # 根据字节获取子序列: 闭区间（包含start,end）
        print(_r.getrange("name", 0, 3))

        # setrange(name, offset, value) # 修改字符串内容，从指定字符串索引开始向后替换，如果新值太长时，则向后添加

        # setbit(name, offset, value)
        # getbit(name, offset)
        # bitcount(key, start=None, end=None)


        _r.delete("name")
        # strlen(name) # Return the number of bytes stored in the value of ``name``

        # incr(self, name, amount=1)
        # #自增mount对应的值，当mount不存在时，则创建mount＝amount，否则，则自增,amount为自增数(整数)
        print(_r.incr("incr"))             # 输出:1 , 创建并设置1
        print(_r.incr("incr", amount=2))  # 输出:3  , 增加2
        # incrbyfloat(self, name, amount=1.0)
        # decr(self, name, amount=1) # 自减 与 incr 类似
        # append(name, value)  字符追加

    def testHash(self):
        r = self.conn
        # hset(name, key, value)  # name对应的hash中设置一个键值对（不存在，则创建，否则，修改）
        # hget(name,key)
        # hgetall(name)   # 获取name对应hash的所有键值 , return dict

        r.hset("dic_name", "a1", "aa")
        r.hset("dic_name", "a2", "aa2")
        print(r.hgetall("dic_name"))

        # hmset(name, mapping)
        # hmget(name, keys, *args)
        # hlen(name) 获取hash中键值对的个数
        # hkeys(name) 获取hash中所有的key的值
        # hvals(name) 获取hash中所有的value的值

        r.hmset("dic_name", {"a1": "a11", "a2": "a22"})
        print(r.hgetall("dic_name"))
        print(r.hmget("dic_name", "a1", "b1"))
        print(r.hlen("dic_name"))
        print(r.hkeys("dic_name"))
        print(r.hvals("dic_name"))

        # hexists(name, key)
        # hdel(name,*keys)
        # hincrby(name, key, amount=1)        # 自增
        # hincrbyfloat(name, key, amount=1.0) # 自增
        # hscan(name, cursor=0, match=None, count=None)
        # hscan_iter(name, match=None, count=None)

    def testList(self):
        """"
        """
        r = self.conn
        # lpush(name, values)
        # rpush(name, values)
        # lrange(name, start, end)  #分片获取元素
        # lpushx(name, value) # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
        # rpushx(name,value)  # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最右边
        # llen(name)
        # linsert(name, where, refvalue, value))
        '''
             参数：
             name: redis的name
             where: BEFORE（前）或AFTER（后）
             refvalue: 列表内的值
             value: 要插入的数据
         '''
        # lset(name, index, value) # 对list中的某一个索引位置重新赋值
        # lrem(name, count,value)
        '''
            参数：
            name:  redis的name
            value: 要删除的值
            num:   num=0 删除列表中所有的指定值；
                   num=2 从前到后，删除2个；
                   num=-2 从后向前，删除2个
        '''
        # lpop(name) # 移除列表的左侧第一个元素，返回值移除值
        # lindex(name, index) # 根据索引获取列表内元素
        # ltrim(name, start, end)  # 移除列表内没有在该索引之内的值
        # rpoplpush(src, dst)   # 从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
        # brpoplpush(src, dst, timeout=0) # 同rpoplpush，多了个timeout, timeout：取数据的列表没元素后的阻塞时间，0为一直阻塞
        # blpop(keys, timeout) # 将多个列表排列,按照从左到右去移除各个列表内的元素
        # brpop(keys, timeout) # 同blpop，将多个列表排列,按照从右像左去移除各个列表内的元素

        r.lpush("list_name", 2)
        r.lpush("list_name", 3, 4, 5)  # 保存在列表中的顺序为5，4，3，2
        print(r.lrange("list_name", 0, -1))
        r.linsert("list_name", "BEFORE", "2", "SS")  # 在列表内找到第一个元素2，在它前面插入SS
        print(r.lrange("list_name", 0, -1))
        # 删除name对应的list中的指定值
        r.lrem("list_name", 0, "SS")
        print(r.lrange("list_name", 0, -1))

        r.delete("list_name")
        r.delete("list_name1")
        r.lpush("list_name", 3, 4, 5)
        r.lpush("list_name1", 3, 4, 5)

        for i in range(0, 7):
            # timeout: 超时时间，获取完所有列表的元素之后，阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞
            print(r.brpop(["list_name", "list_name1"], timeout=1))  # timeout 后return None
            print(r.lrange("list_name", 0, -1), r.lrange("list_name1", 0, -1))

    def testSet(self):
        r = self.conn
        # sadd(name,values)
        # smembers(name)
        # scard(name) # 获取name对应的集合中的元素个数
        # sdiff(keys, *args)  # 在第一个name对应的集合中且不在其他name对应的集合的元素集合
        # sdiffstore(dest, keys, *args) # 把sdiff获取的值加入到dest对应的集合中
        # sinter(keys, *args) # 获取多个name对应集合的交集
        # sismember(name, value) # 检查value是否是name对应的集合内的元素
        # smove(src, dst, value) # 将某个元素从一个集合中移动到另外一个集合
        # spop(name)  # 从集合的右侧移除一个元素，并将其返回
        # srandmember(name, numbers)  # 从name对应的集合中随机获取numbers个元素
        # srem(name, values) # 删除name对应的集合中的某些值
        # sunion(keys, *args) # 获取多个name对应的集合的并集
        # sunionstore(dest, keys, *args) # 获取多个name对应的集合的并集，并将结果保存到dest对应的集合中

        """
        有序集合：

　　      在集合的基础上，为每元素排序，元素的排序需要根据另外一个值来进行比较，
         所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。
        """
        # zadd(name, *args, **kwargs)
        # zcard(name) # 获取有序集合内元素的数量
        # zcount(name, min, max) # 获取有序集合中分数在[min,max]之间的个数
        # zincrby(name, value, amount)  # 自增有序集合内value对应的分数
        # zrange(name, start, end, desc=False, withscores=False, score_cast_func=float)
        '''参数：
            name    redis的name
            start   有序集合索引起始位置
            end     有序集合索引结束位置
            desc    排序规则，默认按照分数从小到大排序
            withscores  是否获取元素的分数，默认只获取元素的值
            score_cast_func 对分数进行数据转换的函数
        '''
        # zrevrange(name, start, end, withscores=False, score_cast_func=float) # 同zrange，集合是从大到小排序的
        # zrank(name, value)、zrevrank(name, value) # #获取value值在name对应的有序集合中的排行位置（从0开始）
        # zscore(name, value)  # 获取name对应有序集合中 value 对应的分数
        # zrem(name, values)   # 删除name对应的有序集合中值是values的成员
        # zremrangebyrank(name, min, max)       # 根据排行范围删除
        # zremrangebyscore(name, min, max)      # 根据分数范围删除

        # zinterstore(dest, keys, aggregate=None)
        #  获取两个有序集合的交集并放入dest集合，如果遇到相同值不同分数，则按照aggregate进行操作aggregate的值为: SUM  MIN  MAX
        # zunionstore(dest, keys, aggregate=None) # 获取两个有序集合的并集并放入dest集合，其他同zinterstore，


        r.zadd("zset_name",  6, "a1", 2,"a2", 5, "a3")
        r.zadd('zset_name1', b1=10, b2=5)
        print(r.zcard("zset_name"))
        print(r.zcard("zset_name1"))
        pass

    def testPipLine(self):
        r = self.conn
        with r.pipeline(transaction=False) as p:

            p.sadd('seta', 1).sadd('seta', 2).srem('seta', 2).lpush('lista', 1).lrange('lista', 0, -1)
            p.execute()
            p.watch('stock:count')
            p.unwatch()
        with r.pipeline() as pipe:
            pipe.multi()
            pipe.decr('name')
            # 把命令推送过去
            # execute返回命令执行结果列表, 这里只有一个decr返回当前值
            print pipe.execute()[0]
            return True


    def testOther(self):
        # delete(*names)       # 根据name删除redis中的任意数据类型
        # exists(name)
        # expire(name, time)     # 为某个name设置超时时间
        # rename(src, dst)
        # move(name, db))  # 将redis的某个值移动到指定的db下
        # randomkey()      # 随机获取一个redis的name（不删除）
        # type(name)       # 获取name对应值的类型
        pass

if __name__ == "__main__":
    rph = RedisPoolHolder(_config)
    rt = RedisTest(rph)
    # rt.testString()
    # rt.testHash()
    # rt.testList()
    # rt.testSet()
    rt.testPipLine()