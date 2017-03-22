#!/usr/bin/env python3
#coding=utf8
"""
Display file with syntax highlighting.
"""
import argparse

import easycat
from cjh import misc
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str, nargs='?')
    parser.add_argument('-C', action='store_true')
    misc.catch_help_flag(help_str='', argprsr=parser)
    return parser.parse_args() if __name__ == '__main__' else None

###############
#  CONSTANTS  #
###############
ARGS = _parse_args()
misc.notebook('    + detect whether or not pager is needed')
Terminal()

##########
#  MAIN  #
##########
def main():
    """
    Main function
    """
    src_str = easycat.get_src_str(ARGS.filename)
    linecount = len(src_str.split('\n'))
    if linecount > Terminal.height():
        easycat.less(src_str)
    else:
        Terminal.clear()
        Terminal.output(src_str)

if __name__ == '__main__':
    main()
