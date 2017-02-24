#!/usr/bin/env python3
#coding=utf8
"""
chomp - 

Replace each newline with a space.
"""
import sys

from easycat import write
from cjh.misc import chomp

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def main():
    """
    Read from stdin, convert newlines to spaces, strip the trailing
    space, and write to stdout.
    """
    write(chomp(sys.stdin.read()))

if __name__ == '__main__':
    main()

