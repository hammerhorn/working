#!/usr/bin/env python
#coding='utf-8'
"""
New program
"""
import argparse

import Tkinter as tk

from versatiledialogs.config import Config
from versatiledialogs.tk_template import TkTemplate

__author__ = 'Chris Horn <hammerhorn@gmail.com>'

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    if __name__ == '__main__':
        args = parser.parse_args()
    else: args = None
    return args


def save_prefs(var1, var2, var3):
    CONFIG.write_to_config_file(shell=var1, editor=var2, terminal=var3)
    SHELL.report_filesave('versatiledialogs/config.json')

##########
#  DATA  #
##########
ARGS = _parse_args()
SHELL = TkTemplate()
CONFIG = Config()
SHELL.main_window.title("cjh Settings Editor")
SHELL.center_window(height_=200)
SHELL.msg.config(width=200, font=('serif',10, 'bold', 'italic'))
SHELL.msgtxt.set('Customize your settings')
variable1 = tk.StringVar(SHELL.main_window)
variable1.set('term')
w1 = tk.OptionMenu(
    SHELL.main_window, variable1, "term", "Tk", "dialog", "zenity", "wx")
w1.pack()

variable2 = tk.StringVar(SHELL.main_window)
variable2.set("emacs")
w2 = tk.OptionMenu(
    SHELL.main_window, variable2, "./tk_text", "gedit", "scite", "emacs", "vim", "nano")
w2.pack()

variable3 = tk.StringVar(SHELL.main_window)
variable3.set("terminal")
w3 = tk.OptionMenu(
    SHELL.main_window, variable3, "terminator -x", "gnome-terminal -x", "xterm -x")
w3.pack()

button = tk.Button(SHELL.main_window, text="Save preferences", command=lambda: save_prefs(variable1.get(), variable2.get(), variable3.get()))
button.pack(pady=15)

##########
#  MAIN  #
##########
def main():
    """
    Main function
    """
    SHELL.main_window.mainloop()

if __name__ == '__main__':
    main()
