#!/usr/bin/env python
#coding=utf8
"""
Test & debug <class 'cjh.geometry.Graph'>.
"""
import atexit
#import sys

from termcolor import colored

from cjh.maths.geometry import Graph
from cjh.misc import notebook

from versatiledialogs.config   import Config
from versatiledialogs.terminal import Terminal

REMARKS = """
    - (0, 1) is not displaying correctly
    * Swap colors"""

SHELL = Config().start_user_profile()
atexit.register(Terminal.unhide_cursor)
def main():
    g1 = Graph(size=21, sh_obj=SHELL, skinfile='test.json')
    if SHELL.interface == 'Tk':
        SHELL.center_window(width_=600, height_=600)
        SHELL.msg.config(font=('courier'))

    SHELL.output(g1)
#    if SHELL.interface == 'term':
    Terminal.hide_cursor()
    while True:
        pressed = Terminal.get_keypress(
            'Please press one> ' + colored(' ', attrs=['reverse']) + 'F' + colored('ill  ', attrs=['reverse']) + 'E' +\
            colored('dit  ', attrs=['reverse']) + 'P' + colored('lot ', attrs=['reverse']))
        if pressed in 'Ff':
            color = g1.prompt_color()
            g1.fill(color)
            SHELL.clear(g1.size + 6)

        elif pressed in 'Ee':
            g1.view_edit()
            SHELL.clear(g1.size +11)

        elif pressed in 'Pp':
            g1.add_polynomial()
        SHELL.output(g1)

if __name__ == '__main__':
    notebook(REMARKS)
    main()
    SHELL.start_app()
