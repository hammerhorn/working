#!/usr/bin/env python3
#coding=utf8
"""
Accepts a valid color name (e.g., 'red') or hex string (e.g., '#FF0000'), and
the window becomes that color.

adapted from:
<http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/>
    and
<http://www.zombieprototypes.com/?p=210>

(web.py has been removed, so this is now compatible with Python 3)
"""
import argparse
import os
import sys

try:
    import Tkinter as tk
    import tkMessageBox
except ImportError:
    try:
        import tkinter as tk
        import tkinter.messagebox as tkMessageBox
    except ImportError:
        sys.exit('Tk could not be loaded.  Ending program.')

from cjh.misc       import fahr_to_kelvins, notebook
from colorful       import color
from colorful.color import Color  # color_dec_to_hex
from fiziko.waves   import kelvin_to_rgb
from versatiledialogs.config      import Config
from versatiledialogs.html_sh     import HtmlShell
from versatiledialogs.terminal    import Terminal
from versatiledialogs.tk_template import TkTemplate


REMARKS = """
    - Intensity must be factored in
    + make Kelvin the default for all shells
    + ask config file for default web browser
    + This must be combined with tk_bbody
    + should contain colored text for bash
    + should contain ANSI colors for non-Truecolor terminals

    * should contain colored text for w3m
    * readline?"""

notebook(REMARKS)

def _parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shell', '-s', type=str)
    parser.add_argument('--html', '-H', action='store_true')
    parser.add_argument(
        '-C', action='store_true', help="read developer's comments")
    parser.add_argument(
        '-F', action='store_true', help='accept input in Fahr')
    parser.add_argument('-T', action='store_true', help='Truecolor')
    return parser.parse_args() if __name__ == '__main__' else None

ARGS = _parse_args()
CONFIG = Config()
SHELL = CONFIG.launch_selected_shell(ARGS.shell) if\
        ARGS is not None and ARGS.shell is not None else\
        CONFIG.start_user_profile()

if ARGS is not None and ARGS.html is True:
    FILENAME = 'results.html'
    BROWSER = CONFIG.config_dict.get('browser')

def main():
    """
    Main function
    """
    if ARGS.html is True:
        html_obj = HtmlShell(
            title='Kelvin -> Hue',
            location=FILENAME)

        html_obj.output(
            'Welcome!  Enter a temperature into your terminal to begin.')

    if SHELL == 'term':

        while True:
            try:
                Terminal.output('')

                def get_kelvins():
                    """
                    Get the temperature from the user and return it in
                    kelvins.
                    """
                    if ARGS.F is True:
                        return fahr_to_kelvins(
                            float(Terminal.input('temperature? (°F) ')))
                    else:
                        return float(Terminal.input('temperature? (K) '))

                kelvins = get_kelvins()
                red, green, blue = kelvin_to_rgb(kelvins)
                bgcolor = Color.dec_to_hex(red, green, blue)
                title = '{}, {}, {} ({}K)'.format(red, green, blue, kelvins)
                color_str = "#000000"
                _heading = '{:,.5}K'.format(kelvins)  # unused?

                if ARGS.html is True:
                    html_obj = HtmlShell(
                        title, FILENAME, bgcolor, color_str, dont_open=True)
                    html_obj.output(color_str)
                Terminal.output(Terminal.fx('bn', color.write(
                    '#000000', 'hex', bgcolor, 'hex', bgcolor + ' ' * 33,
                    truecolor=ARGS.T, get_str=True)), heading=_heading)
            except KeyboardInterrupt:
                Terminal.clear(0)
                if ARGS.html is True:
                    Terminal.clear(1)
                    Terminal.output("\r\nYou may now close '{}/{}'.\n".format(
                        os.getcwd(), FILENAME))
                break

    elif SHELL == 'Tk':
        def change_color(kelvins):
            """
            Takes color name or hex color as an argument,
            and turns the Tk window that color.
            """
            red, green, blue = kelvin_to_rgb(kelvins)
            bgcolor = Color.dec_to_hex(red, green, blue)
            title = '{}, {}, {} ({}K)'.format(red, green, blue, kelvins)
            color_str = "#000000"
            heading = '{:,.5}K'.format(kelvins)
            if ARGS.html is True:
                html_sh = HtmlShell(
                    title, FILENAME, bgcolor, color_str, dont_open=True)
                html_sh.output(heading)
            try:
                SHELL.main_window.config(bg=bgcolor)
                pane.config(bg=bgcolor)
            #build this into shell
            except (tk.TclError, ValueError):
                tkMessageBox.showerror('Color error', 'That color is unknown.')

        SHELL.main_window.title('Kelvin -> Hue')
        SHELL.msg.destroy()

        pane = tk.Frame(SHELL.main_window)
        entry = tk.Entry(pane, width=15, font=('sans', 12))
        button = tk.Button(
            pane, text='Color temp. (K)', command=lambda: change_color(
                float(entry.get())))

        entry.pack(side=tk.LEFT)
        button.pack(side=tk.RIGHT)
        pane.pack(fill=tk.X, side=tk.TOP, pady=10, padx=10)

        TkTemplate.center_window(height_=200, width_=300)


if __name__ == '__main__':
    main()
    SHELL.start_app()
