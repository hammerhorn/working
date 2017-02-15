#!/usr/bin/env python
#coding=utf8
"""
New program
"""
import sys

from cjh.music import Pitch
from versatiledialogs.terminal import Terminal
from things import Thing

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


class TabStaff(Thing):
    """
    Tablature for 6-string guitar
    """
    class GtrString(Thing):
        """
        individual gtr string
        """
        Terminal()
        WIDTH = Terminal.width() // 4

        def __init__(self, string_no=6):
            super(TabStaff.GtrString, self).__init__()
            self.fret_list = []
            for _ in range(self.__class__.WIDTH):
                self.fret_list.append(-1)
            self.open_pitch = Pitch()

        def __str__(self):
            out_str_lst = []
            for col in self.fret_list:
                new_part = '---' if col == -1 else '-{}-'.format(col)
                out_str_lst.append(new_part)
            out_str_lst.append('\n')
            return ''.join(out_str_lst)

    def __init__(self):
        super(TabStaff, self).__init__()
        self.strings = []
        for _ in range(6):
            self.strings.append(self.__class__.GtrString())

    def __str__(self):

        for x in range(9):
            sys.stdout.write(' {} '.format(x+1))

        buffer_lst = ['\n']
        for gtr_string in self.strings:
            buffer_lst.append(gtr_string.__str__())
        return ''.join(buffer_lst)

    def add_entry(self, string_no, fret_no, column_no):
        self.strings[string_no - 1].fret_list[column_no - 1] = fret_no

