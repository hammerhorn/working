#!/usr/bin/env python
"""
Inspired by the classic BASIC program by David Ahl.
"""

import math
import sys
import time

import easycat
from versatiledialogs.terminal import Terminal

if len(sys.argv[1:]) >= 1:
    a_number = float(sys.argv[1])
    if len(sys.argv[1:]) >= 2:
        a_string = sys.argv[2]
    else:
        a_string = '*****'
else:
    a_number = 4.0
    a_string = '*****'


Terminal()
Terminal.clear()
Terminal.output(' ' * 30 + 'SINE WAVE')
Terminal.output(' ' * 15 + 'CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY\n')
Terminal.wait()
Terminal.output('\n' * 4)

toggle = 0
iter_count = 0

try:
    Terminal.hide_cursor()
    while True:
        s = iter_count / a_number
        width = Terminal.width()
        indent = int((width - 10) * math.sin(s) + width - 8) // 2
        easycat.write(' ' * indent)
        if(toggle == 1):
            Terminal.output('CREATIVE')
            toggle = 0
        else:
            Terminal.output('COMPUTING')
            toggle = 1
        time.sleep(.008)
        iter_count += 1

except KeyboardInterrupt:
    pass

finally:
    Terminal.unhide_cursor()
