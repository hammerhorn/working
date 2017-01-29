#!/usr/bin/env python
"""
Produces horizontal lines for use in shell scripts.

usage: hr.py [-h] [-w WIDTH] [-p PATTERN] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -w WIDTH, --width WIDTH
  -p PATTERN, --pattern PATTERN
  -c, --center

* floats should give screenwidths, ints shoudl give charwidths
"""
import argparse

from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

Terminal()
#arg_dic = {}

def _parse_args():
    """
    Parse all args and return 'args' namespace.
    """
    parser = argparse.ArgumentParser(
        description='Produces horizontal lines for use in shell scripts.')
    parser.add_argument(
        '-w', '--width', type=float, help='width in columns or width in ' +
        'screenwidths')
    parser.add_argument(
        '-p', '--pattern', type=str, help='symbol or sequence of symbols')
    parser.add_argument(
        '-c', '--center',
        action='store_true',
        help='centered (default is left-aligned)')
    #parser.add_argument("-s", "--string", action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    ARGS = _parse_args()
else: ARGS = None

# If ARGS.width is an integer, convert it to be of type int.
# An int for this value means width in columns.
# A decimal < 1 means a percentage of the width of the terminal.
if ARGS is not None and ARGS.width is not None and\
    (ARGS.width == int(ARGS.width)):
    ARGS.width = int(ARGS.width)

# possible to this automatically?
def populate_args():
    """
    Convert args namespace to a dictionary, for use in the Cli.hrule()
    method.
    """
    kw_dict = {}
    if ARGS is not None:
        if ARGS.width is not None:
            kw_dict.update({'width': ARGS.width})
        if ARGS.pattern is not None:
            kw_dict.update({'symbols': ARGS.pattern})
        if ARGS.center is True:
            kw_dict.update({'centered': ARGS.center})
    return kw_dict

# print arg_dic
ARG_DICT = populate_args()

if __name__ == '__main__':
    Terminal.hrule(**ARG_DICT)
    Terminal.output('')
