#!/usr/bin/env python3
"""
Test of Terminal.clear()
"""
import time

import easycat
from ranges import gen_range
from versatiledialogs.terminal import Terminal

DELTA_T = 0.25

def tri_num_limit(limit):
    sum = 0
    for i in gen_range(100):
        sum += i
        if sum > limit:
            return i

Terminal()
for _ in gen_range(Terminal.height()):
    Terminal.output('*' * Terminal.width())

loops = tri_num_limit(Terminal.height())
    
for n in gen_range(loops):
    Terminal.clear(n)
    easycat.write('%d lines cleared\r' % n)
    time.sleep(DELTA_T)

for n in gen_range(loops):
    Terminal.clear(-n)
    easycat.write('%d lines cleared\r' % -n)
    time.sleep(DELTA_T)





    
                            
