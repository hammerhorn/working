#!/usr/bin/env python3
#coding=utf8
import sys
import easycat

from versatiledialogs.terminal import Terminal

if {'-h', '--help'} & set(sys.argv):
    sys.exit(''.join(('print ', Terminal.fx('bn', 'bold'), ' text')))
easycat.write(Terminal.fx('bn',easycat.cat(return_str=True, quiet=True)))
