#!/usr/bin/env python3
"""
Converts text from stdin into 1's and 0's and writes them to a file.
With -d, or -f followed by a filename, the message is decoded and written to
stdout.

Ex.:
> Hello, World!

01001000 01100101 01101100 01101100 01101111
00101100 00100000 01010111 01101111 01110010
01101100 01100100 00100001 00001010
"""
import argparse
import textwrap

from termcolor import cprint

from cjh.misc import catch_help_flag, notebook
import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

DEFAULT = '__data__/binary.txt'
REMARKS = """
    - move functionality to Letter class
    - combine with morse, radio, braille, etc...."""

def _parse_args():
    """
    ./bin_text.py -d filename
    """
    notebook(REMARKS)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', type=str, help='decode from user-specified file')
    parser.add_argument('-d', action='store_true', help="decode from '{}'".format(DEFAULT))
    catch_help_flag(__doc__.lstrip(), cleanup=lambda: Terminal.output(''), argprsr=parser)
    return parser.parse_args() if __name__ == '__main__' else None


def main():
    """
    Encode or decode
    """
    EOF = '[ENTER] ^D' if SHELL.os_name == 'posix' else '^Z [ENTER]'
    if ARGS.__dict__ == {'f': None, 'd': False}:
        if SHELL.platform != 'android' and SHELL == 'term':
            cprint('(%s to end)' % EOF, attrs=['reverse'])
            easycat.write('Message: ')
            buf = easycat.cat(return_str=True, quiet=True)
        else:
            buf = SHELL.input(prompt='Message: ', hide_form=True)
        out_str_lst = []
        for char in buf:
            out_str_lst.extend(['{0:b}'.format(ord(char)).zfill(8), ' '])
        out_str = ''.join(out_str_lst)
        kwarg_dict = {}
        lines = len(out_str) // 45
        if SHELL == 'Tk':
            kwarg_dict.update({
                'width' : 400,
                'height': (lines + 1) * 18})
        out_str = textwrap.fill(out_str, width=45)
        SHELL.output('\n%s\n' % out_str, **kwarg_dict)

        if Terminal.platform != 'android':
            with open(DEFAULT, 'w') as fhandler:
                fhandler.write(out_str)
            SHELL.report_filesave(DEFAULT, fast=True)
            Terminal.output('')

    else:
        filename = ARGS.f if ARGS.f is not None else DEFAULT
        with open(filename, 'r') as fhandler:
            in_str = fhandler.read()
        in_str = in_str.replace('\n', ' ')
        bin_list = in_str.split(' ')
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
