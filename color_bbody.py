#!/usr/bin/env python
#coding=utf8
"""
Accepts a valid color name (e.g., 'red') or hex string (e.g., '#FF0000'), and
the window becomes that color.

adapted from:
<http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/>
    and
<http://www.zombieprototypes.com/?p=210>

python 2 only because it uses web.py
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

from colorful       import color
from colorful.color import color_dec_to_hex
from cjh.misc       import fahr_to_kelvins, notebook
from fiziko.waves   import kelvin_to_rgb

from versatiledialogs.config      import Config
if sys.version_info.major == 2:
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
    args = parser.parse_args() if __name__ == '__main__' else None
    return args

ARGS = _parse_args()
if __name__ == '__main__':
    notebook(REMARKS)

FILENAME = 'results.html'
CONFIG = Config()

if ARGS is not None and ARGS.shell is not None:
    SHELL = CONFIG.launch_selected_shell(ARGS.shell)
else:
    SHELL = CONFIG.start_user_profile()

BROWSER = CONFIG.config_dict.get('browser')


def main():
    """
    Main function
    """
    if ARGS.html is True:
        html_obj = HtmlShell(
            title='Kelvin -> Hue',
            location=FILENAME)  #,
            # heading='Welcome!')  # ,
            # content=
        html_obj.output(
            'Welcome!  Enter a temperature into your terminal to begin.')

        html_obj.open_file_in_browser(BROWSER)

    if SHELL.interface == 'term':
#       Terminal.output('\nWelcome.')
#       Terminal.notify('This script requires a Truecolor-compatible terminal
# (xterm, gnome-terminal, konsole, etc....) for the full effect.')

        while True:
            try:
                Terminal.output('')
                if ARGS.F is True:
                    fahr = float(Terminal.input('temperature? (°F) '))
                    kelvins = fahr_to_kelvins(fahr)
                else:
                    kelvins = float(Terminal.input('temperature? (K) '))

                color_tuple = kelvin_to_rgb(kelvins)
                red, green, blue = color_tuple
                bgcolor = color_dec_to_hex(red, green, blue)
                title = '{}, {}, {} ({}K)'.format(red, green, blue, kelvins)
                color_str = "#000000"
                _heading = '{:,.5}K'.format(kelvins)  # unused?
                if ARGS.html is True:
                    html_obj = HtmlShell(
                        title, FILENAME, bgcolor, color_str)
                        # , heading, bgcolor)
                    html_obj.output(color_str)
                #Terminal.output('\x1b[48;5;0;38;2;{};{};{}m{}\x1b[0m'.format(
                #    red, green, blue, Terminal.fx('bn', bgcolor)))
                if ARGS.T is True:
                    Terminal.output(Terminal.fx('bn', color.write(
                        '#000000', 'hex', bgcolor, 'hex', bgcolor + ' ' * 33,
                        truecolor=True, get_str=True)), heading=_heading)
                else:
                    Terminal.output(Terminal.fx('bn', color.write(
                        '#000000', 'hex', bgcolor, 'hex', bgcolor + ' ' * 33,
                        truecolor=False, get_str=True)), heading=_heading)
                #Terminal.output('')
            except KeyboardInterrupt:
                Terminal.clear(0)
                if ARGS.html is True:
                    Terminal.clear(1)
                    Terminal.output("\r\nYou may now close '{}/{}'.\n".format(
                        os.getcwd(), FILENAME))
                break
    elif SHELL.interface == 'Tk':
        def change_color(kelvins):
            """
            Takes color name or hex color as an argument,
            and turns the Tk window that color.
            """
            color_tuple = kelvin_to_rgb(kelvins)
            red, green, blue = color_tuple
            bgcolor = color_dec_to_hex(red, green, blue)
            title = '{}, {}, {} ({}K)'.format(red, green, blue, kelvins)
            color_str = "#000000"
            heading = '{:,.5}K'.format(kelvins)
            if ARGS.html is True:
                html_sh = HtmlShell(
                    title, FILENAME, bgcolor, color_str)
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

#        def get_color():
#            kelvins = float(ENTRY.get())
#            #print '"' + ENTRY.get() + '"'
#            #sys.exit()
#            red, green, blue = kelvin_to_rgb(kelvins)
#            return color_dec_to_hex(red, green, blue)

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
