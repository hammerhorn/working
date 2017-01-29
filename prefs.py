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

#    config_dict = {'shell':shell}
#    with open(filename, 'w') as outfile: json.dump(
#        config_dict, outfile, indent=2)

    string = ''

    if ARGS.v == 2 and ARGS.s is not None:
        string += "\n    versatiledialogs mode: '{}'".format(ARGS.s)
    elif not (ARGS.v or ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b):
        string += "\n    versatiledialogs mode: '{}'".format(SHELL)

    if ARGS.v == 2 and ARGS.e is not None:
        string += "\n      default text editor: '{}'".format(ARGS.e)
    elif not (ARGS.v or ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b):
        string += "\n      default text editor: '{}'".format(EDITOR)

    if ARGS.v == 2 and ARGS.t is not None:
        string += "\ndefault terminal emulator: '{}'".format(ARGS.t)
    elif not (ARGS.v or ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b):
        string += "\ndefault terminal emulator: '{}'".format(TERMINAL)

    if ARGS.v == 2 and ARGS.l is not None:
        string += "\n                 language: '{}'".format(ARGS.l)
    elif not (ARGS.v or ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b):
        string += "\n                 language: '{}'".format(LANGUAGE)


    if ARGS.v == 2 and ARGS.b is not None:
        string += "\n      default web browser: '{}'".format(ARGS.b)
    elif not (ARGS.v or ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b):
        string += "\n      default web browser: '{}'".format(BROWSER)

    if len(string) > 0:
        Terminal.output(string + '\n')

    if (ARGS.v is not None and ARGS.v >= 3) or\
       (not (ARGS.e or ARGS.s or ARGS.t or ARGS.l or ARGS.b) and
        ARGS.v is not None and ARGS.v >= 1):
        Terminal.output('')
        easycat.view_source(FILENAME)
    if ARGS.v is not None and ARGS.v >= 1 and (
            ARGS.s or ARGS.e or ARGS.t or ARGS.l or ARGS.b):
        Terminal.report_filesave(FILENAME)

if __name__ == '__main__':
    main()
