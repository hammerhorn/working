#!/usr/bin/env python
#coding=utf8

from versatiledialogs.terminal import Terminal

class ChessPiece(object):
    piece_dict = {
        'p':'pawn',
        'n':'knight',
        'b':'bishop',
        'r':'rook',
        'q':'queen',
        'k':'king'}

    value_dict = {
        'p': 1,
        'n': 3,
        'b': 3,
        'r': 5,
        'q': 9,
        'k': 0
    }

    unicode_dict = {
        'P': '♙',
        'N': '♘',
        'B': '♗',
        'R': '♖',
        'Q': '♕',
        'K': '♔',
        'p': '♟',
        'n': '♞',
        'b': '♝',
        'r': '♜',
        'q': '♛',
        'k': '♚'
    }

    parlett_dict = {
        'p': 'o1>, c1X>, oi2>',
        'n': '~1/2',
        'b': 'nX',
        'r': 'n+',
        'q': 'n*',
        'k': '1*'
    }

    
    def __init__(self, abbrev):
        self.abbrev = abbrev
        if self.abbrev.isupper():
            self.color = 'white'
        else:
            self.color = 'black'
        self.name = self.__class__.piece_dict[self.abbrev.lower()]
        self.value = self.__class__.value_dict[self.abbrev.lower()]
        self.symbol = self.__class__.unicode_dict[self.abbrev]
        self.move = self.__class__.parlett_dict[self.abbrev.lower()]

    def __str__(self):
        out_str = Terminal.fx('un', '{} {:6s}'.format(self.color, self.name)) + '({}).....{} points \033[2m\033[38;5;0;48;5;231m{}\033[0m\t{}\n\n'.format(self.abbrev, self.value, self.symbol, self.move)
        return out_str

class ChessSquare(object):
    def __init__(self, address, occupant):
        self.address = address
        self.occupant = occupant

    def __str__(self):
        out_str = ' address: {}\noccupant: {}\n'.format(
            self.address, self.occupant)
        return out_str

class ChessBoard(object):
    def __init__(self, fen_str='rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR'):
        fen_list = fen_str.split('/')
        self.rank_count = len(fen_list)
        self.col_count = len(fen_list[0]) #temporary solution only?

        print '{} x {}'.format(self.col_count, self.rank_count)
        self.rank_list = [[]]
        #for rank_no in range(self.rank_count):
        #    for col_no in range(self.col_count):
        #        print "self.rank_list[{0}] += [ChessSquare('', ChessPiece(fen_
        #list[{0}][{1}]))]".format(rank_no, col_no)
        #        try:
        #            self.rank_list[rank_no] += [ChessSquare('', ChessPiece(fen_
        #list[rank_no][col_no]))]
        #        except IndexError:
        #            pass

        ####
        # self.rank_list[0] += [ChessSquare('a8', ChessPiece('r'))]
        # self.rank_list[0] += [ChessSquare('b8', ChessPiece('n'))]
        # self.rank_list[0] += [ChessSquare('c8', ChessPiece('b'))]
        # self.rank_list[0] += [ChessSquare('d8', ChessPiece('k'))]
        # self.rank_list[0] += [ChessSquare('e8', ChessPiece('q'))]
        # self.rank_list[0] += [ChessSquare('f8', ChessPiece('b'))]
        # self.rank_list[0] += [ChessSquare('g8', ChessPiece('n'))]
        # self.rank_list[0] += [ChessSquare('h8', ChessPiece('r'))]

    def __str__(self):
        out_str = '{} ranks\n'.format(self.rank_count)
        for rank in range(self.rank_count-1):
            try:
                out_str += 'Rank {}:'.format(rank)
                out_str += str(self.rank_list[rank])
            except:
                pass
        out_str += str(self.rank_list)
        #for rank in range(self.rank_count):
        #    try:
        #        for sq in self.rank_list[rank]:
        #            out_str += sq.occupant.abbrev
        #    except IndexError:
        #        pass
        #    out_str += '\n'
        return out_str
