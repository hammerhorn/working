#!/usr/bin/env python
"""
Versatile Dialogs Preferences

This is the main script for editing settings in the versatiledialogs
environment.  Reads from and write to the config file, 'config.json'.

Config Attributes:
       shell - 'term', 'dialog', 'zenity', 'SL4A', 'Tk', 'wx', or 'html'
    terminal - name of terminal emulator, e.g., 'terminator -x '
      editor - default text editor, e.g., emacs, vi, gedit, ...
    language - 'EN' and 'EO' will be supported
     browser - default web browser

Examples:
    ./prefs.py         (Lists all keys and their values)
    ./prefs.py -s term (Sets the default shell to 'term')
    ./prefs.py -l en   (Sets the default language to English)
    ./prefs.py -b \\?   (Echos back the name of the default web browser)
"""
import argparse
import copy
import sys
import time

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal
from cjh.misc import notebook  # catch_help_flag

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - go game client
    + include brower
    + use dict.get()"""


def _parse_args():
    """
    Parse command-line arguments
    """
    notebook(REMARKS)
#    if '-C' in sys.argv[1:]:
#        del sys.argv[sys.argv.index('-C')]

    helpflag = True if {'-h', '--help'} & set(sys.argv[1:]) else False
    if helpflag is True:
        Terminal.output('')
    try:
        parser = argparse.ArgumentParser(
            description="Edit or view settings for 'versatiledialogs' package." +
            "  Writes to 'config.json'.  Type 'pydoc prefs' for more info.")
        parser.add_argument('--shell', '-s', type=str, help='set shell')
        parser.add_argument('--editor', '-e', type=str, help='set editor')
        parser.add_argument('--terminal', '-t', type=str, help='set terminal')
        parser.add_argument('--language', '-l', type=str, help='set language')
        parser.add_argument('--browser', '-b', type=str, help='set browser')
        parser.add_argument(
            '-v', action='count', help="verbose; the more v's, the more vebose")
        args = parser.parse_args()
    finally:
        if helpflag:
            Terminal.output('')
    return args


ARGS = _parse_args() if __name__ == '__main__' else None
CONFIG = Config()
FILENAME = 'versatiledialogs/config.json'
KEYNAME_LIST = ['shell', 'editor', 'terminal', 'language', 'browser']

def lookup(key):
    """return the requested value"""
    return CONFIG.config_dict.get(key, None)

def edit_config_file():
    """
    Write the changes to the actual file 'config.json'.
    """
    for key_name in KEYNAME_LIST:
        if ARGS.__dict__[key_name] is not None and\
           ARGS.shell not in ['?', lookup(key_name)]:  # redundent, but safer
            CONFIG.config_dict[key_name] = ARGS.__dict__[key_name]
    CONFIG.write_to_config_file(**CONFIG.config_dict)


def main():
    """
    Writes requested modifications to the 'config.json' file, and sends
    some kind of feedback to stdout.
    """
    string = ''

    def generate_msg(key_name, key_label):
        """
        generate the output to be written to stdout at the appropriate level
        of verbosity
        """
        value = lookup(key_name)
        return "\n{:>25s} = '{}'".format(key_label, value)

    if ARGS is not None:
        args_dict = copy.deepcopy(ARGS.__dict__)
        verbose = 0 if args_dict['v'] is None else args_dict['v']
        del args_dict['v']

        nocommand = True if args_dict.values() == [None, None, None, None, None] else False
        noeditcommand = True
        for value in args_dict.values():
            if value is not None and value != '?':
                noeditcommand = False

        supported_modes = [
            'dialog',
            'html',
            'SL4A',
            'term',
            'Tk',
            'wx',
            'zenity'
        ]

        if args_dict['shell'] not in (supported_modes + ['?', None]):
            args_dict['shell'] = CONFIG.config_dict['shell']
            Terminal.output('\nsupported modes: ' + str(supported_modes)[1:-1] + '\n')

        nochangeneeded = noeditcommand
        for key in args_dict.keys():
            if lookup(key) == args_dict[key]:
                nochangeneeded = True

    if nochangeneeded is False:
        edit_config_file()

    keylabel_list = [
        'mode',
        'default text editor',
        'default terminal emulator',
        'language',
        'default web browser'
    ]

    for key_name, key_label in zip(KEYNAME_LIST, keylabel_list):
        if (verbose > 0 and args_dict[key_name] is not None) or\
           nocommand is True or args_dict[key_name] == '?':
            string += generate_msg(key_name, key_label)


    if len(string) > 0:
        Terminal.output(string + '\n')

    if verbose >= 2 or (noeditcommand is True and verbose >= 1):
        Terminal.output('')
        easycat.view_source(FILENAME)

    if verbose > 0 and nochangeneeded is False:
        Terminal.output('')
        Terminal.clear(1)
        Terminal.report_filesave(FILENAME, fast=True)
        Terminal.output('')

if __name__ == '__main__':
    main()
