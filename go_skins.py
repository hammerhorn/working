#!/usr/bin/env python
#coding=utf8
"""
View the available "skins" for class Goban.
"""

import json
import os
# import sys

from cjh.misc import notebook
from cjh.tablegames.igo import Goban
from ttyfun import blocks
from versatiledialogs.config import Config
from versatiledialogs.lists import PlainList
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - some of the angles are not correct"""

notebook(REMARKS)
CONFIG = Config()
SHELL = CONFIG.start_user_profile()
SKIN_LIST = [sk for sk in os.listdir('skins') if sk.endswith('json')]
SKIN_LIST.sort(key=str.lower)
LIST_OBJ = PlainList(SKIN_LIST)


def main():
    """
    Lets user browse and preview skins for the Goban class.
    """
    goban = Goban(sh_obj=SHELL, size=9)
    while True:
        choice = Terminal.make_page(func=lambda: SHELL.list_menu(LIST_OBJ))
        skinfile = LIST_OBJ[choice - 1]
        try:
            if SHELL.py_version == 2:
                goban.skin_dict = json.load(open('skins/' + skinfile, 'rb'))
            elif SHELL.py_version == 3:
                file_ptr = open('skins/{}'.format(skinfile), 'rb')
                text_buffer = file_ptr.read().decode('utf-8')
                goban.skin_dict = json.loads(text_buffer)
        except IOError:
            Terminal.text_splash(blocks.box("File Error with '{}'".format(
                skinfile)), duration=0)
            SHELL.wait()
            continue
        goban.cursor = [0, 0]
        Terminal.text_splash("== Now give '{}' a try! ==".format(
            skinfile), duration=1, flashes=4)
        goban.view_edit()

if __name__ == '__main__':
    main()
