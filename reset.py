#!/usr/bin/env python
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

FILELIST = glob('*/*/*.pyc') + glob('*/*.pyc') + glob('*.pyc') + glob('*/*/*~')\
           + glob('*~') + glob('*/*~') + glob('*.tmp')

for filename in FILELIST:
    os.remove(filename)

