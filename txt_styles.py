#!/usr/bin/env python3
#coding=utf8
"""
Text Styles - If multiple colors arguments are given, the first one listed will
              be used.

Colors: grey, red, green, yellow, blue, magenta, cyan, white
Styles: bold, dark, underline, blink, reverse, concealed
"""
import argparse

from termcolor import cprint

from cjh.misc import notebook
import easycat
from versatiledialogs.terminal import Terminal

REMARKS = """
    - combine with bold.py, txfx.py; i.e., adapt for pipeline use"""

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
    return parser.parse_args() if __name__ == '__main__' else  None


notebook(REMARKS)
ARGS = _parse_args()
Terminal()

def main():
    """Main function"""
    
    bgcolor = 'on_' + ARGS.b if ARGS.b is not None else None
    fstring = easycat.cat(files=[ARGS.FILENAME], return_str=True)
    color = None
    styles = []

    for style in ARGS.ATTRIBUTES:
        if color is None and style in (
                'grey',
                'red',
                'green',
                'yellow',
                'blue',
                'magenta',
                'cyan',
                'white'):
            color = style            
        else:
            styles.append(style)

    cprint(fstring, color, bgcolor, styles)

if __name__ == '__main__':
    main()
    Terminal.start_app()
