#!/usr/bin/env python3
"""
Convert chessboard position in Forsythe-Edwards notation to an ASCII diagram and
print board position to standard output.
"""
import sys

from cjh.misc import catch_help_flag, notebook

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


REMARKS = """
    - try to get OO version up and running"""

notebook(REMARKS)
Terminal()
SHELL = Config().start_user_profile()
if SHELL.platform != 'android':
    catch_help_flag('\nusage: {} [FEN_NOTATION_STR]\n'.format(
        sys.argv[0].replace('./', '')) + __doc__, SHELL)


def rank_list(fen_str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
    fen_list = fen_str.split('/')
    return fen_list
    
def draw(fen_list):
    out_str = '\n'
    for rank in fen_list:
        for char in rank:
            if char.isdigit():
                out_str += '. ' * int(char)
            elif char.isalpha():
                out_str += char + ' '
        out_str += '\n' #newline at end of each rank
    out_str += '\n' # end with a newline
    return out_str


def main():
    """ Main function """
    # Use class Section from cjh.doc_format
    board_position = rank_list() if len(sys.argv[1:]) == 0 else rank_list(
        sys.argv[1])
    SHELL.output(draw(board_position), height=200)

    while True:
        fen_str = SHELL.input()
        if len(fen_str) == 0:
            break
        board_position = rank_list(fen_str)
        SHELL.output(draw(board_position), height=200)



if __name__ == '__main__':
    main()
    SHELL.start_app()
