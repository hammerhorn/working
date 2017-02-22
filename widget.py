#!/usr/bin/env python3
"""
various dialogs, which can use various shells/toolkits.

dialogs: welcome, output, outputf, input, wait, message, list
 shells: term, dialog, zenity, Tk, wx, html

usage: widget.py (--SHELL shell) [--WIDGET widget] [TEXT]
"""
import argparse
import copy
import string

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
    return parser.parse_args() if __name__ == '__main__' else None


##########
#  DATA  #
##########
ARGS = _parse_args()
CONFIG = Config()
SHELL = CONFIG.launch_selected_shell(ARGS.shell) if ARGS is not None and\
        ARGS.shell is not None else CONFIG.start_user_profile()

def get_input():
    input_dict = {'input': SHELL.input(ARGS.input)}
    fstring = string.Template("You said '$input'.")
    if SHELL.interface in ('dialog', 'zenity'):
        fstring = string.replace("'", "\'")
    SHELL.message(fstring.substitute(input_dict))

def make_list():
    if SHELL == 'term':
        SHELL.clear()

    list_ = PlainList(ARGS.list.split())
    answer = list_[SHELL.list_menu(list_) - 1]
    fstring = string.Template("You chose '$choice'.")
    select_dict = {'choice': answer}
    if SHELL.interface in ('dialog', 'zenity'):
        fstring = string.replace("'", "\'")
    SHELL.output(fstring.substitute(select_dict))

def output():
    if SHELL == 'Tk':
        SHELL.center_window(height_=100, width_=200)
        SHELL.msg.config(width=200)
    SHELL.output(ARGS.output)

def main():
    """
    Display welcome message on first run, then display requested combination of
    dialog box and shell.
    """
    args_dict = copy.copy(ARGS.__dict__)
    del args_dict['shell']

    # comprehension?
    widget_dict = {
        'input'  : get_input,
        'list'   : make_list,
        'message': lambda: SHELL.message(ARGS.message),
        'notify' : lambda: SHELL.notify(ARGS.notify),
        'output' : output,
        'outputf': lambda: SHELL.outputf(msg=ARGS.outputf + ' '),
        'wait'   : lambda: SHELL.wait(ARGS.wait),
        'welcome': lambda: SHELL.welcome(description=ARGS.welcome)
    }

    for key in args_dict:
        if args_dict[key] is not None:
            widget_dict.get(key, lambda: 0)()

    bye()

if __name__ == '__main__':
    main()
    SHELL.start_app()
