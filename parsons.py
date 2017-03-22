#!/usr/bin/env python3
"""
* = start
R = remain same
U = up
D = down

usage:
./parsons.py [PARSONS STR]

example:
./parsons.py '*UDUDUD'

output:

  *   *   *
 / \\ / \\ / \\
*   *   *   *"""

import atexit
import sys
import time

import easycat
from cjh.misc import catch_help_flag
from versatiledialogs.terminal import Terminal


def get_dimensions():
    y_val = 0
    y_max = 0
    y_min = 0

    for char in parson_str:
        if char in '*R':
            continue
        elif char == 'U':
            y_val += 1
            if y_val > y_max:
                y_max = y_val
        elif char == 'D':
            y_val -= 1
            if y_val < y_min:
                y_min = y_val
    height = abs(y_max) + abs(y_min) + 1
    return y_val, y_max, -y_min, height  # displacement


Terminal()
atexit.register(Terminal.unhide_cursor)
catch_help_flag(help_str=__doc__, condition=len(sys.argv[1:])==0, title='Parsons Melody Contour Notation')
parson_str = sys.argv[1].upper()
change, rise, fall, height = get_dimensions()


# Make room to rise
Terminal.output('\n' * (2 * height - 1))
Terminal.cursor_v(2 * fall)

#Draw the contour
Terminal.hide_cursor()
current_level = 0
easycat.write(' ')
for char in parson_str:
    if char == '*':
        easycat.write('*')
    elif char == 'R':
        easycat.write('-*')
    elif char == 'U':
        Terminal.cursor_v(1)
        easycat.write('/')
        Terminal.cursor_v(1)
        easycat.write('*')
        current_level += 1
    elif char == 'D':
        Terminal.cursor_v(-1)
        easycat.write('\\')
        Terminal.cursor_v(-1)
        easycat.write('*')
        current_level -= 1
    time.sleep(0.075)

# Make room for the bottom
easycat.write('\n' * (2 * abs(-fall - change) + 2))
