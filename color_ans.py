#!/usr/bin/env python
#coding=utf8
"""
Display the standard ANSI colors which are available for the terminal.
If no arg, cycle through colors sequentially.

usage: color_ans.py [-h] [ANSI_CODE]
"""
import sys

from cjh.misc import catch_help_flag, notebook

from colorful.color import cycle_thru_ansiboxes, Color
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

DELTA_T = 0.1
REMARKS = """
    + make sure square hangs at the end
    - enable backwards ranges"""
notebook(REMARKS)
SHELL = Config().start_user_profile()


def get_flags():
    """
    -h  -->  print help and exit
    -t  -->  use Truecolor color method (rgb ascii escapes)
    """
    catch_help_flag(__doc__, SHELL)
    arg_dict = {}
    if '-t' in sys.argv[1:]:
        arg_dict.update({'-t': True})
        del sys.argv[sys.argv.index('-t')]
    else:
        arg_dict.update({'-t': False})
    return arg_dict


def main():
    """
    Main function
    """
    startcolor = 0
    endcolor = 255
    truecolor = get_flags()['-t']
    Terminal()
    SHELL.welcome(description=__doc__)

    Terminal.hide_cursor()
    Terminal.output('')
    if len(sys.argv[1:]) == 1:
        color1 = Color(int(sys.argv[1]), 'ansi')
        color1.draw_box(tc_on=truecolor)
    else:
        if len(sys.argv[1:]) == 2:
            startcolor = int(sys.argv[1])
            endcolor = int(sys.argv[2])
        cycle_thru_ansiboxes(startcolor, endcolor, DELTA_T, tc=truecolor)
    Terminal.output('')


if __name__ == '__main__':
    try:
        main()
    finally:
        Terminal.unhide_cursor()
        SHELL.start_app()
