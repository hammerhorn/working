#!/usr/bin/env python
"""
Test of Terminal.clear()
"""
import time

import easycat
from versatiledialogs.terminal import Terminal

DELTA_T = 0.25

Terminal()
for _ in xrange(Terminal.height()):
    Terminal.output('*' * Terminal.width())

for n in xrange(7):
    Terminal.clear(n)
    easycat.write('%d lines cleared\r' % n)
    time.sleep(DELTA_T)

for n in xrange(7):
    Terminal.clear(-n)
    easycat.write('%d lines cleared\r' % -n)
    time.sleep(DELTA_T)
