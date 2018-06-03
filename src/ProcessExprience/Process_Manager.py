#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import os
import time
import signal
from multiprocessing import Process, Manager, Queue, Lock, Pipe,Pool


# test queue
# Queue本身是一个消息队列程序，可以利用它进行进程间通信
#
# Queue.size() 返回当前队列包含的消息数量（mac用不了）
# Queue.empty() 队列为空返回True，反之返回False
# Queue.full() 队列满了返回True，反之返回False
# Queue.get([block[,timeout]]) 获取队列中一条消息，然后将其从队列中移除，block默认为True
# block 默认为True，如果消息队列为空，且没有设置timeout，则程序被阻塞，直到消息队列读到消息为止
# block为False时，如果消息队列为空，立即抛出Queue.Empty异常
# timeout，超时时间，没有读到消息时会等待timeout秒，如果还没读到，就抛出Queue.Empty异常
# Queue.get_nowait() 相当于Queue.get(False)
# Queue.put(item[,block[,timeout]]) 将消息写入队列，block默认为True
# block默认为True，如果消息队列没有写入空间，且没有设置timeout，则程序被阻塞，直到消息队列能写入为止
# block为False时，如果消息队列没有写入空间，立即抛出Queue.Full异常
# timeout，超时时间，没有写入空间时时会等待timeout秒，如果还没有写入空间，就抛出Queue.Full异常
# Queue.put_nowait() 相当于Queue.put(item, False)
#

def add(q, lock, a, b):
    lock.acquire()  # 加锁避免写入时出现不可预知的错误
    L1 = [a, b]
    lock.release()
    q.put(L1)
    print(L1)


def test_queue():
    q = Queue()
    q.put({"x": 23})
    lock = Lock()
    p1 = Process(target=add, args=(q, lock, 20, 30))
    p2 = Process(target=add, args=(q, lock, 30, 40))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(q.get())
    print(q.get())
    print(q.get())


# pip test

def proc1(pipe):
    s = 'Hello,This is proc1'
    pipe.send(s)


def proc2(pipe):
    while True:
        print("proc2 recieve:", pipe.recv())


def test_pipe():
    pipe = Pipe()
    p1 = Process(target=proc1, args=(pipe[0],))
    p2 = Process(target=proc2, args=(pipe[1],))
    # p2.daemon = True
    p1.start()
    p2.start()
    # 等待子进程结束，永不超时
    p1.join()

    # 等待子进程结束，超时后继续执行，p2如果未设置 “p2.daemon = True”， 主进程执行至结尾时，等待子进程结束
    p2.join(2)
    print('\nend all processes.')
    print(p1.is_alive())
    print(p2.is_alive())
    pipe[0].send("end")
    if p2.is_alive():
        try:
            pid = p2.pid
            a = os.kill(pid, signal.SIGKILL)
            # a = os.kill(pid, signal.9) #　与上等效
            print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))
        except OSError as e:
            print('没有如此进程!!!')


# manager test
# Manage专门用来做数据共享

def func(dt, lt):
    for i in range(10):
        key = 'arg' + str(i)
        dt[key] = i * i

    lt += range(11, 16)


def test_manager():
    manager = Manager()
    dt = manager.dict()
    lt = manager.list()

    p = Process(target=func, args=(dt, lt))
    p.start()
    p.join()
    print(dt, '\n', lt)

# process class

class MyNewProcess(Process):
    def run(self):
        while True:
            print("---1---")
            time.sleep(1)
def test_class():
    p = MyNewProcess()
    p.daemon=True
    p.start()
    time.sleep(2)

# test pool

# multiprocessing.Pool常用方法：
#
# apply_async(func[,args[,kwds]])：使用非阻塞方式调用func
# apply(func[,args[,kwds]])：使用阻塞方式调用func
# terminate()：不管任务是否完成，立即终止
# join()：主进程阻塞，等待子进程的退出，必须在close或terminate之后使用（pool.close(),pool.terminate()）



def run(fn):
    # fn: 函数参数是数据列表的一个元素
    time.sleep(1)
    return fn * fn

def testmap():
    testFL = [1, 2, 3, 4, 5, 6]

    pool = Pool(5)  # 创建拥有5个进程数量的进程池
    # testFL:要处理的数据列表，run：处理testFL列表中数据的函数
    rl = pool.map(run, testFL)
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出

    print(rl)

if __name__ == "__main__":
    # test_queue()
    # test_pipe()
    # test_manager()
    # test_class()
    testmap()

    # fork 全局变量在多个进程中不共享,fork 主进程不等待子进程结束
    ret = os.fork()     # 父进程得到子进程pid, 子进程得到0
    if ret > 0:
        print("---父进程---%d" % os.getpid())
    else:
        # ret==0
        print("---子进程---%d---%d" % (os.getpid(), os.getppid()))
        time.sleep(10)  # 子进程10 s 后结束

    print(ret)
    exit(0)