#!/usr/bin/env python
#coding=utf8
"""
Generates sequences, e.g., 'a', 'b', 'c', ... , 'z', 'aa', 'bb' .... and
in the same manner for capital letters.
"""
__author__ = 'Chris Horn'
__license__ = 'GPL'

class Letter(object):
    """
    * Convert to closure or lambda of some kind? These two generators have a
    lot in common....
    """

    pass_no = 1

    @classmethod
    def caps_gen(cls, start_letter='A'):
        """Generates sequences of capital letters."""
        start_ord = ord(start_letter)
        if start_ord >= 65 and start_ord < 91:
            letters = iter(range(start_ord, 91))
            while True:
                try:
                    output = chr(next(letters))
                    if output != 'I':
                        yield output * cls.pass_no
                except StopIteration:
                    cls.pass_no += 1
                    letters = iter(range(65, 91))
        else: raise ValueError

    @classmethod
    def lower_gen(cls, start_letter='a'):
        """Generates sequences of lower-case letters."""
        start_ord = ord(start_letter)
        if start_ord >= 97 and start_ord < 123:
            letters = iter(range(start_ord, 123))
            while True:
                try:
                    output = chr(next(letters))
                    if output != 'i':
                        yield output * cls.pass_no
                except StopIteration:
                    cls.pass_no += 1
                    letters = iter(xrange(97, 123))
        else: raise ValueError

#    @staticmethod
#    def ord()
