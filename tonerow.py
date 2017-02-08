#!/usr/bin/env python3
#coding=utf8
"""
generate a shuffled sequence of integers 1 thru n
"""
import argparse

from cjh.tonerow import Tonerow
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal


def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
   #parser.add_argument('-C', action='store_true', help="developer's comments")
    parser.add_argument('-n', type=int, help='length of tonerow')
    parser.add_argument(
        '-q', action='store_true', help='suppress GUI, for use with pipes')
    return parser.parse_args()

if __name__ == '__main__':
    ARGS = _parse_args()
    if ARGS.n is not None:
        LENGTH = ARGS.n
    else: LENGTH = 12

SHELL = Config().start_user_profile()

def main():
    """
    Main function
    """
    if SHELL.interface == 'Tk':
       #SHELL.center_window(width_=600, height_=80)
        SHELL.msg.config(bg='dark green', fg='white', font=('helvetica', 33), width=700)
        SHELL.main_window.config(bg='dark green')

    row = Tonerow(LENGTH)

    if SHELL.interface == 'Tk':
        if ARGS.q is False:
            SHELL.output('[{}]'.format(row.__str__().replace(' ', ', ')), width=700, height=90)
        else: SHELL.exit()
    elif SHELL.interface in ('dialog', 'zenity') and ARGS.q is False:
        SHELL.output(row, height=10)
    Terminal.output(row)

#    if ARGS.q is False:
#        if SHELL.interface == 'Tk':
#            SHELL.output('[{}]'.format(row.__str__().replace(' ', ', ')), width=700, height=90)            
#        elif SHELL.interface in ['dialog', 'zenity']:
#            SHELL.output(row, height=10)
#    Terminal.output(row)
#    SHELL.exit()

if __name__ == '__main__':
    main()
    SHELL.start_app()
