#!/usr/bin/env python3
"""
Converts text from stdin into 1's and 0's and writes them to a file.
With -d followed by the filename, the message is decoded and written to stdout.
"""
import argparse

import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def _parse_args():
    """./bin_text.py -d filename"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', type=str, help='name of file to be decoded')
    return parser.parse_args() if __name__ == '__main__' else None

def main():
    """Encode or decode"""
    if ARGS.d is None:
        buf = easycat.cat(return_str=True) if SHELL.platform != 'android' else\
              Terminal.input(hide_form=True)
        out_str_lst = []
        for char in buf:
            out_str_lst.extend(['{0:b}'.format(ord(char)).zfill(8), ' '])
        out_str = ''.join(out_str_lst)
        SHELL.output(out_str)

        if Terminal.platform != 'android':
            with open('__data__/binary.txt', 'w') as fhandler:
                fhandler.write(out_str)
            SHELL.report_filesave('__data__/binary.txt')

    else:
        with open(ARGS.d, 'r') as fhandler:
            in_str = fhandler.read()

        bin_list = in_str.split(' ')
        for token in bin_list:
            try:
                easycat.write(chr(int(token, 2)))
            except ValueError:
                pass

Terminal()
if __name__ == '__main__':
    ARGS = _parse_args()
    SHELL = Config().start_user_profile()
    main()
    SHELL.start_app()
