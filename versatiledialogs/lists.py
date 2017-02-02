#!/usr/bin/env python
#coding=utf8
"""
list-type objects
"""
import abc

from things import Thing

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


class AbstractList(Thing):
    """
    Abstract parent for all list-type objects in this package.
    * This should be modified to inherit from the native Python list.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, items, heading=None):
        super(AbstractList, self).__init__()
        if heading is not None:
            self.show_heading = True
            self.label = heading
        else: self.show_heading = False
        self.items = items

    @abc.abstractmethod
    def __str__(self):
        """
        Prints either '[Empty List]' or nothing.
        """
        string = ''
        if len(self) == 0:
            string += ' [Empty List]\n'
        return string

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def index(self, ind):
        return self.items.index(ind)
    
    def sort(self):
        """
        Sort items in place.
        """
        self.items.sort()

    def sorted(self):
        """
        Returns a sorted copy.
        """
        return sorted(self.items)


class PlainList(AbstractList):
    """
    is displayed like a normal list type (e.g., [1, 2, 3, 4]), but inherits
    attributes 'count', 'heading', et al....
    """

    def __init__(self, items, heading=None):
        super(PlainList, self).__init__(items)
        self.label = heading

    def __str__(self):
        string = '\n'
        if self.show_heading:
            string += self.label.upper() + ':'
        string += super(PlainList, self).__str__()
        if len(self) > 0:
            string += str(self.items)
        return string


class VerticalList(AbstractList):
    """
    Abstract parent class for ItemList and Enumeration.

    *Perhaps an indentation mechanism should be worked out.
    """

    def __init__(self, items, heading=None):
        super(VerticalList, self).__init__(items)

    def __str__(self):
        string = '\n'
        if self.show_heading is True and self.label is not None:
            string += self.label
            string += '\n{}'.format('=' * len(self.label))
        string += super(VerticalList, self).__str__()
        return string + '\n'


class ItemList(VerticalList):
    """
    Bulleted VerticalList.
    """
    def __init__(self, items, heading=None):
        super(ItemList, self).__init__(items, heading)
        self.bullet = '•'


    def __str__(self):
        string = ' ' + super(ItemList, self).__str__()
        if len(self) > 0:
            for item in self:
                string += '  {} {}\n'.format(self.bullet, item)
        return string


class Enumeration(VerticalList):
    """
    Numbered VerticalList.
    """
    def __init__(self, items, heading=None):
        super(Enumeration, self).__init__(items)

    def __str__(self):
        """
        *maybe this can be united with its parent method somehow
        """
        string = super(Enumeration, self).__str__()
        if len(self) > 0:
            for num, val in enumerate(self):
                string += '{:>2}. {}\n'.format((num + 1), val)
        return string
