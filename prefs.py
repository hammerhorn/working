#!/usr/bin/env python
"""
Reads from and write to the config file, 'config.json'.
"""
import argparse

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    + include brower
    - go game client"""

def _parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', type=str, help='set shell')
    parser.add_argument('-e', type=str, help='set editor')
    parser.add_argument('-t', type=str, help='set terminal')
    parser.add_argument('-l', type=str, help='set language')
    parser.add_argument('-b', type=str, help='set browser')

    parser.add_argument('-v', action='count')
#    parser.add_argument('-q', action='store_true')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    ARGS = _parse_args()
else:
    ARGS = None

CONFIG = Config()
FILENAME = 'versatiledialogs/config.json'


def lookup(key):
    """return the requested value"""
    if key in list(CONFIG.config_dict.keys()):
        return CONFIG.config_dict[key]
    else:
        return None

SHELL = lookup('shell')
EDITOR = lookup('editor')
TERMINAL = lookup('terminal')
LANGUAGE = lookup('language')
BROWSER = lookup('browser')


def main():
    """
    Writes requested modifications to the 'config.json' file, and sends
    some kind of feedback to stdout.
    """
    if ARGS.s is not None:
        CONFIG.write_to_config_file(shell=ARGS.s)
    if ARGS.e is not None:
        CONFIG.write_to_config_file(editor=ARGS.e)
    if ARGS.t is not None:
        CONFIG.write_to_config_file(terminal=ARGS.t)
    if ARGS.l is not None:
        CONFIG.write_to_config_file(language=ARGS.l.upper())
    if ARGS.b is not None:
        CONFIG.write_to_config_file(browser=ARGS.b)

    string = ''

    def generate_msg(what_arg, attr_name):
        """
        generate the output to be written to stdout at the appropriate level
        of verbosity
        """
        if ARGS.v == 2 and what_arg is not None:
            return_str = "\n{:>25s}: '{}'".format(attr_name, what_arg)
        elif not (ARGS.v or ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b):
            return_str = "\n{:>25s}: '{}'".format(attr_name, SHELL)
        else:
            return_str = None
        return return_str


    string += generate_msg(ARGS.s, 'versatiledialogs mode')
    string += generate_msg(ARGS.e, 'default text editor')
    string += generate_msg(ARGS.t, 'default terminal emulator')
    string += generate_msg(ARGS.l, 'language')
    string += generate_msg(ARGS.b, 'default web browser')

    if len(string) > 0:
        Terminal.output(string + '\n')

    if (ARGS.v is not None and ARGS.v >= 3) or\
       (not (ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b) and
        ARGS.v is not None and ARGS.v >= 1):
        Terminal.output('')
        easycat.view_source(FILENAME)
    if ARGS.v > 0 and (set('setlb') & set(ARGS.__dict__.keys())):
        print
        Terminal.report_filesave(FILENAME)
        Terminal.clear(2)
        Terminal.report_filesave(FILENAME, fast=True)

if __name__ == '__main__':
    main()
