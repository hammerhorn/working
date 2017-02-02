#!/usr/bin/env python3
#coding=utf8
"""
Deletes:
    - .pyc files created by Python
    - backup~ files created by Emacs
    - .tmp files created by shellib.start_app()
"""
from glob import glob
import os

__author__ = 'Chris Horn'
__license__ = 'GPL'

FILELIST = glob('*/*/*.py?') + glob('*/*.py?') + glob('*.py?') + glob('*/*/*~')\
           + glob('*~') + glob('*/*~') + glob('__data__/*.tmp')

for filename in FILELIST:
    os.remove(filename)

