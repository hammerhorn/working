#!/usr/bin/env python3
#coding=utf8
"""
generate a shuffled sequence of integers 1 thru n
"""
import argparse, threading

from cjh.spinner import spin
from cjh.tonerow import Tonerow
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal


def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', type=int, help='length of tonerow')
    parser.add_argument(
        '-q', action='store_true', help='suppress GUI, for use with pipes')
    return parser.parse_args()

if __name__ == '__main__':
    Terminal().hide_cursor()
    ARGS = _parse_args()
    LENGTH = ARGS.n if ARGS.n is not None else 12
    SHELL = Terminal() if ARGS.q is True else Config().start_user_profile()

done_flag = False

#def pinwheel():
#    global done_flag
#    while done_flag is False:
#        spin()

def generate_row():
    global done_flag, row
    row = Tonerow(LENGTH)
    done_flag = True

def main():
    """
    Main function
    """
    global row

    row = None
    th = threading.Thread(target=generate_row)
    th.start()
    while done_flag is False:
        spin()
        #easycat.write('\r', stream=2)
        Terminal.clear(0)  # stream=2)

     
    #th.start()
    #row = Tonerow(LENGTH)
    th.join()
    Terminal.output(row)
    Terminal.unhide_cursor()  # stream=2)
    if ARGS.q is True:
        return
    if SHELL == 'Tk':
        SHELL.msg.config(bg='dark green', fg='white', font=('helvetica', 33), width=700)
        SHELL.main_window.config(bg='dark green')
        #if ARGS.q is False:
        SHELL.output('[{}]'.format(row.__str__().replace(' ', ', ')), width=700, height=90)
        #else:
        #    SHELL.exit()
    elif SHELL.interface in ('dialog', 'zenity') and ARGS.q is False:
        SHELL.output(row, height=10)

    #print(row)

if __name__ == '__main__':
    main()
    SHELL.start_app()
