#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
import collections
import math
import timeit

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

import easycat
from ranges import gen_range
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn'
__license__ = 'GPL'


#class Member(object):
#    def __init__(self, val):
#        self.value = val
#        self.

class DataSet(object):
    """
    A list of values on which you can perform: mean, median, mode,
    use [indices], and print an ascii histogram.  Mode and index
    should work with a list that includes strings, but the other
    functions all require a numerical value.
    """

    def __init__(self, list_=[]):
        self.items = np.array(list_)
        self.items.sort()

    def __getitem__(self, index):
        """ set() works """
        return self.items[index]

    def __str__(self):
        float_str_list_str = str(['{:.4g}'.format(f) for f in self.items])
        return float_str_list_str.replace(
            '[', '{').replace(']', '}').replace("'", '')

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.items.size

    def __max__(self):
        return max(self.items)

    def __min__(self):
        return min(self.items)

    def numpy_sum(self, show_label=False):
        """
        Find sum using the numpy module.
        """
        total = 'Not available.' if NUMPY_AVAILABLE is not True else np.array(
            self.items, float).sum()
        return 'numpy.array.sum(): {}'.format(total) if show_label is True\
            else total

    def math_sum(self, show_label=False):
        """
        Calculate using the math module from the standard library.
        """
        total = math.fsum(self.items)
        return 'math.fsum(): {}'.format(total) if show_label is True else total

    def native_sum(self, show_label=False):
        """
        Calculate using the native sum() function.
        """
        total = sum(self.items)
        return 'sum(): {}'.format(total) if show_label is True else  total

    def sum_str(self):
        out_str_list = []

        # Make into a loop
        out_str_list.append('{}\n({:.2g} s)\n\n'.format(
            self.math_sum(True),
            timeit.timeit(lambda: self.math_sum(True), number=1000)))
        out_str_list.append('{}\n({:.2g} s)\n\n'.format(
            self.numpy_sum(True),
            timeit.timeit(lambda: self.numpy_sum(True), number=1000)))
        out_str_list.append('{}\n({:.2g} s)\n\n'.format(
            self.native_sum(True),
            timeit.timeit(lambda: self.native_sum(True), number=1000)))
        return ''.join(out_str_list)

    def range_str(self, lang='EN'):
        label_dict = {'EN':'cardinality', 'EO':'kardinalo'}
        return '  {} ≤ {{{} {}}} ≤ {}\n'.format(
            min(self), label_dict[lang.upper()], len(self), max(self))

    def averages_str(self, lang='EN'):
        out_str_list = []
        # loop-ize?
        label_dict = {'EN':'mean', 'EO':'meznombro'}
        out_str_list.append(
            "{:>9} = {:.4g}\n".format(label_dict[lang.upper()], self.mean))

        label_dict = {'EN':'median', 'EO':'mediano'}
        out_str_list.append(
            "{:>9} = {:.4g}\n".format(label_dict[lang.upper()], self.median))

        label_dict = {'EN':'mode', 'EO':'   reĝimo'}
        out_str_list.append(
            "{:>9} = {}\n".format(label_dict[lang.upper()], self.mode))
        return ''.join(out_str_list)

    @property
    def mean(self):
        return self.items.mean()

    @property
    def median(self):
        self.items.sort()
        if self.items.size % 2 == 1:
            return self.items[(self.items.size - 1) // 2]
        else:
            middle_two = DataSet(
                self.items[
                    (self.items.size // 2 - 1):(self.items.size // 2 + 1)])
            return middle_two.mean

    @property
    def mode(self):
        mode_list = []
        common_list = collections.Counter(self.items).most_common()
        freq_list = [f[1] for f in common_list]
        mode_list = [m[0] for m in common_list if m[1] == max(freq_list)]
        mode_set = DataSet([float(m) for m in mode_list])
        return mode_set

    @property
    def variance(self):
        variance_list = [(i-self.mean) ** 2 for i in self]
        variance_set = DataSet(variance_list)
        return variance_set.mean

    @property
    def std_dev(self):
        return float('{:.4g}'.format(float(self.variance) ** 0.5))

    def histogram(self):
        easycat.write('\n%3s:' % self.items[0])
        for i in gen_range(len(self)):
            easycat.write('[*]')
            try:
                if self[i] != self[i + 1]:
                    easycat.write('\n%3s:' % self[i + 1])
            except IndexError:
                pass
        Terminal.output('\n')
