#!/usr/bin/env python3
#coding=utf8
"""
Comparison of Truecolor terminal color and Colortrans conversion script
Run this script to see if your terminal is Truecolor compatible.
"""
import atexit
import sys
import time

from colorful import color
import easycat
from ranges import gen_range
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


REMARKS = """
    * revise with a function or something; refactor the motherfucker"""

atexit.register(Terminal.unhide_cursor)
Terminal()

DELTA_T = 0.005
OUT_STR1, OUT_STR2 = ' TRUECOLOR', 'COLORTRANS'


def side_by_side(red, green, blue):
    """
    Show Truecolor and Colortrans methods on your terminal.
    """
    Terminal.cursor_v(6)
    hexcolor = color.color_dec_to_hex(red, green, blue)
    culler = color.Color(hexcolor, 'hex')
    Terminal.output(culler.__str__() + '\n')

    def position_and_color(txt_str, tc_bool):
        easycat.write('  ')
        color.write(
            16, 'ansi', hexcolor, 'hex', txt_str, truecolor=tc_bool)
        Terminal.output('')

    position_and_color(OUT_STR1, True)
    position_and_color(OUT_STR2, False)    
    time.sleep(DELTA_T)


def main():
    """
    The words 'TRUECOLOR' and 'COLORTRANS' both appear as shifting spectra on a
    terminal that supports Truecolor escapes.
    """
    Terminal.hide_cursor()
    Terminal.output(''.join([
        '\nANSI escape:\nRGB hexcode\n\n', OUT_STR1,
        '\n', OUT_STR2, '\n' * 4]))
    time.sleep(DELTA_T * 4)
    Terminal.cursor_v(4)
    try:
        #Fade from black to red
        for val in gen_range(256):
            side_by_side(val, 0, 0)
        Terminal.wait()
        Terminal.hide_cursor()

        for _ in gen_range(50):
            #Fade from red to yellow
            for val in gen_range(256):
                side_by_side(255, val, 0)
            Terminal.wait()
            Terminal.hide_cursor()

            #Fade from yellow to green
            for val in gen_range(256):
                side_by_side(255 - val, 255, 0)
            Terminal.wait()
            Terminal.hide_cursor()

            #Fade from green to cyan
            for val in gen_range(256):
                side_by_side(0, 255, val)
            Terminal.wait()
            Terminal.hide_cursor()

            #Fade from cyan to blue
            for val in gen_range(256):
                side_by_side(0, 255 - val, 255)
            Terminal.wait()
            Terminal.hide_cursor()

            #Fade from blue to magenta
            for val in gen_range(256):
                side_by_side(val, 0, 255)
            Terminal.wait()
            Terminal.hide_cursor()

            #Fade from magenta to red
            for val in gen_range(256):
                side_by_side(255, 0, 255 - val)
            Terminal.wait()
            Terminal.hide_cursor()

        Terminal.output('')
    except KeyboardInterrupt:
        Terminal.clear(0)

if __name__ == '__main__':
    main()
    Terminal.start_app()
