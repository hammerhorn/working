#!/usr/bin/env python
#coding='utf-8'
"""
New program
"""
import argparse

import Tkinter as tk

from cjh.misc import notebook
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
    return parser.parse_args() if __name__ == '__main__' else None


def save_prefs(var1, var2, var3):
    """
    write all changes to config.json
    """
    CONFIG.write_to_config_file(shell=var1, editor=var2, terminal=var3)
    SHELL.report_filesave('versatiledialogs/config.json', fast=True)

##########
#  DATA  #
##########
REMARKS = """
    - add a 'Refresh' button"""
notebook(REMARKS)

ARGS = _parse_args()
SHELL = TkTemplate()
CONFIG = Config()
SHELL.main_window.title("cjh Settings Editor")
SHELL.center_window(height_=200)
SHELL.msg.config(width=200, font=('serif', 10, 'bold', 'italic'))
SHELL.msgtxt.set('Customize your settings')

VARIABLE1 = tk.StringVar(SHELL.main_window)
VARIABLE1.set(CONFIG.config_dict['shell'])
W1 = tk.OptionMenu(
    SHELL.main_window, VARIABLE1, 'term', 'Tk', 'dialog', 'zenity', 'wx')
W1.pack()

VARIABLE2 = tk.StringVar(SHELL.main_window)
VARIABLE2.set(CONFIG.config_dict['editor'])
W2 = tk.OptionMenu(
    SHELL.main_window, VARIABLE2, "./tk_text", "gedit", "scite", "emacs", "vim", "nano")
W2.pack()

VARIABLE3 = tk.StringVar(SHELL.main_window)
VARIABLE3.set(CONFIG.config_dict['terminal'])
W3 = tk.OptionMenu(
    SHELL.main_window, VARIABLE3, "terminator -x", "gnome-terminal -x", "xterm -x")
W3.pack()

BUTTON = tk.Button(
    SHELL.main_window, text="Save preferences", command=lambda: save_prefs(
        VARIABLE1.get(), VARIABLE2.get(), VARIABLE3.get()))
BUTTON.pack(pady=15)

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
