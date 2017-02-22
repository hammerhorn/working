#!/usr/bin/env python
#coding=utf8
"""
Contains class for simulating die-rolls.
"""
from random import randint
import time

from things import Thing
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Die(Thing):
    """
    For simulated die-rolls.  "Sidedness" of die can be specified.
    """

    def __init__(self, sides=6):
        super(Die, self).__init__()
        Terminal()
        self.face = []
        self.sides = sides
        self.label = '(d{})'.format(self.sides)
        self.value = randint(1, self.sides)
        self.clear_face()

    def __call__(self):
        """
        prints diagram to screen and returns the value
        """
        self.roll()
        if self.sides <= 6:
            Terminal.output('')
            self.clear_face()
            self.generate_face()
            self.draw_face()
        else:
            Terminal.output(self.value)
        return self.value

    def __str__(self):
        return ' '.join((self.label, str(self.value)))

    def __len__(self):
        return self.sides

    def __eq__(self, other):
        if type(other) == type(self):
            return self.value == other.value
        elif type(other) == int:
            return self.value == other
        else:
            return None

    def __gt__(self, other):
        return self.value > other.value

#   def __add__(self, ):
#       sum_die = Die()
#       sum_die.value = self.value + other.value

#    def __iter__(self):
#        return self
#    def next()

    def clear_face(self):
        self.face = [' ----- ',
                     '|     |',
                     '|     |',
                     '|     |',
                     ' ----- ']

    def roll(self):
        self.value = randint(1, self.sides)

    def generate_face(self):
        self.clear_face()
        if   self.value == 1:
            self.face[2] = '|  *  |'
        elif self.value == 2:
            self.face[1] = '|    *|'
            self.face[3] = '|*    |'
        elif self.value == 3:
            self.face[1] = '|    *|'
            self.face[2] = '|  *  |'
            self.face[3] = '|*    |'
        elif self.value == 4:
            self.face[1] = '|*   *|'
            self.face[3] = '|*   *|'
        elif self.value == 5:
            self.face[1] = '|*   *|'
            self.face[2] = '|  *  |'
            self.face[3] = '|*   *|'
        elif self.value == 6:
            self.face[1] = '|*   *|'
            self.face[2] = '|*   *|'
            self.face[3] = '|*   *|'

    def draw_face(self, get_str=False, verbose=False, shellib=Terminal):
        self.generate_face()
        
        str_list = [str(self), '\n'] if verbose is True else []
        for index in range(5):
            str_list.extend([self.face[index], '\n'])
        string = ''.join(str_list)
        if get_str is True:
            return string
        else:
            heading = ' ' if verbose is True else self.label
        if shellib.interface == 'Tk':
            shellib.msg.config(font=('mono', 9, 'normal'))
        shellib.outputf(msg=string, head=heading)

    def animate(self):
        tdelta = .08

        for _ in range(4):
            Terminal.print_header()

            self.roll()
            
            Terminal.output('')
            self.draw_face()

            time.sleep(tdelta)
            Terminal.print_header()
            time.sleep(tdelta)

        Terminal.print_header()
        return self()
