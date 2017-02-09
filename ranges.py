import sys
if sys.version_info.major == 2:
        from itertools import izip

def gen_range(*args):
    return range(*args) if sys.version_info.major == 3 else xrange(
        *args)

def lst_range(*args):
    return list(range(*args)) if sys.version_info.major == 3 else range(
        *args)

def iter_zip(list1, list2):
    return zip(list1, list2) if sys.version_info.major == 3 else izip(
        list1, list2)
