#!/usr/bin/env python3
#coding=utf8
"""
You can use this in pipelines in bash scripts to make text bold.
"""
import sys
from easycat import write

from versatiledialogs.terminal import Terminal

if __name__ == '__main__':
    if {'-h', '--help'} & set(sys.argv):
        sys.exit('\nprint bold text\n' + __doc__)

    write(Terminal.fx('bn', sys.stdin.read()))  # easycat.cat(return_str=True,
                                                # quiet=True)))

