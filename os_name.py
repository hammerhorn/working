#!/usr/bin/env python3
"""
Displays sytem info.  Works with bash, Tk, dialog, or zenity.
"""
__author__ = 'Chris Horn <hammerhorn@gmail.com>'

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

TERMINAL = Terminal()
CONFIG = Config()
SHELL = CONFIG.start_user_profile() if __name__ == '__main__' else TERMINAL

if SHELL == 'Tk':
    SHELL.msg.config(bg='black', fg='chartreuse', font=('mono', 10), width=525)
    SHELL.main_window.config(bg='black')
    SHELL.main_window.title(TERMINAL.hostname)

def main():
    """
    Output system info
    """
    string = SHELL.view_info(get_str=True)
    dimensions = {}

    if SHELL == 'term':
        #SHELL.tty(string + '\n')
        SHELL.output(string + '\n\n')
    else:
        if SHELL == 'Tk':
            dimensions.update({'width': 525, 'height': 200})
        SHELL.output(string, **dimensions)

if __name__ == '__main__':
    main()
    SHELL.start_app()
