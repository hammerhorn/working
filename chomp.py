#!/usr/bin/env python
#coding=utf8
"""
chompall
-
Replace each newline with a space.
"""
import sys

from easycat import write
from cjh.misc import chomp, notebook

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def main():
    """
    Read from stdin, convert newlines to spaces, strip the trailing
    space, and write to stdout.
    """
    notebook("""
    + Works fine.
    + Works with python 3""")
    write(chomp(sys.stdin.read()))

if __name__ == '__main__':
    main()
