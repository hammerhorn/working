#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
from cjh.maths.geometry import Point
from ranges import gen_range
from things import Thing

from versatiledialogs.terminal import Terminal
from versatiledialogs.lists import PlainList

TUI = Terminal()

class ChessSquare(Point):
    """
    a single square on a chess board
    """
    def __init__(self, x, y):
        super(ChessSquare, self).__init__(x, y)
        self.label = '. '
        self.occupant = None

    def __str__(self):
        return self.label

    def address(self):
        return '({}, {})'.format(self.x, self.y)

    def populate(self, piece):
        self.occupant = piece
        self.label = self.occupant.abbrev
        
class ChessBoard(Thing):
    """
    chess board
    """
    def _get_board_type(self):
        board_list = PlainList(
            ('8x8', '9x9', '10x9'),
            heading="Board Size")
        self.board_type = board_list[TUI.list_menu(board_list) - 1]
        TUI.output(self.board_type)
        if self.board_type == '8x8':
            self.rankcount, self.colcount = 8, 8
        elif self.board_type == '9x9':
            self.rankcount, self.colcount = 9, 9
        elif self.board_type == '10x9':
            self.rankcount, self.colcount = 9, 10
		
    def __init__(self):
        super(ChessBoard, self).__init__()
        TUI.output('')
        self._get_board_type()
        
        self.board_array = [[0 for _ in gen_range(self.colcount)] for _ in gen_range(
            self.rankcount)]

        for rank in reversed(gen_range(self.rankcount)): #range(self.rankcount)[::-1]:
            for col in gen_range(self.colcount):
#                print('self.board_array[{0}][{1}] = ChessSquare({0}, {1})'.for
#                mat(col, self.rankcount - rank - 1))
                self.board_array[col][self.rankcount - rank - 1] = ChessSquare(
                    col, self.rankcount - rank - 1)
               # self.board_array[col][rank].populate(ChessPiece(raw_input(), ''))


    def __str__(self):
        #out_str = ''
        #for x in self.board_array:
        #    out_str += x.__str__()
        out_str_list = []

        for rank in reversed(gen_range(self.rankcount)):  #[::-1]:
            for col in gen_range(self.colcount):
                if self.board_array[col][rank].occupant is not None:
                    out_str_list.extend((self.board_array[col][rank].occupant.abbrev, ' '))
                else:
                    out_str_list.append('. ')
                #Terminal.clear(1)
                #Terminal.wait(out_str)
                
            out_str_list.append('\n')

        return ''.join(out_str_list)


    def read_fen(self, fen_str):
        fen_list = fen_str.split('/')
        out_str_list = []
        for row in fen_list:
            for char in row:
                self.board_array[row.index(char)][fen_list.index(row)].populate(ChessPiece(char))
#            out_str += row #self.board_array[col][rank].label
#            out_str += '\n'
            out_str_list.extend((row, '\n'))
        return ''.join(out_str_list)

    
    def map(self):
        out_str_list = []
        for rank in gen_range(self.rankcount):
            for col in gen_range(self.colcount):
                out_str_list.append(self.board_array[col][rank].address())
            out_str_list.append('\n')
        return ''.join(out_str_list)

    def edit(self):
        try:
            position = ChessSquare(0, 0)
            Terminal.output(self.__str__())
            while True:
                #print('\n' * 3 + self.__str__())
                Terminal.clear(self.rankcount + 2)
                Terminal.output(self.__str__())
                self.board_array[int(position.x)][int(position.y)].label = '. '
                key = Terminal.get_keypress()

                if key in 'Ll' and position.x < self.colcount - 1:
                    position.x += 1
                elif key in 'Hh' and position.x > 0:
                    position.x -= 1
                elif key in 'Jj' and position.y > 0:
                    position.y -= 1
                elif key in 'Kk' and position.y < self.rankcount - 1:
                    position.y += 1
                self.board_array[int(position.x)][int(position.y)].label = '? '
        except KeyboardInterrupt:
            return
     #       print("self.board_array[{}][{}].label = '? '".format(int(position.
     #       x), int(position.y)))


class ChessPiece(Thing):
    """
    custom piece
    """
    def __init__(self, abbrev, parlett_str='1>'):
        super(ChessPiece, self).__init__()
        self.pstr = parlett_str
        self.abbrev = abbrev

    def __str__(self):
        return Terminal.fx('u', self.label) +\
            'Parlett notation: {}\n    Abbreviation: {}\n'.format(
                self.abbrev, self.pstr)


        #capturing_move=set([Vector(math.sqrt(2), Angle(45)), Vector(mat
        #h.sqrt(2), Angle(-45))])
        #first_move= set([Vector(2, Angle(0))])


class ChessVariant(Thing):
    """
    custom variant
    """
    def __init__(self):
        super(ChessVariant, self).__init__()
        self.board = ChessBoard()
        #TUI.output(self.board.__str__())

        #pawn_list = PlainList(
        #    ['o1>,c1X>,oi2>', 'o1>,c1X>', '1>=', '1>'],
        #    heading="Pawn type")
        #self.pawn_type = pawn_list[TUI.list_menu(pawn_list) - 1]
        #cli.write('You have selected a variant with a')
        #if self.board.board_type == '8x8':
        #    cli.write('n')
        #TUI.output(' {} board'.format(
        #    self.board.board_type))
        #print('\n' + ChessPiece('p', self.pawn_type).__str__())
        
    def __str__(self):
        return self.board.__str__()
        
def main():
    variant1 = ChessVariant()
    #print variant1
    print(variant1.board)
#    fen_str = raw_input("FEN string (e.g., 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')\n : ")
#    print(variant1.board.read_fen(fen_str))
#    print(variant1.board)    
#    variant1.board.edit()
    #piece1 = ChessPiece('1>')
    #TUI.output(piece1)

#    board1 = ChessBoard()
#    TUI.output(board1)
#    #cli.Cli.wait(board1.map())
#    board1.edit()

if __name__ == '__main__':
    main()
#cb1 = ChessBoard()
# regular move - 1 forward or 1 forward or one to the side
# capturing move - 1 diagonal or 1 forward or
# special first move
# promotion
# starting position
