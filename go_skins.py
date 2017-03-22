#!/usr/bin/env python
#coding=utf8
"""
View the available "skins" for class Goban.
"""
import os

from cjh.misc import notebook, read_json_file
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
SKIN_LIST = [sk for sk in os.listdir('__data__/skins') if sk.endswith('json')]
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
            goban.skin_dict = read_json_file('__data__/skins/%s' % skinfile)
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
