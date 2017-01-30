#!/usr/bin/env python
#coding=utf8
"""
EMR HZ-TO-COLOR -

User inputs a frequency (e.g., 5e14 is in the visible light range).
The program outputs a description of EM radiation at the given frequency.

Current version is based on this:
<https://academo.org/demos/wavelength-to-colour-relationship/>
"""
import argparse
import sys

try:
    from Tkinter import TclError
except ImportError:
    from tkinter import TclError

from colorful.color import color_dec_to_hex, nm_to_rgb, write
from cjh import misc
from cjh.fiziko.scalars import Unit
from cjh.fiziko.waves import EMWave

from versatiledialogs.config import Config

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - readline!
    + move certain functions to the class file
    - its tricky trying to terminate the program under 'dialog' interface
    + colored text in bash-mode w/ Linux
    + wavelength output does not work
    + Works well with bash, dialog, and Tk.

    * adjust size of window corresponding to the amount of text
    * unite with tk_bbody
    * Temperature to color would be the best?"""

def _parse_args():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-s', '--shell', type=str, help='bash, dialog, sh, Tk, wx, zenity')
    parser.add_argument(
        '-C', action='store_true', help="view developer's comments")
    if __name__ == '__main__':
        args = parser.parse_args()
    else:
        args = None
    return args

ARGS = _parse_args()
CONFIG = Config()
if ARGS is not None and ARGS.shell is not None:
    SHELL = CONFIG.launch_selected_shell(ARGS.shell)
else:
    SHELL = CONFIG.start_user_profile()

if ARGS is not None and ARGS.C:
    misc.notebook(REMARKS)


def main():
    """
    docstring
    """
    SHELL.welcome('EMWaves - demonstration of my EMWave class')
    hertz = None

    if SHELL.interface == 'Tk':
        SHELL.msg.config(
            bg='black', fg='white', width=200, font=('times', 15))#, 'bold'))
        SHELL.main_window.config(bg='black')
        SHELL.center_window(height_=200, width_=300)
        SHELL.main_window.title('EM Radiation (Hz)')

    while True:
        try:
            try:
                freq_string = SHELL.input('Frequency in Hz: ')
                hertz = float(freq_string)
            except ValueError:
                continue
            except (AttributeError, KeyboardInterrupt):
                if SHELL.interface == 'term':
                    SHELL.clear(0)
                sys.exit()

            emw = EMWave(hertz, Unit('Hz'))

            if SHELL.interface == 'term':
                red, green, blue = nm_to_rgb(emw.wlength.nanometers)
                if red + green + blue == 0.0:
                    write(7, 'ansi', 0, 'ansi', emw.__str__() + '\n')
                else:
                    write(
                        color_dec_to_hex(red, green, blue), 'hex', 16, 'ansi',
                        emw.__str__())
                SHELL.output('\n')

        except KeyboardInterrupt:
            SHELL.clear(0)

        if SHELL.interface == 'Tk':
            bgcolor = str(emw).split()[0]
            SHELL.main_window.title(emw.label)
            fgcolor = 'black'

            rgb_tuple = nm_to_rgb(emw.wlength.nanometers)
            bgcolor = color_dec_to_hex(*rgb_tuple)

            if sum(rgb_tuple) <= 160:
                fgcolor = 'white'
            try:
                SHELL.main_window.config(bg=bgcolor)
                SHELL.msg.config(bg=bgcolor, fg=fgcolor)
                SHELL.output(emw.__str__())
            except TclError:
                pass

if __name__ == '__main__':
    main()
    SHELL.start_app()
