#!/usr/bin/env python
"""
Reads from and write to the config file, 'config.json'.
"""
import argparse
import copy
import time

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    + include brower
    - go game client
    - use dict.get()"""

def _parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shell', '-s', type=str, help='set shell')
    parser.add_argument('--editor', '-e', type=str, help='set editor')
    parser.add_argument('--terminal', '-t', type=str, help='set terminal')
    parser.add_argument('--language', '-l', type=str, help='set language')
    parser.add_argument('--browser', '-b', type=str, help='set browser')
    parser.add_argument('-v', action='count')
    args = parser.parse_args()
    return args

def lookup(key):
    """return the requested value"""
    return CONFIG.config_dict.get(key, None)

ARGS = _parse_args() if __name__ == '__main__' else None
CONFIG = Config()
FILENAME = 'versatiledialogs/config.json'

def edit_config_file():  # take off lookup's
    if ARGS.shell is not None: #and ARGS.shell not in ['?', lookup('shell')]:
        CONFIG.write_to_config_file(shell=ARGS.shell)
    if ARGS.editor is not None: #and ARGS.editor not in ['?', lookup('editor')]:
        CONFIG.write_to_config_file(editor=ARGS.editor)
    if ARGS.terminal is not None: #and ARGS.terminal not in ['?', lookup('terminal')]:
        CONFIG.write_to_config_file(terminal=ARGS.terminal)
    if ARGS.language is not None: #and ARGS.language not in ['?', lookup('language')]:
        CONFIG.write_to_config_file(language=ARGS.language.upper())
    if ARGS.browser is not None: #and ARGS.browser not in ['?', lookup('browser')]:
        CONFIG.write_to_config_file(browser=ARGS.browser)

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

        nochangeneeded = noeditcommand
        for key in args_dict.keys():
            if lookup(key) == args_dict[key]:
                nochangeneeded = True  # needs more efficiency

                #        print nochangeneeded
    if nochangeneeded is False:
        edit_config_file()

    keyname_list = ['shell', 'editor', 'terminal', 'language', 'browser']

    keylabel_list = [
        'versatiledialogs mode',
        'default text editor',
        'default terminal emulator',
        'language',
        'default web browser'
    ]

    for key_name, key_label in zip(keyname_list, keylabel_list):
        if (verbose > 0 and args_dict[key_name] is not None) or\
           nocommand is True or args_dict[key_name] == '?':
            string += generate_msg(key_name, key_label)

    if len(string) > 0:
        Terminal.output(string + '\n')

    if verbose >= 3 or (noeditcommand is True and verbose >= 1):
        Terminal.output('')
        easycat.view_source(FILENAME)

    delta_t = 0.3
    if verbose > 0 and nochangeneeded is False:
        Terminal.output('')
        Terminal.report_filesave(FILENAME, fast=True)
        time.sleep(delta_t)
        Terminal.clear(2)
        Terminal.report_filesave(FILENAME, fast=True)
        time.sleep(delta_t)
if __name__ == '__main__':
    main()
