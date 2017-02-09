#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
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
    Terminal()
    Terminal.hide_cursor()
    try:
        while True:
            easycat.write('/')
            time.sleep(DELTA_T)
            easycat.write('\b|')
            time.sleep(DELTA_T)
            easycat.write('\b\\')
            time.sleep(DELTA_T)
            easycat.write('\b-')
            time.sleep(DELTA_T)
            easycat.write('\b')
    except KeyboardInterrupt:
        return
    finally:
        Terminal.unhide_cursor()
