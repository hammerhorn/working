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

FILE_LIST = []
PATTERN_TUPLE = (
    '*/*/*.py?',
    '*/*.py?',
    '*.py?',
    '*/*/*~',
    '*~',
    '*/*~',
    '__data__/*.tmp'
)

# Build up a list of all files matching one of the patterns
for pattern in PATTERN_TUPLE:
    FILE_LIST.extend(glob(pattern))

# Deletes each file in the list
for filename in FILE_LIST:
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
