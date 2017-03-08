#!/usr/bin/env python3
"""
Inspired by the classic BASIC program by David Ahl.
"""

import math
import sys
import time

from cjh.misc import notebook
import easycat
from versatiledialogs.terminal import Terminal

def print_welcome():
    Terminal.clear()
    Terminal.output(''.join((
        ' ' * 30, 'SINE WAVE\n',
        ' ' * 15, 'CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY\n')))
    Terminal.wait()
    Terminal.output('\n' * 4)


REMARKS = """
    - allow real-time modification of the speed, wavelength"""
DELTA_T = 0.018
notebook(REMARKS)

a_number = float(sys.argv[1]) if __name__ == '__main__' and len(sys.argv[1:]) >= 1 else 4.0
Terminal()



def main():
    print_welcome()
    toggle, iter_count = 0, 0
    try:
        Terminal.hide_cursor()
        while True:
            s = iter_count / a_number
            width = Terminal.width()
            indent = int((width - 10) * math.sin(s) + width - 8) // 2
            easycat.write(' ' * indent)
            if toggle == 1:
                Terminal.output('COMPUTING')
                toggle = 0
            else:
                Terminal.output('CREATIVE')
                toggle = 1
            time.sleep(DELTA_T)
            iter_count += 1

    except KeyboardInterrupt:
        pass

    finally:
        Terminal.unhide_cursor()

if __name__ == '__main__':
    main()
    Terminal.start_app()
