#!/usr/bin/env python3
"""
Test of Terminal.clear()
"""
import time

import easycat
from ranges import gen_range
from versatiledialogs.terminal import Terminal

DELTA_T = 0.125

def tri_num_limit(limit):
    sum = 0
    for i in gen_range(100):
        sum += i
        if sum > limit:
            return i

Terminal()


if __name__ == '__main__':
    # Star Fill
    for _ in gen_range(Terminal.height()):
        Terminal.output('*' * Terminal.width())


    # How many loops will fit on the screen?
    loops = tri_num_limit(Terminal.height())


    # Demonstrate clear()
    for x in gen_range(2):
        for n in gen_range(loops):
            if x == 1:
                n *= -1
            Terminal.clear(n)
            easycat.write('%d lines cleared\r' % n)
            time.sleep(DELTA_T)







