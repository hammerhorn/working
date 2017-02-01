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
    ./prefs.py -b \?   (Echos back the selected web browser)
"""
import argparse
import copy
import sys
import time

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal
from cjh.misc import catch_help_flag

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    + include brower
    - go game client
    - use dict.get()"""

#if {'-h', '--help'} & set(sys.argv[1:]):
#    catch_help_flag(__doc__)

def _parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='Edit or view settings for versatiledialogs package.  ' +
            "Writes to 'config.json'.")
    parser.add_argument('--shell', '-s', type=str, help='set shell')
    parser.add_argument('--editor', '-e', type=str, help='set editor')
    parser.add_argument('--terminal', '-t', type=str, help='set terminal')
    parser.add_argument('--language', '-l', type=str, help='set language')
    parser.add_argument('--browser', '-b', type=str, help='set browser')
    parser.add_argument('-v', action='count')
    args = parser.parse_args()
    return args

ARGS = _parse_args() if __name__ == '__main__' else None
CONFIG = Config()
FILENAME = 'versatiledialogs/config.json'
KEYNAME_LIST = ['shell', 'editor', 'terminal', 'language', 'browser']

def lookup(key):
    """return the requested value"""
    return CONFIG.config_dict.get(key, None)

def edit_config_file():                     
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
            'term',
            'Tk',
            'wx',
            'zenity'
        ]
                
        # This bit is a little hacky
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

    if verbose >= 3 or (noeditcommand is True and verbose >= 1):
        Terminal.output('')
        easycat.view_source(FILENAME)

    delta_t = 0.3
    if verbose > 0 and nochangeneeded is False:
        Terminal.output('')
        report_str = Terminal.report_filesave(FILENAME, get_str=True)

        def print_and_wait():
            Terminal.output(report_str)
            time.sleep(delta_t)

        print_and_wait()
        Terminal.clear(2)
        print_and_wait()

if __name__ == '__main__':
    main()
