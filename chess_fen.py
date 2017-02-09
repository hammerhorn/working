#!/usr/bin/env python3
"""
Convert chessboard position in Forsythe-Edwards notation to an ASCII
diagram and print board position to standard output.
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
    SCRIPT_NAME = sys.argv[0].replace('./', '')
    catch_help_flag(
        '\nusage: {} [FEN_NOTATION_STR]\n'.format(SCRIPT_NAME)+__doc__,
        SHELL)

def rank_list(fen_str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
    """return a list, a str for each rank"""
    return fen_str.split('/')

def draw(fen_list):
    """draw the board to stdout"""
    out_str_lst = ['\n']
    for rank in fen_list:
        for char in rank:
            if char.isdigit():
                out_str_lst.append('. ' * int(char))
            elif char.isalpha():
                out_str_lst.extend([char, ' '])
        out_str_lst.append('\n') #newline at end of each rank
    out_str_lst.append('\n') # end with a newline
    return ''.join(out_str_lst)


def main():
    """ Main function """
    kwarg_dict = {}
    if SHELL.interface == 'Tk':
        SHELL.msg.config(font=('courier'))
        kwarg_dict.update({'height': 200})

    # Use class Section from cjh.doc_format
    board_position = rank_list() if len(sys.argv[1:]) == 0 else rank_list(
        sys.argv[1])
    SHELL.output(draw(board_position), **kwarg_dict)

    while True:
        fen_str = SHELL.input()
        if len(fen_str) == 0:
            break
        board_position = rank_list(fen_str)
        SHELL.output(draw(board_position), **kwarg_dict)

if __name__ == '__main__':
    main()
    SHELL.start_app()
