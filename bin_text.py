#!/usr/bin/env python3
"""
Converts text from stdin into 1's and 0's and writes them to a file.
With -d followed by the filename, the message is decoded and written to stdout.
"""
import argparse
import sys
import textwrap

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def _parse_args():
    """./bin_text.py -d filename"""
    # this should be a form of catch_help_flag
    helpflag = True if {'-h', '--help'} & set(sys.argv[1:]) else False
    if helpflag is True:
        Terminal.output('')
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('-d', type=str, help='name of file to be decoded')
        args = parser.parse_args() if __name__ == '__main__' else None
    finally:
        if helpflag is True:
            Terminal.output('')
    return args

def main():
    """Encode or decode"""
    if ARGS.d is None:
        buf = easycat.cat(return_str=True, quiet=True) if SHELL.platform != 'android' and\
              SHELL.interface == 'term' else SHELL.input(hide_form=True)
        out_str_lst = []
        for char in buf:
            out_str_lst.extend(['{0:b}'.format(ord(char)).zfill(8), ' '])
        out_str = ''.join(out_str_lst)
        kwarg_dict = {}
        lines = len(out_str) // 45
        if SHELL.interface == 'Tk':
            kwarg_dict.update({
                'width': 400,
                'height': (lines + 1) * 18})
        out_str = textwrap.fill(out_str, width=45)        
        SHELL.output(''.join(('\n', out_str, '\n')), **kwarg_dict)

        if Terminal.platform != 'android':
            with open('__data__/binary.txt', 'w') as fhandler:
                fhandler.write(out_str)
            SHELL.report_filesave('__data__/binary.txt', fast=True)
            Terminal.output('')

    else:
        with open(ARGS.d, 'r') as fhandler:
            in_str = fhandler.read()
        #Terminal.wait(in_str)
        in_str = in_str.replace('\n', ' ')
        bin_list = in_str.split(' ')
        #print(bin_list)
        char_list = []
        for token in bin_list:
            try:
                char_list.append(chr(int(token, 2)))
            except ValueError:
                pass
        SHELL.output(''.join(char_list))
Terminal()
if __name__ == '__main__':
    ARGS = _parse_args()
    SHELL = Config().start_user_profile()
    main()
    SHELL.start_app()
