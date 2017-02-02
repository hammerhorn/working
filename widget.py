#!/usr/bin/env python3
"""
various dialogs, which can use various shells/toolkits.

dialogs: welcome, output, outputf, input, wait, message, list
 shells: term, dialog, zenity, Tk, wx, html

usage: widget.py (--SHELL shell) [--WIDGET widget] [TEXT]
"""
import argparse
# import atexit
# import sys

from cjh.misc import bye
from versatiledialogs.config import Config
from versatiledialogs.lists import PlainList


__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse command-line arguments; --help for details
    """
    parser = argparse.ArgumentParser(
        description='Test various dialogs from the command line.')
    parser.add_argument('--shell', '-s', type=str)
    parser.add_argument('--welcome', type=str, help='Welcome Dialog')
    parser.add_argument('--output', type=str, help='Output Dialog')
    parser.add_argument('--outputf', type=str, help='Outputf Dialog')
    parser.add_argument('--input', type=str, help='Input Dialog')
    parser.add_argument('--wait', type=str, help='Continue Dialog')
    parser.add_argument(
        '--notify', type=str, help='Notification Widget')
    parser.add_argument('--message', type=str, help='Message Dialog')
    parser.add_argument('--list', type=str, help='List Dialog')
    args = parser.parse_args() if __name__ == '__main__' else None
    return args


##########
#  DATA  #
##########
ARGS = _parse_args()
CONFIG = Config()
SHELL = CONFIG.launch_selected_shell(ARGS.shell) if ARGS is not None and\
        ARGS.shell is not None else CONFIG.start_user_profile()

def main():
    """
    Display welcome message on first run, then display requested combination of
    dialog box and shell.
    """
    if ARGS.welcome is not None:
        SHELL.welcome(description=ARGS.welcome)

    elif ARGS.message is not None:
        SHELL.message(ARGS.message)

    elif ARGS.output is not None:
        if SHELL.interface == 'Tk':
            SHELL.center_window(height_=100, width_=200)
            SHELL.msg.config(width=200)
        SHELL.output(ARGS.output)

    elif ARGS.input is not None:
        answer = SHELL.input(ARGS.input)
        string = "You said '{}'."
        if SHELL.interface in ['zenity']:
            string = string.replace("'", "\'")

        SHELL.output(string.format(answer))
        if SHELL.interface == 'term':
            SHELL.wait()

    elif ARGS.wait is not None:
        SHELL.wait(ARGS.wait)

    elif ARGS.outputf is not None:
        SHELL.outputf(msg=ARGS.outputf + ' ')

    elif ARGS.notify is not None:
        SHELL.notify(ARGS.notify)

    elif ARGS.list:
        if SHELL.interface == 'term':
            SHELL.clear()

        string = "You chose '{}'."
        if SHELL.interface in ['zenity', 'dialog']:
            string = string.replace("'", "\'")
        list_ = PlainList(ARGS.list.split())
        answer = list_[SHELL.list_menu(list_) - 1]
        SHELL.output(string.format(answer))
    bye()

if __name__ == '__main__':
    main()
    SHELL.start_app()
