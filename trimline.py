#!/usr/bin/env python
#coding=utf-8
"""
Removes trailing whitespace.
"""
import argparse
import pydoc
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
    args = parser.parse_args() if __name__ == '__main__' else None
    return args


def main():
    """
    Reads in a specified file, removes trailing whitespace, and re-saves.
    """

    # Open file and store lines as str list
    try:
        file_handler = open(ARGS.filename, 'r+')
    except IOError:
        Terminal.output(traceback.format_exc())
        sys.exit()

    lines_of_text = file_handler.readlines()
    file_handler.seek(0)
    file_handler.truncate()

    # Preview and write text back to file and close file
    #Terminal.output(lines_of_text)
    #Terminal.wait()
    string = ''
    preview_string = ''
    for index, _ in enumerate(lines_of_text):
        string += lines_of_text[index].rstrip() + '\n'
        preview_string = string.strip() + Terminal.fx('b', 'EOL')
    pydoc.pipepager(preview_string, cmd='less -R')
    try:
        char = Terminal.get_keypress('Write to file?')
        assert char == 'y'
        file_handler.write(string)
    except AssertionError:
        Terminal.output('File not saved.  Good bye.')
    finally:
        file_handler.close()

Terminal()
ARGS = _parse_args()

if __name__ == '__main__':
    notebook("""    - add text-wrapping
    - learn argparse syntax better
    - allow multiple files
    + fails to erase old file before writing new one""")
    main()
