#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys, getopt


def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["in=", "out=","help"])
        print("--------------------------")
        print(opts)
        print(args)
        print("--------------------------")

    except getopt.GetoptError:
        print('args error')
        sys.exit(2)

    for opt, arg in opts:
        pass


if __name__ == "__main__":
    main(["help"])
    main(["-h"])
    # *.py -i input --out=output
    main(["-i", "input", "--out", "output"])
