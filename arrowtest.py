#!/usr/bin/env python3
#coding=utf8
"""
Detect pressing of the arrow keys (or h, j, k, l).
"""
from termcolor import colored, cprint

from cjh.misc import catch_help_flag, notebook
from colorful import color
import easycat
from versatiledialogs.terminal import Terminal

REMARKS = """
    - create get_keypress method for Tk
    + Move the function to versatiledialogs.terminal.Terminal

    * Alternatives to termcolor:
      - 'cjh.colorful' package
      - raw-coding the colors"""


notebook(REMARKS)
catch_help_flag(__doc__.strip())

def main():
    """
    Get a keypress and echo back the name of any arrow keys pressed.
    """
    try:
        Terminal.hide_cursor()
        Terminal.output('\n   |    (arrow keys)\n --+--\n   |')
        Terminal.cursor_v(1)

        while True:
            try:
                key_dict = {
                    'H': 'left',
                    'J': 'down',
                    'K': 'up',
                    'L': 'right'
                }

                whichway = Terminal.get_arrow_key()
                if whichway == chr(12):
                    Terminal.clear()
                    Terminal.output('\n\n')
                elif len(whichway) == 1:
                    whichway = key_dict.get(whichway.upper(), None)
                Terminal.clear(0)
                easycat.write('   |  ')
                Terminal.cursor_h(5)

                if whichway is not None:
                    out_str = colored(
                        whichway, 'white', 'on_red', attrs=['bold'])
                else:
                    out_str = ' ' * 4
                Terminal.output(out_str + '\r')

                Terminal.cursor_v(3)
                Terminal.cursor_h(3)

                
                if whichway == 'up':
                    cprint('|', 'yellow', 'on_blue')
                else:
                    Terminal.output('|')
                Terminal.cursor_h(1)
                if whichway == 'left':
                    easycat.write(colored('--', 'yellow', 'on_blue'))
                else:
                    easycat.write('--')
                easycat.write('+')
                if whichway == 'right':
                    cprint('--', 'yellow', 'on_blue')
                else:
                    Terminal.output('--')
                Terminal.cursor_h(3)
                if whichway == 'down':
                    cprint('|', 'yellow', 'on_blue')
                else:
                    Terminal.output('|')
                Terminal.cursor_v(1)

            # Fails when get_arrow_key() returns None
            except TypeError:
                pass

    except KeyboardInterrupt:
        pass
    finally:
        Terminal.output('\n')
        Terminal.unhide_cursor()

Terminal()
if __name__ == '__main__':
    main()
    Terminal.start_app()
