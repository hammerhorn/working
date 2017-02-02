#!/usr/bin/env python3
"""
Accepts a valid color name (e.g., 'red') or hex string (e.g., '#FF0000'),
and the window becomes that color.
"""
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

from versatiledialogs.tk_template import TkTemplate

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

SHELL = TkTemplate()


def change_colour(name_or_hex, pane):
    """
    Takes color name or hex color as an argument,
    and turns the window that color.
    """
    try:
        SHELL.main_window.config(bg=name_or_hex)
        pane.config(bg=name_or_hex)

    #build this into shell
    except tk.TclError:
        tkMessageBox.showerror('Color error', 'That color is unknown.')

def main():
    """
    Create a Tk window and adjust the background color according to user input.
    """
    SHELL.main_window.title('Colors by Hex or Name')

    #build this in
    SHELL.msg.destroy()

    pane = tk.Frame(SHELL.main_window)
    entry = tk.Entry(pane, width=15, font=('sans', 12))
    bottom = tk.Button(
        pane, text="Change Color", command=lambda: change_colour(
            entry.get(), pane))
    entry.pack(side=tk.LEFT)
    bottom.pack(side=tk.RIGHT)
    pane.pack(fill=tk.X, side=tk.BOTTOM, pady=10, padx=10)

    TkTemplate.center_window(height_=50, width_=300)

if __name__ == '__main__':
    main()
    SHELL.start_app()


