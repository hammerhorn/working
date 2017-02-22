#!/usr/bin/env python3
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
    return parser.parse_args()

ARGS = _parse_args() if __name__ == '__main__' else None

# If ARGS.width is an int, it means: width in columns.                       #
#            If it's < 1,  it means: a percent of the width of the terminal. #

if None not in (ARGS, ARGS.width) and (ARGS.width == int(ARGS.width)):
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
