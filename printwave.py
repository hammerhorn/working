#!/usr/bin/env python3
"""
Inspired by the classic BASIC program by David Ahl.
"""

import math
import sys
import time

import easycat
from versatiledialogs.terminal import Terminal

def print_welcome():
    Terminal()
    Terminal.clear()
    Terminal.output(' ' * 30 + 'SINE WAVE')
    Terminal.output(' ' * 15 + 'CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY\n')
    Terminal.wait()
    Terminal.output('\n' * 4)


a_number = float(sys.argv[1]) if len(sys.argv[1:]) >= 1 else 4.0
print_welcome()


def main():
    toggle, iter_count = 0, 0
    try:
        Terminal.hide_cursor()
        while True:
            s = iter_count / a_number
            width = Terminal.width()
            indent = int((width - 10) * math.sin(s) + width - 8) // 2
            easycat.write(' ' * indent)
            if(toggle == 1):
                Terminal.output('SPECIAL')
                toggle = 0
            else:
                Terminal.output('YOU ARE')
                toggle = 1
            time.sleep(.018)
            iter_count += 1

    except KeyboardInterrupt:
        pass

    finally:
        Terminal.unhide_cursor()

if __name__ == '__main__':
    main()
    Terminal.start_app()
