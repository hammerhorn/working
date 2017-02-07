#!/usr/bin/env python3
#coding=utf-8
"""
Removes trailing whitespace.
"""
import argparse
import sys
import traceback

from cjh.misc import notebook
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


def _parse_args():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str, help='file to process', nargs="?")
    parser.add_argument('-C', action='store_true')
    return parser.parse_args() if __name__ == '__main__' else None

Terminal()
ARGS = _parse_args()


def main():
    """
    Reads in a specified file, removes trailing whitespace, and re-saves.
    """
    try:
        file_handler = open(ARGS.filename, 'r+')
    except IOError:
        Terminal.output(traceback.format_exc())
        sys.exit()

    lines_of_text = file_handler.readlines()
    file_handler.seek(0)
    file_handler.truncate()

    # Preview and write text back to file and close file
    fstring = ''
    for line in lines_of_text:
        fstring = ''.join((fstring, line.rstrip(), '\n'))

    try:
        file_handler.write(fstring)
    finally:
        file_handler.close()

if __name__ == '__main__':
    notebook("""    - add text-wrapping
    - learn argparse syntax better
    - allow multiple files
    - there is probably a nicer way to write this code
    + fails to erase old file before writing new one""")
    main()
