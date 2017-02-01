#!/usr/bin/env python
#coding=utf8
r"""
Versatile Dialogs

Contains modules for:
    - providing equivalent dialogs in the following modes: term, Tk, dialog,
      zenity, SL4A, wx, and html, which will run under Python 2 or Python 3 on
      Linux, qpython for android, and Windows.


This package uses the 'config.json' file and the './prefs.py' script to control
configuration.

Config Attributes:
       shell - 'term', 'dialog', 'zenity', 'SL4A', 'Tk', 'wx', or 'html'
    terminal - name of terminal emulator, e.g., 'terminator -x '
      editor - default text editor, e.g., emacs, vi, gedit, ...
    language - 'EN' and 'EO' will be supported
     browser - default web browser

Examples:
    ./prefs.py              Lists all keys and their values
    ./prefs.py -s term      Sets the default shell to 'term'
    ./prefs.py -l en        Sets the default language to English
    ./prefs.py -b \?        Echos back the name of the default web browser
"""

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'
