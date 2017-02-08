#!/usr/bin/env python3
#coding=utf8
"""
usage: cowscript [message]

    Interactively browse through
available art for cowsay classic
UNIX utility.

* If fortunes program is available,
  it will provide the text.

* Otherwise, the user must provide
  a string of text.
"""
import os
import subprocess
import sys

from cjh.misc import catch_help_flag, notebook

from ttyfun.unix import Cow
from versatiledialogs.config import Config
from versatiledialogs.lists import PlainList
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

##################
##  PROCEDURES  ##
##################
def prelims():
    """
    if '-h', print help and exit
    """
    notebook("""    - there should be a cow: object? interface? shell method?
    - maybe a dropdown list would be better?""")
    catch_help_flag(__doc__, SHELL)
    SHELL.welcome(description=__doc__)

def define_text():
    """
    Use  /usr/games/fortunes if present.  Otherise, read from
    command-line args.
    """
    try:
        text = subprocess.check_output('fortune -s', shell=True)
    except (OSError, subprocess.CalledProcessError):
        try:
            text = sys.argv[1]
        except IndexError:
            SHELL.message('use: cowscript [message]')
            sys.exit()
    return text.strip().decode('utf8')


def make_list_obj():
    """
    Populate an AbstractList object with a list of available ASCII art
    files.
    """
    tmp_list = []
    cow_list = os.listdir('/usr/share/cowsay/cows')
    for cow in cow_list:
        cow = cow.split('.')[:-1]
        cow = '.'.join(cow)
        tmp_list.append(cow)
    cow_list = tmp_list
    cow_list.sort()
    return PlainList(cow_list)


#################
##  CONSTANTS  ##
#################
CONFIG = Config()
SHELL = CONFIG.start_user_profile()
LIST_OBJ = make_list_obj()
MENU_FUNC = lambda: SHELL.list_menu(LIST_OBJ)
TERMINAL = Terminal()

############
##  MAIN  ##
############
def main():
    """
    Feed fortunes to the selected ASCII character.
    """

    prelims()

    cow = ''
    message1 = define_text()
    cow_num = TERMINAL.make_page('UP NEXT: {}'.format(message1), '', MENU_FUNC)

    while True:
        message2 = message1
        message1 = define_text()
        cow = LIST_OBJ[cow_num - 1]
        message2 = message2.replace('"', r'\"')
        ascii_cow = Cow(cow).output(message2, get_str=True)
        TERMINAL.make_page(
            'UP NEXT: {}'.format(message1),
            ascii_cow,
            SHELL.wait)
        cow_num = TERMINAL.make_page(
            'UP NEXT: {}'.format(message1),
            '',
            MENU_FUNC)

if __name__ == '__main__':
    main()
    SHELL.start_app()
