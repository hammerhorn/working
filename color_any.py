#!/usr/bin/env python
#coding=utf8
"""
Define a color by ANSI code, RGB hex code, Kelvins (, wavelength, or frequency).
"""
import argparse

from cjh.misc import notebook
from colorful.color import Color

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-C', action='store_true', help="developer's comments")
    parser.add_argument('value')
    parser.add_argument(
        'type', type=str,
        help='ansi (0-255), hex (e.g., #000000), kelvin (> 0)')
    parser.add_argument('--shell', '-s', type=str,
                        help='bash/dialog/Tk/zenity, etc....')
    parser.add_argument(
        '-t', action='store_true',
        help='for more accurate colors (except ANSI-type), if your terminal' +\
        ' supports truecolor escape sequences.')
    if __name__ == '__main__':
        args = parser.parse_args()
    else:
        args = None
    return args


########################
#  INITIALIZE DIALOGS  #
########################
notebook('    - by freq and wavelength')
ARGS = _parse_args()
CONFIG = Config()
if ARGS is not None and ARGS.shell is not None:
    SHELL = CONFIG.launch_selected_shell(ARGS.shell)
else:
    SHELL = CONFIG.start_user_profile()


##########
#  MAIN  #
##########
def main():
    """
    Main function
    """
    if len(ARGS.value) == 1:
        ARGS.value = '0' + ARGS.value
    new_color = Color(ARGS.value, ARGS.type)
    SHELL.output(new_color)

    Terminal.output('Truecolor is {}.\n'.format(ARGS.t))

    new_color.draw_box(tc_on=ARGS.t)
    Terminal.output('\n')

if __name__ == '__main__':
    main()
    SHELL.start_app()
