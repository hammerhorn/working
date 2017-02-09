#!/usr/bin/env python3
#coding=utf8
"""
An attractive clock for your terminal.

Depends: toilet; bash, dialog, or Tk
"""
# Std Lib
import datetime
import random
import time

# Add-ons
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

# Local
from cjh.misc import catch_help_flag, notebook
from ttyfun.unix import Figlet
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


##########
#  DATA  #
##########
Terminal()
CONFIG = Config()
SHELL = CONFIG.start_user_profile()
LANG = CONFIG.get_lang_key()
MONTH_DICT = {
    'January': 'januaro',
    'February': 'februaro',
    'March': 'marto',
    'April': 'aprilo',
    'May': 'majo',
    'June': 'junio',
    'July': 'julio',
    'August': 'aŭgusto',
    'September': 'septembro',
    'October': 'oktobro',
    'November': 'novembro',
    'December': 'decembro'}


## SHORT CIRCUITS ##
catch_help_flag(__doc__, SHELL, SHELL.interface == 'zenity')
notebook("""
    - add '-s' option
    - merge some functions
    - ascii analog clock face""")


## SET UP Tk ##
if SHELL.interface == 'Tk':
    SHELL.msg.config(
        border=2, relief='raised', font=('helvetica', 18, 'bold'),
        bg='#fff', width=200)
    SHELL.main_window.config(bg='dark green')
    SHELL.center_window(width_=300, height_=125)
    if LANG.upper() == "EO":
        SHELL.main_window.title('horloĝo')
    elif LANG.upper() == "EN":
        SHELL.main_window.title('clock')


def main_loop_bash(month):
    """
    Check the time, refresh the clock.
    """
    fig_writer = Figlet('mono9', 'gay')
    Terminal.hide_cursor()
    try:
        while True:
            _today = datetime.datetime.today()
            now = _today.strftime('%l:%M %P')
            if LANG.upper() == 'EO':
                now = now[:-1] + 'tm'

            try:
                string = fig_writer.output(now, get_str=True)
            except OSError:
                Terminal.output(
                    "unix shell not available or 'toilet' not available")

            string += '\n'
            if LANG.upper() == 'EN':
                string += "{}'s for Stevie!!!\n\n".format(month.capitalize())
            elif LANG.upper() == 'EO':
                string += '{} estas por Stevie!!!\n\n'.format(
                    month.capitalize())

            SHELL.output('\n    ' + string.rstrip().replace('\n', '\n    '))
            time.sleep(1)
            Terminal.cursor_v(11)
    except KeyboardInterrupt:
        Terminal.clear(1)
        Terminal.output('\n')
    finally:
        Terminal.unhide_cursor()


def main_loop_dialog():
    """
    Check the time, refresh the clock.
    """
    while True:
        _today = datetime.datetime.today()
        now = _today.strftime('%l:%M %P')
        now = now[:-1] + 'tm'
        string = now
        SHELL.output(string)
        time.sleep(1)


def main_loop_tk(day, month):
    """
    Check the time, refresh the clock.
    """
    if LANG.upper() == 'EO':
        msgtext = "{} estas por Stevie!!!"
    elif LANG.upper() == 'EN':
        msgtext = "{}'s for Stevie!!!"
    else:
        msgtext = ''
    message = tk.Message(
        border=2, relief='raised', font=('courier', 14, 'italic', 'bold'),
        width=270, bg='yellow', fg='blue',
        text=msgtext.format(month.capitalize()))
    message.pack()
    now = day.strftime('%l:%M:%S %P')
    now = now[:-1] + 'tm'
    SHELL.msgtxt.set(now)

    def update(hex_red, hex_green, hex_blue):
        """update the time and the background color."""
        today = datetime.datetime.today()
        now = today.strftime('%l:%M:%S %P')
        if LANG.upper() == 'EO':
            now = now[:-1] + 'tm'
        SHELL.msgtxt.set(now)

        red1 = int(hex_red, 16) + random.randint(-5, 5)
        if red1 > 255:
            red1 = 255
        elif red1 < 0:
            red1 = 0

        blue1 = int(hex_blue, 16) + random.randint(-5, 5)
        if blue1 > 255:
            blue1 = 255
        elif blue1 < 0:
            blue1 = 0

        green1 = int(hex_green, 16) + random.randint(-5, 5)
        if green1 > 255:
            green1 = 255
        elif green1 < 0:
            green1 = 0

        red2 = ('%x' % red1).rjust(2, '0')
        blue2 = ('%x' % blue1).rjust(2, '0')
        green2 = ('%x' % green1).rjust(2, '0')

        hex_string = '#{}{}{}'.format(red2, green2, blue2).upper()
        SHELL.main_window.config(bg=hex_string)
        SHELL.main_window.after(100, lambda: update(red2, green2, blue2))

    SHELL.main_window.after(100, lambda: update('00', '64', '00'))


def get_date_and_month():
    """
    Return date and month from the datetime package as a tuple
    """
    _today = datetime.datetime.today()
    en_month = _today.strftime('%B')
    if LANG.upper() == 'EO':
        mnth = MONTH_DICT[en_month]
    else:
        mnth = en_month
    return (_today, mnth)


def main():
    """
    Main function
    """
    _today, _month = get_date_and_month()
    if SHELL.interface == 'term' and SHELL.os_name == 'posix':
        main_loop_bash(_month)
    elif SHELL.interface == 'dialog':
        main_loop_dialog()
    elif SHELL.interface == 'Tk':
        main_loop_tk(_today, _month)
    else:
        SHELL.message('Sorry.')

if __name__ == '__main__':
    main()
    SHELL.start_app()
