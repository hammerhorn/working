#!/usr/bin/env python
#coding=utf8
"""
Test & debug <class 'cjh.geometry.Graph'>.
"""
# Std Lib
import atexit

# Add-ons
from termcolor import colored

# Local
from cjh.maths.geometry import Graph
from cjh.misc import notebook
from versatiledialogs.config   import Config
from versatiledialogs.terminal import Terminal
from ranges import iter_zip
REMARKS = """
    - (0, 1) is not displaying correctly
    - improve the animation by not redrawing the whole screen each time
    * Swap colors"""
SHELL = Config().start_user_profile()
atexit.register(Terminal.unhide_cursor)

def main():
    plane = Graph(size=21, sh_obj=SHELL, skinfile='test.json')

    if SHELL.interface == 'Tk':
        SHELL.center_window(width_=600, height_=600)
        SHELL.msg.config(font=('courier'))
    elif SHELL.interface == 'term':
        Terminal.hide_cursor()

    def action(func, lines):
        func()
        SHELL.clear(plane.size + lines)

    SHELL.output(plane)
    pos_txt = ('Please press one> ', 'F', 'E', 'P')
    neg_txt = (' ', 'ill ', 'dit  ', 'lot ')
    prompt_list = []
    for p, n in iter_zip(pos_txt, neg_txt):
        prompt_list.extend([p, colored(n, attrs=['reverse'])])
    prompt = ''.join(prompt_list)

    while True:
        pressed = Terminal.get_keypress(prompt)
        cmd_dict = {
            'f': lambda: action(lambda: plane.fill(plane.prompt_color()), 6),
            'e': lambda: action(plane.view_edit, 11),
            'p': plane.add_polynomial
        }
        cmd_dict.get(pressed.lower(), lambda: 0)()
        SHELL.output(plane)

if __name__ == '__main__':
    notebook(REMARKS)
    main()
    SHELL.start_app()
