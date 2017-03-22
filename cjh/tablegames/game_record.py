#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
import pprint
import textwrap
import time

import easycat
from things import Thing
from cjh.tablegames.igo import Goban
from versatiledialogs.lists import Enumeration, ItemList
from versatiledialogs.terminal import Terminal

class Turn(Thing):
    """
    Sequential turn within a game
    """
    def __init__(self, color, pt_tuple, comments=''):
        super(Turn, self).__init__()
        self.address = pt_tuple
        self.color = color
        self.comments = comments

    def __remove_captured_stones(self):
        """
        (This is where captured stones will be removed)
        """
        pass

    def __repr__(self):
        commentsf = textwrap.fill(
            self.comments, replace_whitespace=False, width=45)
        #return self.address + '\n' + self.color + '\n\n' + commentsf + '\n'
        if len(
            commentsf) > 0: string = '{}{} ({})'.format(
                self.address[0], self.address[1], commentsf)
        else: string = '{}{}'.format(self.address[0], self.address[1])
        return string

    def __getitem__(self, index):
        return self.address[index]

#    def __str__(self):
#        return "{}{}".format(self.address[0], self.address[1])

class GoGame(Thing):
    """
    One game
    """
    header = {}
    #moves = []

    def __init__(self, sgf_str=''):#, skin='unicode1.json'):
        self.bullets = None

        # Parent constructor
        super(GoGame, self).__init__()

        # Declare a new dictionary
        self.header_dict = {}

        # If an sgf string is given...
        if len(sgf_str) > 0:

            # Split it up into units
            self.units_list = sgf_str.split(';')

            # Get the header string
            self.units_list = self.units_list[1:]  # Game, size 
            self.header_str = self.units_list[0]  # board position

            # Get the list of moves and
            self.moves_list = self.units_list[1:]

            # Strip off any whitespace
            self.moves_list = [move.strip(') \n') for move in self.moves_list]
            #print(self.moves)
            #import sys
            #sys.exit()

            # Convert the header information to a dictionary
            self.head_list = self.header_str.split(']')[:-1]
            for unit in self.head_list:
                unit_list = unit.split('[')
                unit_list = [i.strip() for i in unit_list]
                self.header_dict.update({unit_list[0]:unit_list[1]})

            #there is a better way i think
            self.size = int(self.header_dict['SZ'])

            # Convert the sgf representations to Turn objects
            #for i, move in enumerate(self.moves_list):
            for move in self.moves_list:
                #if self.moves[i[0]][0] == 'B':
                if move[0] == 'B':
                    colour = 'black'
                elif move[0] == 'W':
                    colour = 'white'
                #address = (
                #    self.moves_list[i[0]][2].upper(),
                #    self.size - (ord(self.moves_list[i[0]][3]) - 97))
                #self.moves_list[i[0]] = Turn(colour, address, self.moves_list[i[0]][5:])



        else:

            # If this is a new game, there will be no header.
            # So let's make one.
            black_player = Terminal.input("Black player's name: ")
            white_player = Terminal.input("White player's name: ")
            self.header_dict.update(
                {'SZ': 19,
                 'PW': white_player,
                 'PB': black_player,
                 'KM': 6.5,
                 'GM':1})

        # If this is a new games, there will be no moves....

    def __str__(self):
        return '\n{}{}: {}\n\n{}: {}'.format(
            Terminal.fx('b', self.label),
            Terminal.fx('nu', 'header'),
            pprint.pformat(self.header_dict),
            Terminal.fx('nu', 'moves'),
            self.moves_list)

    def __getitem__(self, index):
        return self.moves_list[index]

    def __len__(self):
        return len(self.moves_list)

    #def __iter__(self):
    #    return

    def __repr__(self):
        string_lst = []
        try:
            if self.header_dict['GM'] == '1':
                string_lst.append('Game: Go\n')
            elif self.header_dict['GM'] == '2':
                string_lst.append('Game: Reversi\n')
        except KeyError:
            pass

        try:
            string_lst.append('Size: {0} x {0}\n'.format(
                self.header_dict['SZ']))
        except KeyError:
            pass

        try:
            string_lst.append('{} vs. {}\n'.format(
                self.header_dict['PW'], self.header_dict['PB']))
        except KeyError:
            pass

        try:
            string_lst.append('Komi: {}\n'.format(self.header_dict['KM']))
        except KeyError:
            pass

        # try:
        for game, index in enumerate(self):  #.game_list):
            self[index].header = str(game[1]) + '\n'            
            # self.game_list[index].header = str(game[1]) + "\n"
        # except: # type?
        #    pass



        ### This block doesn't work ###
        bullet_items = []
        try:
            bullet_items.append(
                'SGF generated by {}.'.format(self.header['AP']))
        except KeyError:
            pass
        if 'DT' in self.header:
            bullet_items.append(self.header['DT'])
        #if "GM" in self.header:
        #    game = ''
        #    if self.header['GM'] == '1':
        #        game = 'go'
        #    else: game = 'unknown'
        #    s += ["The game is {}.".format(game)]
        if 'RU' in self.header:
            bullet_items.append('{} rules.'.format(self.header['RU']))
        if 'SZ' in self.header:
            bullet_items.append('The board size is {0} × {0}.'.format(
                self.header['SZ']))
        if 'KM' in self.header:
            bullet_items.append('Komi is {}.'.format(self.header['KM']))
        if 'PB' in self.header:
            bullet_items.append('Black Player: {}'.format(self.header['PB']))
        if 'PW' in self.header:
            bullet_items.append('White Player: {}'.format(self.header['PW']))
        self.bullets = ItemList(bullet_items)

        ###############################

        moves_enum = Enumeration(self.moves_list)
        string_lst = ['\n', Terminal.fx('u', self.label.title()), string_lst]
        string_lst.extend(('\nmoves_enum: ',
                           str(moves_enum),
                           '\n',
                           Terminal.hrule(string=True, width=40)))
        return ''.join(string_lst)

    def less(self):
        """
        show with a pager
        """
        easycat.less(self.__str__())

    def play_thru(self, autoplay=False):
        """
        page thru a game
        """
        goban = Goban(int(self.header_dict['SZ'])) #, skinfile=self.skin)
        color = 'black'
        for _, turn in enumerate(self.moves_list):
            goban.place_stone(turn[0], int(turn[1:]), color)
            func = lambda: time.sleep(0.25) if autoplay else Terminal.wait

            Terminal.make_page(self.label, str(goban), func)
            if color == 'white':
                color = 'black'
            elif color == 'black':
                color = 'white'


class GameRecord(Thing):
    """
    First, I will try to make it work with single-game files.
    """
    def __init__(self, filename):#, skin="unicode1.json"):
        super(GameRecord, self).__init__()
        GoGame.count = 0
        self.headers = []
        self.games = []

        # Read file into buffer
        self.buffer_ = easycat.cat(
            files=[filename], quiet=True, return_str=True)

        self.chunks = self.buffer_.split('(')[1:]

        for chunk in self.chunks:
            self.games.append(GoGame(chunk))

#        # Break the buffer up into units, with ';' as the delimiter
#        self.unit_list = self.buffer_.split(';')

        # Strip newlines off of units in unit_list
#        for index, unit in enumerate(self.unit_list):
#            self.unit_list[index] = unit.strip()

        # Get headers
#        for index, unit in enumerate(self.unit_list):
#            if unit.startswith('('):
#                self.headers.append(self.unit_list[index + 1])
        #if len(this_game) > 0:
#                self.games.append(GoGame(self.headers[0]))
#                this_game.append(unit)
#                print "game = " + str(this_game)
#            print('[+] unit_list[{}]: {}'.format(index, self.unit_list[index]))
#        self.headers.append(self.unit_list[1])
        #self.games.append(GoGame(self.headers[0]))
#        moves = []
#        Cli.wait()
#        count = 2
#        board = Goban()

#        while True:
#            address = unit_list[count].split('[')[1][0:2]
#            if unit_list[count][0] == 'B': color = 'black'
#            elif unit_list[count][0] == 'W': color = 'white'
#            if len(unit_list[count]) > 5: comments = unit_list[count][7:-2]
#            else: comments = ''
#            turn = Turn(color, address, comments)
#            board.place_stone(address[0].upper(), ord(address[1]) - 96, color)
#            Cli.clear()
#            print board
#            print '\n' + Cli.term_fx('u', "Turn:") + str(turn)
#            count += 1
#            Cli.wait()

    def __str__(self):
        #s = ''
        #for game in self.game_list:
        #    s += ("\n" + str(game))
        #return s
        return self.buffer_

    def __getitem__(self, index):
        return self.games[index]

    def __len__(self):
        return len(self.games)

    def __iter__(self):
        pass
