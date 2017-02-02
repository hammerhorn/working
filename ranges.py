import sys

def gen_range(*args):
    gen = range(*args) if sys.version_info.major == 3 else xrange(
        *args)
    return gen

def lst_range(*args):
    lst = list(range(*args)) if sys.version_info.major == 3 else range(
        *args)
    return lst
