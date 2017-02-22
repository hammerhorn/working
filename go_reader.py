#!/usr/bin/env python
#coding='utf-8'
"""
replay a go game from an SGF file

use: ./go_reader.py [ SGF_FILE ]
"""
import argparse

from cjh.tablegames.game_record import GameRecord
from cjh.tablegames.igo import Goban
import easycat
from versatiledialogs.lists import Enumeration
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str)
    if __name__ == '__main__':
        args = parser.parse_args()
    else: args = None
    return args


##########
#  DATA  #
##########
ARGS = _parse_args()
Terminal()

##########
#  MAIN  #
##########
def main():
    """
    Main function
    """
    record = GameRecord(ARGS.filename)

    game_list = record[:]
    game_label_list = [game.label for game in game_list]

    while True:
        int_response = Terminal.list_menu(Enumeration(game_label_list))
        move_list = game_list[int_response - 1][:]
        easycat.less(Enumeration(move_list))

        goban = Goban(game_list[int_response - 1].header_dict['SZ'])

        color = 'black'
        for move in move_list:
            Terminal.wait()
            Terminal.clear()
            Terminal.output(goban)
            goban.place_stone(move.address[0], move.address[1], color)

            if color == 'black':
                color = 'white'
            elif color == 'white':
                color = 'black'

if __name__ == '__main__':
    main()
