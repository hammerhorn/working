#!/usr/bin/env python3
#coding=utf8
"""
Draw Tonerow

Generate an ASCII diagram of a sequence of consecutive numbers 0 through (n - 1).

Example
    ./tonerow -n 11 | ./draw_row.py -p

'tonerow' generated a sequence of shuffled 0 thru 10, and draw_row.py draws the
picture.
"""
import argparse

from cjh.misc import notebook
from cjh.tonerow import Tonerow

from versatiledialogs.terminal import Terminal
from versatiledialogs.config import Config

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - The Tk version should be adjusted to look better.
    - It might be good to define more functions.
    - sh_obj should be an attribute of Thing"""

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments: -h (help), -s (bash, Tk, etc.)
    """
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-p', action='store_true', help='if using in a pipeline')
    parser.add_argument('-s', '--shell', type=str)
    parser.add_argument(
        '-C', action='store_true', help="see developer's comments")
    return parser.parse_args()


###############
#  CONSTANTS  #
###############
if __name__ == '__main__':
    ARGS = _parse_args()

    CONFIG = Config()
    if ARGS is not None and ARGS.shell is not None:
        SHELL = CONFIG.launch_selected_shell(ARGS.shell)
    else:
        SHELL = CONFIG.start_user_profile()

    notebook(REMARKS)

    ## Set up Tk window ##
    if SHELL.interface in ['Tk']:
        #SHELL.msg.config(font=('mono', 9, 'bold'))
        SHELL.center_window(width_=400, height_=300)

#    elif SHELL.interface in ['dialog']:
#        w, h = 46, 24
else:
    ARGS = None


##########
#  MAIN  #
##########
def main():
    """
    Takes  a space-delimited int list (e.g., '0 1 2 3 4 5 6 7 8 9 10 11') as
    input; generates and ouputs an ASCII diagram.
    """
    Terminal()
    SHELL.welcome(
        'Draw Tonerow', 'draw a diagram of an n-tone row.  Default is 12.')
    in_str = Terminal.input(prompt='', hide_form=True) if ARGS.p is True else\
             SHELL.input()
    Terminal.clear(0)
    str_list = in_str.split()
    ints = [int(s) for s in str_list]
    row = Tonerow(int_list=ints, sh_obj=SHELL)
    row.draw()

if __name__ == '__main__':
    main()
    SHELL.start_app()
