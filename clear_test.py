#!/usr/bin/env python
import time

import easycat
from versatiledialogs.terminal import Terminal
Terminal()
for line in range(Terminal.height()):
    Terminal.output('*' * Terminal.width())

for n in range(7):
    Terminal.clear(n)
    easycat.write('%d lines cleared\r' % n)
    time.sleep(.25)

for n in range(7):
    Terminal.clear(-n)
    easycat.write('%d lines cleared\r' % -n)
    time.sleep(.25)
