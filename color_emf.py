#!/usr/bin/env python3
#coding=utf8
"""
EMR HZ-TO-COLOR

User inputs a frequency (e.g., 5e14 is in the visible light range).
The program outputs a description of EM radiation at the given frequency.

Current version is based on this:
<http://academo.org/demos/wavelength-to-colour-relationship/>
"""
import argparse
import sys

#mod_name = 'Tkinter' if sys.version_info == 2 else 'tkinter'
#exec('from {} import TclError'.format(mod_name))

try:
    from Tkinter import TclError
except ImportError:
    from tkinter import TclError  # pylint: disable=E0401

from cjh.misc import notebook
from colorful.color import Color, nm_to_rgb, c_write
from fiziko.scalars import Unit
from fiziko.waves import EMWave
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
    return parser.parse_args() if __name__ == '__main__' else None

ARGS = _parse_args()
CONFIG = Config()
SHELL = CONFIG.launch_selected_shell(ARGS.shell)\
        if ARGS is not None and ARGS.shell is not None else CONFIG.start_user_profile()

notebook(REMARKS)

def main():
    """
    docstring
    """
    SHELL.welcome(description='EMWaves - demonstration of my EMWave class')
    hertz = None

    if SHELL == 'Tk':
        SHELL.msg.config(
            bg='black', fg='white', width=200, font=('times', 15))
        SHELL.main_window.config(bg='black')
        SHELL.center_window(height_=200, width_=300)
        SHELL.main_window.title('EM Radiation (Hz)')
    if SHELL == 'term':
        SHELL.output('')
    while True:
        try:
            try:
                freq_string = SHELL.input('Frequency in Hz: ')
                if SHELL == 'term':
                    SHELL.clear(4)
                hertz = float(freq_string)
            except ValueError:
                continue
            except (AttributeError, KeyboardInterrupt):
                if SHELL == 'term':
                    SHELL.clear(0)
                sys.exit()

            emw = EMWave(hertz, Unit('Hz'))

            if SHELL == 'term':
                red, green, blue = nm_to_rgb(emw.wlength.nanometers)
                if red + green + blue == 0.0:
                    c_write(7, 'ansi', 0, 'ansi', emw.__str__())  # + '\n')
                else:
                    c_write(
                        Color.dec_to_hex(red, green, blue), 'hex', 16, 'ansi',
                        emw.__str__())
                SHELL.output('\n')

        except KeyboardInterrupt:
            SHELL.clear(0)

        if SHELL == 'Tk':
            bgcolor = str(emw).split()[0]
            SHELL.main_window.title(emw.label)
            fgcolor = 'black'

            rgb_tuple = nm_to_rgb(emw.wlength.nanometers)
            bgcolor = Color.dec_to_hex(*rgb_tuple)

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
