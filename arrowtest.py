#!/usr/bin/env python
#coding=utf8
"""
detect pressing the arrowkeys
"""
from cjh.misc import catch_help_flag, notebook
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

REMARKS = '    - Move the function to versatiledialogs.terminal.Terminal'

Terminal()
SHELL = Config().start_user_profile()

def get_arrow_key():
    """
    distinguish between arrow keys being pressed
    """
    direction = None
    pressed = Terminal.get_keypress()
    if pressed == chr(27):
        pressed = Terminal.get_keypress()
        if pressed == '[':

            code_dict = {
                'A': 'up',
                'B': 'down',
                'C': 'right',
                'D': 'left'
            }

            pressed = Terminal.get_keypress()
            direction = code_dict.get(pressed, None)
    return direction
           

def main():
    """
    Get a keypress and echo back the name of any arrowkeys pressed.
    """
    try:
        while True:
            try:
                Terminal.output('\b' + get_arrow_key())

            # Fails when get_arrow_key() returns None
            except TypeError:
                pass
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    catch_help_flag(__doc__)
    notebook(REMARKS)
    main()
    SHELL.start_app()
