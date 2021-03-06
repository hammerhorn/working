#!/usr/bin/env python3
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

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal
from cjh.misc import notebook, catch_help_flag
from ranges import iter_zip

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - go game client
    + include browser
    + use dict.get()"""

def _parse_args():
    """
    Parse command-line arguments
    """
    notebook(REMARKS)
    parser = argparse.ArgumentParser()
    parser.add_argument('--shell', '-s', type=str, help='set shell')
    parser.add_argument('--editor', '-e', type=str, help='set editor')
    parser.add_argument('--terminal', '-t', type=str, help='set terminal')
    parser.add_argument('--language', '-l', type=str, help='set language')
    parser.add_argument('--browser', '-b', type=str, help='set browser')
    parser.add_argument(
        '-v', action='count', help="verbose; the more v's, the more verbose")
    description = """Edit or view settings for 'versatiledialogs' package.  Writes to
'config.json'.  Type 'pydoc prefs' for more info.\n"""
    catch_help_flag(help_str=description, argprsr=copy.copy(parser))
    return parser.parse_args()


ARGS = _parse_args() if __name__ == '__main__' else None
CONFIG = Config()
FILENAME = 'versatiledialogs/config.json'
KEYNAME_LIST = ('shell', 'editor', 'terminal', 'language', 'browser')


def edit_config_file():
    """
    Write the changes to the actual file 'config.json'.
    """
    if ARGS.language is not None:
        ARGS.language = ARGS.language.upper()
    for key_name in KEYNAME_LIST:
        if ARGS.__dict__[key_name] is not None and\
           ARGS.shell not in ('?', CONFIG.config_dict.get(key_name, None)):  # redundent, but safer
            CONFIG.config_dict[key_name] = ARGS.__dict__[key_name]
    CONFIG.write_to_config_file(**CONFIG.config_dict)


def main():
    """
    Writes requested modifications to the 'config.json' file, and sends
    some kind of feedback to stdout.
    """
    def generate_msg(key_name, key_label):
        """
        generate the output to be written to stdout at the appropriate level
        of verbosity
        """
        value = CONFIG.config_dict.get(key_name, None)
        return "\n{:>25s} = '{}'".format(key_label, value)

    if ARGS is not None:
        args_dict = copy.copy(ARGS.__dict__)
        verbose = 0 if args_dict['v'] is None else args_dict['v']
        del args_dict['v']

        nocommand = tuple(args_dict.values()) == (None, ) * 5
        noeditcommand = True
        for value in args_dict.values():
            if value is not None and value != '?':
                noeditcommand = False
                break

        supported_modes = (
            'dialog',
            'html',
            'SL4A',
            'term',
            'Tk',
            'wx',
            'zenity'
        )

        if args_dict['shell'] not in (supported_modes + ('?', None)):
            args_dict['shell'] = CONFIG.config_dict['shell']
            Terminal.output(
                '\nsupported modes: {}\n'.format(str(supported_modes)[1:-1]))

        nochangeneeded = noeditcommand
        for key in args_dict.keys():
            if CONFIG.config_dict.get(key, None) == args_dict[key]:
                nochangeneeded = True

    if nochangeneeded is False:
        edit_config_file()

    keylabel_list = (
        'mode',
        'default text editor',
        'default terminal emulator',
        'language',
        'default web browser'
    )

    msg_list = []
    for key_name, key_label in iter_zip(KEYNAME_LIST, keylabel_list):
        if (verbose > 0 and args_dict[key_name] is not None) or\
            nocommand is True or args_dict[key_name] == '?':
            msg_list.append(generate_msg(key_name, key_label))
    outstring = ''.join(msg_list)

    if len(outstring) > 0:
        Terminal.output(outstring + '\n')

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
