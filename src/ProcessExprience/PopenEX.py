#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os

"""

cmd in PATH is available
alias is not available

"""


if __name__ == "__main__":

    proc = Popen("which ll", stdout=PIPE, stderr=PIPE, shell=True, env=None, close_fds=False)
    (stdout, stderr) = proc.communicate()
    print stdout
    os.system("ls")

    pass
