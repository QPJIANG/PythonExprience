#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os

"""

cmd in PATH is available
alias is not available

"""

if __name__ == "__main__":
    proc = Popen("df", stdout=PIPE, stderr=PIPE, shell=True, env=None, close_fds=False)
    (stdout, stderr) = proc.communicate()
    print len(stdout.splitlines())
    stdout = stdout.strip()
    print len(stdout.splitlines())
    print stdout.splitlines()
    print "------------"
    # os.system("ls")

    pass
