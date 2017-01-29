#!/usr/bin/env python
#coding=utf8
"""
detect pressing the arrowkeys
"""
from cjh.misc import catch_help_flag, notebook
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal
Terminal()
SHELL = Config().start_user_profile()

def get_arrow_key():
    pressed = Terminal.get_keypress()
    if pressed == chr(27):
        pressed = Terminal.get_keypress()
        if pressed == '[':
            pressed = Terminal.get_keypress()
            if pressed == 'A':
                direction = 'up'
            elif pressed == 'B':
                direction = 'down'
            elif pressed == 'C':
                direction = 'right'
            elif pressed == 'D':
                direction = 'left'
            else:
                direction = None
        else:
            direction = None
    else:
        direction = None
    return direction


def main():
    """
    Get a keypress and echo back the name of any arrowkeys pressed.
    """
    try:
        while True:
            try:
                Terminal.output('\b' + get_arrow_key())
            except TypeError:
                pass
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    catch_help_flag(__doc__)
    notebook('    - Move the function to versatiledialogs.terminal.Terminal')
    main()
    SHELL.start_app()
