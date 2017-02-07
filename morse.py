#!/usr/bin/env python3
"""
Read from command line args or stdin, converting to Morse code.
"""
import sys
import time

from cjh.letter import Letter

import easycat
from versatiledialogs.terminal import Terminal


REMARKS = """
    - figure out multitasking
    - add Tk
    + build it into the letter object"""

Terminal()

def play_and_print(char):
    """
    write dots and dashes while also playing audible Morse code sounds
    """
    try:
        letter = Letter(char)
        easycat.write(letter.morse + ' ')
        letter.play_morse()
    except KeyError:
        #make it flash
        time.sleep(.1)
        easycat.write(char)

def main():
    """
    main
    """
    sample = Letter(' ')
    Terminal.output('({} Hz, {} words per minute)'.format(sample.hz, sample.wpm))
    if len(sys.argv[1:]) > 0:
        char_string = sys.argv[1].upper()
        for char in char_string:
            play_and_print(char)
    else:
        while True:
            char = Terminal.get_keypress()
            play_and_print(char)
    Terminal.output('')

if __name__ == '__main__':
    main()
    Terminal.start_app()
