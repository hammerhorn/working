#!/usr/bin/env python
from versatiledialogs.terminal import Terminal
VT = Terminal()

def gen_range(*args):  # min=None, max=None, stepwise=1):
    gen = range(*args) if VT.py_version == 3 else xrange(
        *args)
    return gen

def lst_range(*args):  # min=None, max=None, stepwise=1):
    lst = list(range(*args)) if VT.py_version == 3 else range(
        *args)
    return lst
