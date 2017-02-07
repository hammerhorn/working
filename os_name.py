#!/usr/bin/env python3
"""
Displays sytem info.  Works with bash or Tk.
"""
__author__ = 'Chris Horn <hammerhorn@gmail.com>'

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

TERMINAL = Terminal()
CONFIG = Config()

SHELL = CONFIG.start_user_profile() if __name__ == '__main__' else TERMINAL

if SHELL.interface == 'Tk':
    SHELL.msg.config(bg='black', fg='chartreuse', font=('mono', 10), width=525)
    SHELL.main_window.config(bg='black')
    SHELL.main_window.title(TERMINAL.hostname)

def main():
    """
    Output system info; if using bash, use animated text.
    """
    string = SHELL.view_info(get_str=True)


    # dictionary comprehension?    
    if SHELL.interface == 'Tk':
        SHELL.output(string, width=525, height=200)
    elif SHELL.interface in ('dialog', 'zenity', 'SL4A'):
        SHELL.output(string)
    elif SHELL.interface == 'term':
        SHELL.tty(''.join((string, '\n')))

if __name__ == '__main__':
    main()
    SHELL.start_app()
