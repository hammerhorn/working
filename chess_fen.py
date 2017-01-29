#!/usr/bin/env python
"""
Convert chessboard position in Forsythe-Edwards notation to an ASCII diagram and
print to standard output.
"""
import sys

from cjh.misc import catch_help_flag, notebook

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Chess(object):
    """
    converts strings of Forsythe-Edwards board notation and draws the board
    position
    """
    def __init__(self, fen_str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
        self.fen_list = fen_str.split('/')

    def __str__(self):
        out_str = '\n'
        for rank in self.fen_list:
            for char in rank:
                if char.isdigit():
                    out_str += '. ' * int(char)
                elif char.isalpha():
                    out_str += char + ' '
            out_str += '\n' #newline at end of each rank
        out_str += '\n' # end with a newline
        return out_str


REMARKS = """
    - try to get OO version up and running"""

notebook(REMARKS)
Terminal()
SHELL = Config().start_user_profile()
if SHELL.platform != 'android':
    catch_help_flag('\nusage: {} [FEN_NOTATION_STR]\n'.format(
        sys.argv[0].replace('./', '')) + __doc__, SHELL)

def main():
    """ Main function """
    # Use class Section from cjh.doc_format
    if len(sys.argv[1:]) == 0:
        board_position = Chess()
    else:
        board_position = Chess(sys.argv[1])
    SHELL.output(board_position, height=200)

    while True:
        board_position = Chess(SHELL.input())
        SHELL.output(board_position, height=200)


if __name__ == '__main__':
    main()
    SHELL.start_app()
