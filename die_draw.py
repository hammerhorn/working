#!/usr/bin/env python3
#coding=utf8
"""
DRAW DIE - Reads an int from the command line or input prompt and draws the die.
Works with bash or Tk.
"""
import sys

from cjh.tablegames.die import Die
from cjh.misc import catch_help_flag
from cjh.music import Pitch

from versatiledialogs.config import Config

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

MAX_SIDES = 6
SHELL = Config().start_user_profile()

if SHELL.interface in ('Tk', 'wx'):
    SHELL.center_window(height_=100, width_=150)

help_str = '\n'.join(('usage: %s [VALUE]' % sys.argv[0],
                   __doc__,
                   '  -h, --help\t\tshow this help message and exit'))
catch_help_flag(help_str)

def main():
    """
    Get an int from the pipeline or from user input, and draw the die.
    """
    die = Die(MAX_SIDES)

    if __name__ == '__main__':
        valid_input = False
        while valid_input is False:
            try:
                die.value = int(SHELL.arg("(1-{})".format(die.sides)))
                valid_input = True
                while MAX_SIDES < die.value < 1:
                    die.value = int(SHELL.input(" (1-{}): ".format(die.sides)))
            except ValueError:
                if len(sys.argv[1:]) == 0:
                    continue
                else:
                    Pitch('A', 4).play()
                    SHELL.message('ERROR--Invalid argument')
                    sys.exit()

        die.draw_face(shellib=SHELL)


if __name__ == '__main__':
    main()
    SHELL.start_app()
