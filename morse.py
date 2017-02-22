#!/usr/bin/env python3
"""
Read from command line args or stdin, converting to Morse code.
"""
import atexit
import getpass
import sys
import time

from cjh.letter import Letter
from cjh.misc import notebook
import easycat
from versatiledialogs.terminal import Terminal


REMARKS = """
    - figure out multitasking
    - there is a problem with some soundcards which necessitates very
      slow timing
    - add Tk
    + build it into the letter object"""

Terminal()
atexit.register(Terminal.unhide_cursor)
notebook(REMARKS)

def play_and_print(char):
    """
    write dots and dashes while also playing audible Morse code sounds
    """
    try:
        letter = Letter(char)
        easycat.write(Terminal.fx('bn', letter.morse + ' '))
        letter.play_morse()
    except KeyError:
        #make it flash
        time.sleep(.1)
        easycat.write(char)

def main():
    """
    main
    """
    Terminal.hide_cursor()
    sample = Letter(' ')
    Terminal.output('')
    Terminal.print_header('{} Hz, {} words per minute'.format(
        sample.hz, sample.wpm))
    Terminal.output('')
    Terminal.cursor_v(1)

    if len(sys.argv[1:]) > 0:
        easycat.write('    ')
        char_string = sys.argv[1].upper()
        for char in char_string:
            play_and_print(char)
    else:
        line_no = 1
        while True:
            try:
                try:  # Terminal.get_keypress()
                    line = getpass.getpass(prompt='%2d: ' % line_no)
                except KeyboardInterrupt:
                    Terminal.clear(1)
                    Terminal.cursor_v(1)
                    break

                easycat.write('\t')
                Terminal.cursor_v(1)
                for char in line:
                    #if char == ' ':
                    #    easycat.write('/ ')
                    #else:
                    play_and_print(char)
                Terminal.output('\n')
                line_no += 1
                #easycat.write('    ')
            except KeyboardInterrupt:
                break

    Terminal.output('\n\n\n' +
        '#  #  #'.center(Terminal.width()))
    Terminal.hrule()
    Terminal.output('')

if __name__ == '__main__':
    main()
    Terminal.start_app()
