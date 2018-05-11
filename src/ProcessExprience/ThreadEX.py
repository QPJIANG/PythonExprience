#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import thread # for python 2

import _thread
import threading
import time
import subprocess
from multiprocessing import Process, Queue, Pool
import os, time, random

"""
https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868323401155ceb3db1e2044f80b974b469eb06cb43000
在Unix/Linux下，multiprocessing模块封装了fork()调用，使我们不需要关注fork()的细节。
由于Windows没有fork调用，因此，multiprocessing需要“模拟”出fork的效果，
父进程所有Python对象都必须通过pickle序列化再传到子进程去，所有，如果multiprocessing在Windows下调用失败了，
要先考虑是不是pickle失败了。


在Unix/Linux下，可以使用fork()调用实现多进程。
要实现跨平台的多进程，可以使用multiprocessing模块。
进程间通信是通过Queue、Pipes等实现的。

"""


##################################################################
def timmer_test():
    def time_caller():
        print("called")
        proc = subprocess.Popen("sleep 1 && ls /", stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE, shell=True)
        print(proc.stdout.readlines())  # wait process exit and get stdout

    timer = threading.Timer(0, time_caller)
    timer.start()


##################################################################

def thraed_test1():
    def target():
        print('the current threading  %s is running' % threading.current_thread().name)
        time.sleep(1)
        print('the current threading  %s is ended' % threading.current_thread().name)

    def target2():
        print('the current threading  %s is running' % threading.current_thread().name)
        time.sleep(1)
        print('the current threading  %s is ended' % threading.current_thread().name)
        # thread.exit()
        _thread.exit()

    print('the current threading  %s is running' % threading.current_thread().name)
    # Thread(group=None, target=None, name=None,args=(), kwargs=None, verbose=None)
    t = threading.Thread(target=target)
    t.setDaemon(True)
    t.start()
    t.join()

    # noinspection PyBroadException
    try:
        # thread.start_new_thread(target2, ())
        _thread.start_new_thread(target2, ())
        time.sleep(3)
    except Exception:
        print("Error: unable to start thread")

    # t.join(1)   # main thread wait 1s ,t will be killed if it is not end
    print('the current threading  %s is ended' % threading.current_thread().name)


##################################################################
balance = 0


def thread_lock_test():
    lock = threading.Lock()

    def change_it(n):
        # 先存后取，结果应该为0:
        global balance
        balance = balance + n
        balance = balance - n

    def run_thread(n):
        for i in range(100000):
            # 先要获取锁:
            lock.acquire()
            try:
                # 放心地改吧:
                change_it(n)
            finally:
                # 改完了一定要释放锁:
                lock.release()

    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)


##################################################################


def process_test1():
    import os
    import platform

    if platform.system() == "Linux":
        print('Process (%s) start...' % os.getpid())
        # Unix/Linux操作系统提供了一个fork()系统调用,Windows上无法运行
        pid = os.fork()
        if pid == 0:
            print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
        else:
            print('I (%s) just created a child process (%s).' % (os.getpid(), pid))


##################################################################


def process_test2():
    # 跨平台的多进程支持:multiprocessing
    from multiprocessing import Process
    import os

    # 子进程要执行的代码

    def run_proc(name):
        print('Run child process %s (%s)...' % (name, os.getpid()))

    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Process will start.')
    p.start()
    p.join()
    print('Process end.')


##################################################################


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)

    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


def process_pool_test1():
    print('Parent process %s.' % os.getpid())
    # 由于Pool的默认大小是CPU的核数
    p = Pool()
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all sub processes done...')
    p.close()
    p.join()
    print('All sub processes done.')


##################################################################
# 写数据进程执行的代码:
def write(q):
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())


# 读数据进程执行的代码:
def read(q):
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)


def process_pool_test2():
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()


##################################################################
##################################################################
if __name__ == "__main__":
    # timmer_test()
    # thraed_test1()
    # thread_lock_test()
    # process_test1()
    # process_test2()
    # process_pool_test1()
    # process_pool_test2()
    thraed_test1()
    pass
