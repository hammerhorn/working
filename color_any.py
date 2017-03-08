#!/usr/bin/env python3
#coding=utf8
"""
Define a color by ANSI code, RGB hex code, Kelvins (, wavelength, or frequency).
"""
import argparse
import sys

from cjh.misc import notebook
from colorful.color import Color, cycle_thru_ansiboxes
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
    return parser.parse_args() if __name__ == '__main__' else None


########################
#  INITIALIZE DIALOGS  #
########################
notebook('    - by freq and wavelength')

TRUECOLOR = '-t' in sys.argv[1:]
if len(sys.argv[1:]) == 0 or\
   (len(sys.argv[1:]) == 1 and TRUECOLOR is True):
    Terminal.hide_cursor()
    try:
        Terminal.output('')
        cycle_thru_ansiboxes(delta_t=0.1, tc=TRUECOLOR)
    finally:
        Terminal.output('')
        Terminal.unhide_cursor()
        Terminal.start_app()
        sys.exit()

ARGS = _parse_args()
CONFIG = Config()
SHELL = CONFIG.launch_selected_shell(ARGS.shell) if\
        ARGS is not None and ARGS.shell is not None else\
        CONFIG.start_user_profile()

##########
#  MAIN  #
##########
def main():
    """
    Main function
    """
    #if not {'value', 'type'} & set(ARGS.__dict__.keys()):
    #    cycle_thru_ansiboxes()
    #    return

    if len(ARGS.value) == 1:
        ARGS.value = '0' + ARGS.value
    if ARGS.type != 'hex':
        ARGS.value = int(ARGS.value) if ARGS.type != 'kelvin' else float(ARGS.value)
    new_color = Color(ARGS.value, ARGS.type)
    SHELL.output(new_color)
    Terminal.output('Truecolor is {}.\n'.format(ARGS.t))
    new_color.draw_box(tc_on=ARGS.t, label_type=ARGS.type)
    Terminal.output('\n')

if __name__ == '__main__':
    main()
    SHELL.start_app()
