#!/usr/bin/env python3
"""
Allow the user to preview the available fonts for toilet (or figlet).

Python 2 only for now.
"""
import argparse
import atexit
import os
# import subprocess
import sys

from cjh.misc import notebook
from ttyfun.unix import Figlet
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal
from versatiledialogs.lists import PlainList

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


 ################
 #  PROCEDURES  #
 ################
def set_text():
    """
    Must be called before _parse_args() or it will not work
    """
    if len(sys.argv[1:]) == 0:
        phrase = 'Hello'
    else:
        phrase = sys.argv[1]
        del sys.argv[1]
    return phrase


def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--nox', action='store_true')
    parser.add_argument('-C', action='store_true')

    if __name__ == '__main__':
        args = parser.parse_args()
    else:
        args = None
    return args


 #################
 #   CONSTANTS   #
 #################
PHRASE = set_text()

# Prepare environment
ARGS = _parse_args()
notebook('    - Combine with cowscript.py')
CONFIG = Config()
if ARGS is not None and ARGS.nox is True:
    sys.argv = [i for i in sys.argv if not i.startswith('-')]
    SHELL = Terminal()
else:
    Terminal()
    SHELL = CONFIG.start_user_profile()
    if SHELL.interface in ('Tk', 'wx'):
        SHELL.center_window()
atexit.register(Terminal.unhide_cursor)
        
FONT_OPTIONS = os.listdir('/usr/share/figlet')
FONT_OPTIONS = [line for line in FONT_OPTIONS if not line.endswith('.flc')]
FONT_OPTIONS.sort()
LIST_OBJ = PlainList(FONT_OPTIONS)


 ##########
 #  MAIN  #
 ##########
def main():
    """
    Gets the user's choice and gives them a preview.
    """
    _first_pass = True
    art = ''
    Terminal.hide_cursor()
    while True:
#        try:
            if SHELL.interface == 'dialog' and not _first_pass:
                Terminal.wait()
            else:
                _first_pass = False

            selection = Terminal.make_page(
                obj='\n'+art, func=lambda: SHELL.list_menu(LIST_OBJ))
            if selection == -1:
                break
            figlet_font = FONT_OPTIONS[selection - 1]
            fig_writer = Figlet(figlet_font, 'gay')
            art = fig_writer.output(PHRASE, get_str=True)

#        except (AttributeError, KeyboardInterrupt, TypeError):
#            sys.exit('\nBye.')

if __name__ == '__main__':
    main()
