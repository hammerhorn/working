#!/usr/bin/env python3
#coding=utf8
"""
detect pressing the arrowkeys
"""
from cjh.misc import catch_help_flag, notebook
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

REMARKS = '    - Move the function to versatiledialogs.terminal.Terminal'
notebook(REMARKS)

SHELL = Config().start_user_profile()
catch_help_flag(__doc__)

CODE_DICT = {
    'A': 'up',
    'B': 'down',
    'C': 'right',
    'D': 'left'
}


def get_arrow_key():
    """
    distinguish between arrow keys being pressed
    """
    direction = None
    pressed = Terminal.get_keypress()
    if pressed == chr(27):
        pressed = Terminal.get_keypress()
        if pressed == '[':
            pressed = Terminal.get_keypress()
            direction = CODE_DICT.get(pressed, None)
    return direction


def main():
    """
    Get a keypress and echo back the name of any arrowkeys pressed.
    """
    try:
        while True:
            try:
                Terminal.output(''.join(['\b', get_arrow_key()]))

            # Fails when get_arrow_key() returns None
            except TypeError:
                pass
    except KeyboardInterrupt:
        pass

Terminal()
if __name__ == '__main__':
    main()
    SHELL.start_app()
