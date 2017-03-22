#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
import os
import textwrap

from cjh.maths.geometry import Graph, Point
from things import Thing
from versatiledialogs.terminal import Terminal, ListPrompt

__author__ = 'Chris Horn'
__license__ = 'GPL'

class Goban(Graph):
    """
    a crude graphing calculator in the shape of a go board
    """
    def __init__(self, size=19, skinfile='unicode1.json', sh_obj=Terminal(),
                 adjust_ssize=0):
        """
        Call parent constructor; declare empty list, 'self.groups'.
        """
        super(Goban, self).__init__(size, skinfile, sh_obj, adjust_ssize)
        self.groups = []

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['sh_obj']
        return state

     ###########
     #  BOARD  #
     ###########
    def is_hoshi(self, coords):
        """
        Return True if the point is a starpoint; should take A1 type args.
        """
        x_coord, y_coord = coords

        # Convert ordered pair to array indices
        x_coord += self.max_domain
        y_coord = self.max_domain - y_coord

        # Determine starpoint
        if self.size >= 12:
            starpoint = 4
        elif self.size >= 9:
            starpoint = 3
        else:
            starpoint = 2

        side_point = False
        if self.size % 2 == 1 and self.size >= 13:
            side_point = True

        if x_coord == starpoint - 1 == y_coord:
            return True

        if side_point is True:
            if (x_coord == self.max_domain and y_coord == starpoint - 1) or \
               (x_coord == starpoint - 1 and y_coord == self.max_domain) or \
               (x_coord == starpoint - 1 and y_coord == self.max_domain) or \
               (x_coord == self.size - starpoint and y_coord == self.max_domain) or \
               (x_coord == self.max_domain and y_coord == self.size - starpoint):
                return True

        if (x_coord == self.size - starpoint and y_coord == starpoint - 1) or \
           (x_coord == starpoint - 1 and y_coord == self.size - starpoint) or \
           (x_coord == self.size - starpoint and y_coord == self.size - starpoint):
            return True
        return False

    def access_gnugo_functs(self, basename):
        """
        Scoring/estimating tools from gnugo; this should take filename instead.
        """
        Terminal.make_page(
            'WRITE FILE: {}.sgf'.format(basename),
            self,
            lambda: self.write_sgf(basename))

        menu1 = ListPrompt(('..', 'fast', 'medium', 'slow'))
        sel1 = Terminal.make_page('MENU: GNUGO Scoring Tools', self, menu1.input)
        gnugo_dict = {'fast':'estimate', 'medium':'finish', 'slow':'aftermath'}
        Terminal.output('')
        if sel1 != 1:
            os.system('gnugo --score ' + gnugo_dict[menu1.items[sel1 - 1]] +\
                      ' --quiet -l {}.sgf'.format(basename))
            Terminal.wait()

     ############
     #  POINTS  #
     ############
    def place_stone(self, letter, number, color):
        """
        Add a stone to the board.  letter, number are the coordinates, color is
        color.
        """
        letter = letter.upper()

        # 'I' is skipped in th enumeration
        if letter >= 'I':
            ordinal = ord(letter) - 66
        else:
            ordinal = ord(letter) - 65
        tmp_pt = self.indices_to_point(ordinal, self.size - number)

        x_val, y_val = tmp_pt.x_mag, tmp_pt.y_mag

        #If it is a legal move
        #????????????????

        self.plot_point(x_val, y_val, color)
        self.cursor = x_val, y_val


class GoStone(Point):
    """
    attributes such as color, position
    """
    def __init__(self, color, pt_tuple):
        super(GoStone, self).__init__()
        self.alive = True
        self.color = color
        self.pt_tuple = pt_tuple


class Group(Thing):
    """
    (this class will deal with groups)
    """
    def __init__(self):#, seed_stone):
        super(Group, self).__init__()
