#!/usr/bin/env python3
#coding=utf8
"""
detect pressing the arrowkeys
"""
import sys
from cjh.misc import catch_help_flag, notebook
import easycat
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

REMARKS = """
    - create get_keypress method for Tk
    + Move the function to versatiledialogs.terminal.Terminal"""


notebook(REMARKS)

SHELL = Config().start_user_profile()
catch_help_flag(__doc__)

def main():
    """
    Get a keypress and echo back the name of any arrowkeys pressed.
    """
    try:
        Terminal.hide_cursor()
        Terminal.output(' *** Press an arrow key ***')
        while True:
            try:
                whichway = Terminal.get_arrow_key(arrows_only=True)
                Terminal.clear(0)
                easycat.write(whichway)

            # Fails when get_arrow_key() returns None
            except TypeError:
                pass

    except KeyboardInterrupt:
        pass
    finally:
        Terminal.output('')
        Terminal.unhide_cursor()

Terminal()
if __name__ == '__main__':
    main()
    SHELL.start_app()
