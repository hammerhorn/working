#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
import threading
import time

import easycat
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn'
__license__ = 'GPL'

DELTA_T = 0.075

def spin():
    """
    spinning character on the screen
    """
    #easycat.write('\033[?25l', stream=2)
#    Terminal.hide_cursor()
#    try:
#        easycat.write('\b/', stream=2)
#        time.sleep(DELTA_T)
#        easycat.write('\b|', stream=2)
#        time.sleep(DELTA_T)
#        easycat.write('\b\\', stream=2)
#        time.sleep(DELTA_T)
#        easycat.write('\b-', stream=2)
#        time.sleep(DELTA_T)

#    except KeyboardInterrupt:
#        return
#    Terminal.cursor_h(1)
    for char in ('/', '|', '\\', '-'):
        easycat.write(char, stream=2)
        time.sleep(DELTA_T)
        easycat.write('\b', stream=2)
