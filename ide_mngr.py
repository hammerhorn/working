#!/usr/bin/env python
#coding=utf8
"""
selects a python file in the current directory at random and outputs the
filename.
"""
import os
# import sys
from random import randint

from versatiledialogs.config import Config

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

CONFIG = Config()
SHELL = CONFIG.start_user_profile()
if SHELL.interface in ['wx', 'Tk']:
    SHELL.center_window()

ALL_FILES = os.listdir('.')
PY_FILES = [this_file for this_file in ALL_FILES if this_file.endswith('.py')]
NUMBER_OF_PYFILES = len(PY_FILES)

def main():
    """DOCSTR"""
    index = randint(0, NUMBER_OF_PYFILES - 1)
    if SHELL.interface in ['wx', 'Tk']:
        SHELL.message(PY_FILES[index])
    else:
        SHELL.output(PY_FILES[index])
    SHELL.exit()

if __name__ == '__main__':
    main()
    SHELL.start_app()

