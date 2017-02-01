#!/usr/bin/env python
"""
Animation #1: Oscillation.

Control certain aspects of a simple animation.
"""

import argparse
# import os
import time

from cjh.misc import notebook
from cjh.tablegames.igo import Goban

from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - animate1() or something could be a method of cjh.geometry.Graph
    - Also, the ability to 'trace' the oscillation (like a seismograph) would be
      quite nice."""

def _parse_args():
    """
    Parse arguments
    (see above)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-t', '--deltat', type=float, help='time interval, default 0.1')
    parser.add_argument(
        '-d', '--deltad', type=float, help='displacement interval, default 2')
    parser.add_argument('-z', '--size', type=int, help='board size, default 19')
    parser.add_argument(
        '-C', action='store_true', help="see developer's comments")


    if __name__ == '__main__':
        args = parser.parse_args()
    else:
        args = None
    return args

# Set all Parameters
ARGS = _parse_args()
notebook(REMARKS)

if ARGS is not None and ARGS.deltat is not None:
    T_INTERVAL = ARGS.deltat
else:
    T_INTERVAL = 0.1

if ARGS is not None and ARGS.deltad is not None:
    D_INTERVAL = ARGS.deltad
else:
    D_INTERVAL = 2

if ARGS is not None and ARGS.size is not None:
    SIZE_ = ARGS.size
else:
    SIZE_ = 19


def main():
    """
    This particular file shows a point oscillating left and right along
    the x-axis.
    """
    goban = Goban(size=SIZE_, sh_obj=Terminal(), adjust_ssize=-8)
    current_frame_no = 0
#    count = 0
    while True:
        for i in range(
                -(goban.max_domain),
                goban.max_domain + 1,
                int(round(D_INTERVAL))
            ):
            #count = 0
            goban.plot_point(i, 0, 'white')
            #for j in range(count + 1):
            #goban.plot_point(i - int(round(D_INTERVAL)), count - 1, 'white')

            current_frame_no += 1
            Terminal.print_header('+f{}'.format(current_frame_no))
            Terminal.output((str(goban).rstrip()))
            time.sleep(T_INTERVAL)
            goban.plot_point(i, 0, 'empty')

            #count += 1

        for i in range(
                -(goban.max_domain - 1),
                (goban.max_domain),
                int(round(D_INTERVAL))
            ):
            goban.plot_point(-i, 0, 'black')
            current_frame_no += 1
            Terminal.print_header('+f{}'.format(current_frame_no))
            Terminal.output((str(goban).rstrip()))
            time.sleep(T_INTERVAL)
            goban.plot_point(-i, 0, 'empty')
            #goban.plot_point(-i, count + 1, 'black')
            #count += 1
#        count -= 1
if __name__ == '__main__':
    Terminal.hide_cursor()  # os.system('tput civis')
    try:
        main()
    finally:
        Terminal.unhide_cursor()  # os.system('tput cnorm')
