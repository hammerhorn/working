#!/usr/bin/env python3
#coding=utf8
"""
detect pressing the arrowkeys
"""
from cjh.misc import catch_help_flag, notebook
import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

REMARKS = """
    + Move the function to versatiledialogs.terminal.Terminal
    - create get_keypress method for Tk"""

notebook(REMARKS)

SHELL = Config().start_user_profile()
catch_help_flag(__doc__)

def main():
    """
    Get a keypress and echo back the name of any arrowkeys pressed.
    """
    try:
        while True:
            try:
                whichway = Terminal.get_arrow_key()
               # easycat.write('\b')
                Terminal.clear(0)
                easycat.write(whichway)
                #
            # Fails when get_arrow_key() returns None
            except TypeError:
                pass
    except KeyboardInterrupt:
        pass

Terminal()
if __name__ == '__main__':
    main()
    SHELL.start_app()
