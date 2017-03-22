#!/usr/bin/env python3
#coding=utf8
"""
Comparison of:

    * Truecolor RGB escape sequences for the terminal and
    * Micah Elliot's 'colortrans' module for color conversion.

Run this script to see if your terminal supports Truecolor sequences.
"""
import atexit
# import sys
import time

from colorful import color
import easycat
from cjh.misc import catch_help_flag, notebook
from ranges import gen_range
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


REMARKS = """
    * revise with a function or something; refactor the motherfucker"""

atexit.register(Terminal.unhide_cursor)
Terminal()

DELTA_T = 0.00125
OUT_STR1, OUT_STR2 = ' TRUECOLOR', 'COLORTRANS'


def side_by_side(red, green, blue):
    """
    Show Truecolor and Colortrans methods on your terminal.
    """
    Terminal.cursor_v(6)
    hexcolor = color.Color.dec_to_hex(red, green, blue)
    culler = color.Color(hexcolor, 'hex')
    Terminal.output(culler.__str__() + '\n')

    def position_and_color(txt_str, tc_bool):
        """indent & print colored text followed by a newline"""
        easycat.write('  ')
        color.c_write(
            16, 'ansi', hexcolor, 'hex', txt_str, truecolor=tc_bool)
        Terminal.output('')

    position_and_color(OUT_STR1, True)
    position_and_color(OUT_STR2, False)
    time.sleep(DELTA_T)

def wait_and_hide():
    """wait for user acknowlegement and hide cursor"""
    Terminal.wait()
    Terminal.hide_cursor()

def main():
    """
    On a terminal that supports Truecolor escapes, the words 'TRUECOLOR'
    and 'COLORTRANS' both appear as shifting spectra.
    """
    Terminal.hide_cursor()
    #Terminal.output(''.join((
    #    '\nANSI escape:\nRGB hexcode\n\n',
    #    OUT_STR1,
    #    '\n',
    #    OUT_STR2,
    #    '\n' * 4)))
    Terminal.output('\nANSI escape:\nRGB hexcode\n\n{}\n{}\n\n\n\n'.format(OUT_STR1, OUT_STR2))
    time.sleep(DELTA_T * 4)
    Terminal.cursor_v(4)
    try:
        #Fade from black to red
        for val in gen_range(256):
            side_by_side(val, 0, 0)
        #wait_and_hide()

        for _ in gen_range(50):
            #Fade from red to yellow
            for val in gen_range(256):
                side_by_side(255, val, 0)
            #wait_and_hide()

            #Fade from yellow to green
            for val in gen_range(256):
                side_by_side(255 - val, 255, 0)
            #wait_and_hide()

            #Fade from green to cyan
            for val in gen_range(256):
                side_by_side(0, 255, val)
            #wait_and_hide()

            #Fade from cyan to blue
            for val in gen_range(256):
                side_by_side(0, 255 - val, 255)
            #wait_and_hide()

            #Fade from blue to magenta
            for val in gen_range(256):
                side_by_side(val, 0, 255)
            #wait_and_hide()

            #Fade from magenta to red
            for val in gen_range(256):
                side_by_side(255, 0, 255 - val)
            #wait_and_hide()

        Terminal.output('')
    except KeyboardInterrupt:
        Terminal.clear(0)
        Terminal.output('')

if __name__ == '__main__':
    notebook(REMARKS)
    catch_help_flag(help_str=__doc__.rstrip())
    main()
    Terminal.start_app()
