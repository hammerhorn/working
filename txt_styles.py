#!/usr/bin/env python
#coding=utf8
"""
Text Styles

colors: grey, red, green, yellow, blue, magenta, cyan, white
styles: bold, dark, underline, blink, reverse, concealed
"""
import argparse

from termcolor import cprint

from cjh.misc import notebook
import easycat
from versatiledialogs.terminal import Terminal

REMARKS = """
    """

def _parse_args():
    """
    Parse arguments; --help for more info
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-C', action='store_true', help="see developer's comments")

    parser.add_argument('-b', type=str, help='background color')
    parser.add_argument('FILENAME', type=str, help='filename')
    parser.add_argument('ATTRIBUTES', nargs='*')
    if __name__ == '__main__':
        args = parser.parse_args()
    else:
        args = None
    return args

notebook(REMARKS)
ARGS = _parse_args()
Terminal()

def main():
    """Main function"""
    if ARGS is not None and ARGS.b is not None:
        bgcolor = 'on_' + ARGS.b
    else:
        bgcolor = None
    string = easycat.cat(files=[ARGS.FILENAME], return_str=True)
    color = None
    for index in range(len(ARGS.ATTRIBUTES)):
        if ARGS.ATTRIBUTES[index] in [
                'grey',
                'red',
                'green',
                'yellow',
                'blue',
                'magenta',
                'cyan',
                'white']:
            color = ARGS.ATTRIBUTES[index]
            del ARGS.ATTRIBUTES[index]
            break

    if bgcolor is not None:
        cprint(string, color, bgcolor, attrs=ARGS.ATTRIBUTES)
    elif color is not None:
        cprint(string, color, attrs=ARGS.ATTRIBUTES)
    else:
        cprint(string, attrs=ARGS.ATTRIBUTES)

if __name__ == '__main__':
    main()
    Terminal.start_app()
