#!/usr/bin/env python3
#coding=utf8
import sys
from easycat import write

from versatiledialogs.terminal import Terminal

if {'-h', '--help'} & set(sys.argv):
    sys.exit(''.join(('print ', Terminal.fx('bn', 'bold'), ' text')))

write(Terminal.fx('bn', sys.stdin.read()))  # easycat.cat(return_str=True,
                                            # quiet=True)))

