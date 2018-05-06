#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import subprocess
import time

"""
shell call test
"""


##################################################################

def env():
    _env = os.environ
    print (_env)
    print (_env["PYTHONPATH"])
    print ("----------------------")
    pass


##################################################################

def call_method1():
    # execl(file, *args)

    os.execl("/bin/ls", "")
    # the fallow lines are disabled to execute, because main process exit
    print ("----------------------")

    pass


##################################################################

def call_method2():
    # Popen
    s = os.popen("ls /").read()
    for line in s.split("\n"):
        print(line)

    lines = os.popen("ls").readlines()
    for line in lines:
        print(line.strip())  # line contain "\n"

    pass


##################################################################

def call_method3():
    # 需要注意的是commands模块不支持windows平台
    # *commands.getstatusoutput(cmd)     返回(status, output)
    # *commands.getoutput(cmd)     仅仅返回输出结果
    # *commands.getstatus(file)     返回ls - ld file的运行结果字符串，调用了getoutput。不建议使用此方法
    output = commands.getoutput("ls /")
    print (output)

    (status, output) = commands.getstatusoutput("ls")
    for line in output.split("\n"):
        print(line)

    pass


##################################################################
def call_method4():
    # call: args is a list
    returncode = subprocess.call(["ls", "-l"])
    print (returncode)
    print ("-----------------------------------------------------------------------")
    # subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None,
    #                                    preexec_fn=None, close_fds=False, shell=False, cwd=None,
    #                                   env=None, universal_newlines=False, startupinfo=None,
    #                                   creationflags=0)
    # https://blog.csdn.net/gmq_syy/article/details/76855621
    # https://www.cnblogs.com/yyds/p/7288916.html
    proc = subprocess.Popen("ls /", stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    while proc.poll() is None:  # check proc finish: runing:return None
        print ("waiting .......")
        time.sleep(0.005)


    print proc.returncode  # exit_code
    print proc.pid  # thread_pid
    print proc.wait()  # wait proc exit and return the exit_code
    print proc.returncode
    print proc.stderr.readlines()  # read proc stderr
    print proc.stdout.readlines()  # read proc stdout
    # print proc.stdin

    pass


##################################################################

if __name__ == "__main__":
    env()
    print ("#####################################################")

    # call_method1()
    # print ("#####################################################")

    call_method2()
    print ("#####################################################")
    call_method3()
    print ("#####################################################")
    call_method4()
    print ("#####################################################")
    pass
