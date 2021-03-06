#!/usr/bin/env python
#coding=utf8
"""
classes: Point, Area, TwoDShape, Polygon, Ellipse, Circle, Graph

move non-geometry stuff from graph to goboard
"""
import decimal
import json
import math
import sys
import time

try:
    import Tkinter as tk
except ImportError:
    try:
        import tkinter as tk
    except ImportError:
        print("Could not import module 'tkinter'.") #pylint: disable=C0325

from termcolor import colored

from cjh.letterator import Letter
from cjh.maths.algebra import Polynom
from cjh.maths.angles import Angle
import easycat
from fiziko.kinematics import Disp
from fiziko.scalars import Scalar, Unit
from ranges import gen_range
from things import Thing
from versatiledialogs.lists import Enumeration, ItemList, PlainList
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Point(Disp):
    """
    2-d spatial point
    """
    def __init__(self, x, y):
        super(Point, self).__init__(0, Angle())
        # self.label = 'a point'
        self.x_mag, self.y_mag = float(x), float(y)
        self.units = Unit()
        # self.marker = 'none'  # should be put into child class go_stone?
        self._initialize()
        self.mag = math.sqrt(self.x_mag**2 + self.y_mag**2)
        # if self.x_mag < 0.0:  # what does this do?
        #    self.mag *= -1.0
        self.theta.units = Unit('rad')

    def __repr__(self):
        return '({}, {})'.format(round(self.x_mag, 4), round(self.y_mag, 4))

    def __eq__(self, other):
        return self.tuple() == other.tuple()

    def __ne__(self, other):
        return self.tuple() != other.tuple()

    def __add__(self, other):
        return Point(
            decimal.Decimal(self.x_mag) + decimal.Decimal(other.x_mag),
            decimal.Decimal(self.y_mag) + decimal.Decimal(other.y_mag))

    def __sub__(self, other):
        """Get the distance between two points."""
        return math.hypot(self.x - other.x, self.y - other.y)

    def _initialize(self):
        """
        Finds the distance from the origin and the angle.
        (There might be something comparable in a parent class?)
        """
        self.mag = math.sqrt(self.x_mag**2 + self.y_mag**2)
        try:
            self.theta = Angle(math.atan(self.y_mag/self.x_mag), 'rad')
        except ZeroDivisionError:
            self.theta = Angle(0, 'rad')
        if self.x_mag < 0.0:
            self.mag *= -1.0
        self.theta.units = Unit('rad')

    def input(self, shell=Terminal, prompt=''):
        """prompts user for comma-separated tuple"""
        prompt += ' (x, y) : '
        inp = lambda: tuple(eval(shell.input(prompt)))  # pylint: disable=W0123

        while True:
            try:
                self.x_mag, self.y_mag = inp()
            except KeyboardInterrupt:
                break
            except (NameError, TypeError, ValueError):  # What kind?
                continue
            else:
                break
        self._initialize()

    @property
    def distance_str(self):
        """str describing the distance from the origin"""
        return '{} from the origin'.format(Scalar(abs(self.mag), self.units))

    def tuple(self):
        """returns point as a float tuple"""
        return (self.x_mag, self.y_mag)

    @property
    def x(self):
        """x magnitude of the Point"""
        return self.x_mag

    @x.setter
    def x(self, x_val):
        """setter for x"""
        self.x_mag = float(x_val)
        self._initialize()

    @property
    def y(self):
        """y magnitude of the Point"""
        return self.y_mag

    @y.setter
    def y(self, y_val):
        """setter for y"""
        self.y_mag = float(y_val)
        self._initialize()

    @property
    def x_y(self):
        """coordinates in tuple form"""
        return self.tuple()

    @x_y.setter
    def x_y(self, xy):
        """takes a 2-member tuple"""
        self.x_mag = xy[0]
        self.y_mag = xy[1]
        self._initialize()


class Area(Scalar):
    """area on a two-dimensional grid, surface area"""
    def __init__(self, d=0.0):
        super(Area, self).__init__(d, 'units^2')

    def draw(self):
        """ a very rough approximation only """
        length = int(float(self.mag) ** 0.5)
        drawn = 0
        for _ in range(length):
            Terminal.output('')
            for _ in range(length):
                easycat.write(colored('  ', attrs=['reverse', 'bold']))
                drawn += 1

            easycat.write(' ')
        for _ in range(int(self.mag) - drawn):
            easycat.write(colored('  ', attrs=['reverse', 'bold']))

class TwoDShape(Thing):
    """Ellipses and Polygons"""
    def __init__(self):
        super(TwoDShape, self).__init__()
        self.perimeter = Disp(u='units')
        self.area = Area()

    def __str__(self):
        return ''.join(
            ('\n', Terminal.fx('u', self.label),
             '{:>9} = {}\n'.format('Area', self.area),
             '{:>9} = {}'.format('Perimeter', self.perimeter.to_scalar())))

    @property
    def area_(self):
        """returns area as an Area object"""
        return self.area

    @area_.setter
    def area_(self, fl):
        """set area, takes a float"""
        self.area = Area(fl)

    @property
    def perim(self):
        """returns perimeter as Disp object"""
        return self.perimeter

    @perim.setter
    def perim(self, fl):
        """set perimeter, takes a float"""
        self.perimeter = Disp(fl)


class Polygon(TwoDShape):
    """Polygon - will be changed to being set by a collection of Points"""
    def __init__(self, sides):
        super(Polygon, self).__init__()
        self.label += ' ({}-gon)'.format(sides)
        self.sides = sides
        self.angle_sum = Angle((self.sides - 2) * 180)

    def __str__(self):
        return ''.join(('In a figure with {} sides,\n'.format(self.sides),
                        '\n\tsum of all angles = {}\n'.format(self.angle_sum),
                        '\t    average angle = {}\n'.format(
                            self.angle_sum / self.sides)))

class Ellipse(TwoDShape):
    """Plot Ellipse, get area and circumference; parent for Circle"""
    def __init__(self, h_semiaxis, v_semiaxis=None,
                 center_point=Point(0.0, 0.0)):
        super(Ellipse, self).__init__()
        if v_semiaxis is None:
            v_semiaxis = h_semiaxis
        self.area = Area(decimal.Decimal(math.pi) * decimal.Decimal(
            h_semiaxis) * decimal.Decimal(v_semiaxis))
        self.center = center_point
        if h_semiaxis > v_semiaxis:
            f = math.sqrt(h_semiaxis ** 2 - v_semiaxis ** 2)
            self.focus1 = self.center + Disp(f, 'units', Angle(0))
            self.focus2 = self.center - Disp(f, 'units', Angle(0))
            self.eccentricity = f / h_semiaxis
        else:
            f = math.sqrt(v_semiaxis ** 2 - h_semiaxis ** 2)
            self.focus1 = Point(self.center.x_mag, self.center.y_mag + f)
            self.focus2 = Point(self.center.x_mag, self.center.y_mag - f)
            self.eccentricity = decimal.Decimal(f) / decimal.Decimal(v_semiaxis)

    def __str__(self):
        s = ''.join(
            ('\n', Terminal.ul(self.label),
             '\n{:>13} = {}\n'.format('Area', self.area),
             '{:>13} = {}\n'.format('Center', self.center)))

      # s += "{:>13} = {}".format('Circumference', self.perimeter.to_Scalar())
        
        if self.focus1 != self.focus2:
            s += '{:>13} = {} & {}\n'.format('Foci', self.focus1, self.focus2)
        s += '{:>13} = {}\n'.format('Eccentricity', self.eccentricity)
        return s

class Circle(Ellipse):
    """Plot Circles; get area and circumference"""
    def __init__(self, radius, center=Point(0.0, 0.0)):
        """currently takes a float"""
        super(Circle, self).__init__(radius, center_point=center)
        self.perimeter = Disp(decimal.Decimal(2.0) * decimal.Decimal(
            math.pi) * decimal.Decimal(radius))
        self.radius = Disp(radius, u='units')

    def eval(self, x_input):
        """Modify this to return a tuple of two y values"""
        return (
            self.__call__(x_input),
            self.center.y_mag - math.sqrt(
                self.radius.mag ** 2 - decimal.Decimal(
                    x_input - self.center.x_mag) ** 2))

    def __call__(self, x_value):
        """Function of the upper half of the circle"""
        try:
            return self.center.y_mag + math.sqrt(
                self.radius.mag ** 2 -decimal.Decimal(
                    x_value - self.center.x_mag) ** 2)

        except ValueError:
            Terminal.notify(
                'function is undefined at f({})'.format(x_value))
            return None


class Graph(Thing):
    """
    a crude graphing calculator and multi-purpose grid
    """
    def __get_basedir(self):
        basedir = '__data__/skins'
        if self.sh_obj.platform == 'android':
            basedir =\
                '/storage/sdcard0/com.hipipal.qpyplus/lib/python2.7/\
                site-packages/' + basedir  # should read from config
        return basedir
            
    def __init__(self, size=19, skinfile='graph.json',
                 sh_obj=Terminal(), adjust_ssize=0):
        self.sh_obj = sh_obj
        basedir = self.__get_basedir()

        super(Graph, self).__init__()
        self.size = int(size)

        # shrink to screen size
        def shrink(deduct):
            """
            if board would be too big for screen size, make a smaller board.
            """
            if self.size + deduct > Terminal.height():
                self.size = Terminal.height() - deduct
        shrink(-adjust_ssize)

        max_domain = self.size // 2
        min_domain = -max_domain
        if self.size % 2 == 0:
            min_domain += 1
        #print('Size is %s' % self.size)
        #print('Max domain is %s' % max_domain)
        #print('Min domain is %s' % min_domain)        
        #Terminal.wait()
        
        self.domain = (min_domain, max_domain)
        self.cursor = [self.domain[0], self.domain[1]]
        #if self.size % 2 == 0:  # wtf
        #    self.cursor[0] -= 1 # idk
        self.plane = [[0 for _ in gen_range(self.size)] for _ in gen_range(self.size)]
        #print(self.plane)
        for col in gen_range(self.size):
            for rank in gen_range(self.size):
                self.plane[col][rank] = Point(
                    col - self.domain[1], self.domain[1] - rank)

                if col == -self.domain[0] and rank == self.domain[1]:
                    self.plane[col][rank].marker = 'origin'
                elif col == -self.domain[0]:
                    self.plane[col][rank].marker = 'y_axis'
                elif rank == self.domain[1]:
                    self.plane[col][rank].marker = 'x_axis'
                else: self.plane[col][rank].marker = 'empty'


    # DO NOT--># if self.is_hoshi(
    #       -->#     col - self.max_domain, self.max_domain - rank):
    # ERASE!-->#     self.plane[col][rank].marker = 'hoshi'

        #if sys.version_info.major == 2:

        self.skin_dict = json.load(open(
            '{}/{}'.format(basedir, skinfile), 'r'))

        #elif sys.version_info.major == 3:
        #    file_handle = open(basedir + '/' + skinfile, 'r')
        #    file_str = file_handle.read()  # .decode('utf-8')
        #    self.skin_dict = json.loads(file_str)

        ##    reader = codecs.getreader('utf-8')
        ##    self.skin_dict = json.load(reader('skins/' + skinfile))
        ##    self.skin_dict = json.load(f)
        ##    raw_input('Press enter to try opening ' + skinfile)
        ##    self.skin_dict = json.load(str(open('skins/' + skinfile, 'rb'), en
#co
#ding='UTF-8'))     ##
#        except: # else:
#            self.skin_dict = {"black"  : u"● ",
#                              "white"  : u"o ",
#                              "star"   : u"⨉ ",
#                              "hoshi"  : u"  ",
#                              "origin" : u"+-",
#                              "y_axis" : u"| ",
#                              "x_axis" : u"--",
#                              "empty"  : u"  "}
        #self.skin = skinfile

        self.fx_list = []
        self.funct_cnt = len(self.fx_list)
        seq = Letter.caps_gen()
        Letter.pass_no = 1
        self.letters = [next(seq) for _ in range(self.size)]
        #self.label = "goban #%d (%d × %d)" % (self.__class__.count, BOARD_SIZE
#, B
#OARD_SIZE)
        self.label += ' ({0} × {0})'.format(self.size)

    def __str__(self):
        """this would be better if the cursor could be hidden"""
        str_list = ['\n'] #'{}\n'.format(self.ul_label(self.size * 2 + 5))
        str_list.append(' ' * 3)
        for i in range(self.size):
            str_list.append('{:>2s}'.format(self.letters[i]))
        str_list.append('\n')

        for rank in range(self.size):
            str_list.append('%3d ' % (self.size - rank))
            for col in range(self.size):
                # xy_coords = self.indices_to_point(col, rank).tuple()
                xy_coords = col + self.domain[0], self.domain[1] - rank
                if xy_coords == tuple(self.cursor):
                    str_list.append('\b(')
                tag_list = self.skin_dict.keys()
                tag = self.plane[col][rank].marker
                symbol = self.skin_dict[tag] if tag in tag_list else '??'  # .encode('utf-8')
                str_list.append(symbol)  # .encode('utf-8'))
                if xy_coords == tuple(self.cursor):
                    str_list.append('\b)')
            if self.size > 9:
                str_list.append('{:2d} '.format(self.size - rank))
            else: str_list.append('{:1d} '.format(self.size - rank))
            str_list.append('\n')
        str_list.append(' '* 3)
        for i in range(self.size):
            str_list.append('{:>2s}'.format(self.letters[i]))
        str_list.append('\n')
        return ''.join(str_list)


     ###########
     #  PLANE  #
     ###########
    #@staticmethod
    #def is_hoshi(self, x, y):
    #    """
    #    don't show "cross-hairs"
    #    returns False
    #    """
    #    return False

    def fill(self, color='empty'):
        """
        some problems under python3?
        """
        for col in gen_range(self.domain[0], self.domain[1] + 1):
            for rank in gen_range(self.domain[0], self.domain[1] + 1):
                #try:
                self.plot_point(col, rank, color)
                #except:
                #    print 'fail: ' + str(col) + ', ' + str(rank)
                #time.sleep(0.1)  #  / self.size ** 2)
                #Terminal.cursor_v(self.size + 5)
                #print('(' + str(col) + ', ' + str(rank) + ')\n' + self.__str__())


    def view_edit(self):  # , widget=None):
        """
        Interactive wysiwyg editor

        * When board size is even, rightmost column willaccept neither a  point
        nor the cursor, but you can go past and back.
        """
        Terminal.hide_cursor()
        point = None  # self.pt_at_cursor()  # ???
        while True:
            try:
                if self.sh_obj.interface == 'term':
                    try:  # this is probably cheating
                        point = Terminal.make_page(
                        'EDIT', self, self.pt_at_cursor)
                    except IndexError:
                        pass
                elif self.sh_obj.interface == 'Tk':
                    self.sh_obj.msgtxt.set(self.__str__())
                    point = self.pt_at_cursor()

                if isinstance(point, Point):
                    string = ''.join(
                        ('\t', point.__str__(), '\n\t[', point.distance_str,
                        ']\n'))

                    if self.sh_obj.interface == 'term':
                        Terminal.output(string)
                    #self.sh_obj.output(string)
                    elif self.sh_obj.interface == 'Tk':
                        tk.Label(self.sh_obj.main_window, text=str(point))
                        tk.Label(self.sh_obj.main_window, text='[{}]'.format(
                            point.distance_str))
                        #label1.pack()
                        #label2.pack()

                info_list = [
                    'Use h, j, k, l or the arrow keys to move the cursor',
                    'b=black, w=white, x=erase, *=star',
                    'Ctl-c to exit editor']
                #if self.cursor[0] < self.domain[0] or\
                #   self.cursor[0] > self.domain[1] or\
                #    self.cursor[1] < self.domain[0] or\
                #    self.cursor[1] > self.domain[1]:
                #    rescue_key = 'j or k' if self.cursor[1] < self.domain[0] or\
                #                 self.cursor[1] > self.domain[1] else 'l or h'
                #    info_list[0] = 'Press {} to reveal cursor'.format(
                #        rescue_key)

                info = ItemList(info_list)
                if self.sh_obj.interface == 'term':
                    Terminal.output(info)
                elif self.sh_obj.interface == 'Tk':
                    tk.Label(self.sh_obj.main_window, text=str(info)).pack()
                #print(self.cursor) #__repr__())
                char = Terminal.get_arrow_key() 
                #if char is None:
                #    char = Terminal.get_keypress()  # make a method that can
                if char in ('h', 'left'):                 #    get chars or arrows
                    if self.cursor[0] > self.domain[0]:
                        self.cursor[0] -= 1
                    else:
                        self.cursor[0] = self.domain[1]
                    #self.cursor[0] += -1 if self.cursor[0] > self.domain[0]\
                    #                  else self.size
                elif char in ('l', 'right'):
                    if self.cursor[0] < self.domain[1]:
                        self.cursor[0] += 1
                    else:
                        self.cursor[0] = self.domain[0]                  
                    ##if self.size % 2 == 0:
                    ##    self.domain[1] += 1
                    #self.cursor[0] += 1 if self.cursor[0] < self.domain[1]\
                    #                  else -self.size
                    ##if self.size % 2 == 0:
                    ##    self.max_domain += 1
                elif char in ('j', 'down'):
                    #self.cursor[1] += -1 if self.cursor[1] > self.domain[0]\
                    #                  else self.size
                    if self.cursor[1] > self.domain[0]:
                        self.cursor[1] -= 1
                    else:
                        self.cursor[1] = self.domain[1]                                      
                elif char in ('k', 'up'):
                    #self.cursor[1] += 1 if self.cursor[1] < self.domain[1]\
                    #                  else -self.size
                    if self.cursor[1] < self.domain[1]:
                        self.cursor[1] += 1
                    else:
                        self.cursor[1] = self.domain[0]                                      
                elif char == 'b':
                    self.plot_point(self.cursor[0], self.cursor[1], 'black')
                elif char == 'w':
                    self.plot_point(self.cursor[0], self.cursor[1], 'white')
                elif char == 'x' or char == '\x7f':
                    self.plot_point(self.cursor[0], self.cursor[1], 'empty')
                elif char == '*':
                    self.plot_point(self.cursor[0], self.cursor[1], 'star')

            except KeyboardInterrupt:
                Terminal.unhide_cursor()
                Terminal.output('')
                break


     ############
     #  POINTS  #
     ############
    def color_chooser(self):
        """
        set the point's color tag
        """
        colors = ['black', 'white', 'empty', 'star']
        if self.sh_obj.interface == 'term':
            return Terminal.make_page(
                'color-chooser', str(self) + '\nPress Ctrl-c to cancel',
                self.prompt_color)
        else:
            opt_no = self.sh_obj.list_menu(
                PlainList(colors), 'Choose a color', 'Color Chooser')
            index = opt_no - 1
            return colors[index]

    def prompt_color(self):
        """
        Prompt the user to choose a color; this should be in a go_stone class
        """
        choice = -1
        while choice not in ('b', 'w', 'x', '*'):
            choice = self.sh_obj.get_keypress(
                '\nPick up a color\n(b=black, w=white, x=erase, *=star)')
        color_dict = {
            'b': 'black',
            'w': 'white',
            'x': 'empty',
            '*': 'star'
            }
        return color_dict[choice]

    def prompt_point(self, color):
        """
        Prompt user for x,y coordinates and plot point.
        """
        pair_x, pair_y = tuple(eval(self.sh_obj.input('(x, y):')))
        self.plot_point(pair_x, pair_y, color)

    def plot_point(self, x_val, y_val, color='black'):
        """
        Plot a point of specified color at x, y
        """
        if color == 'empty':
            self.erase_point(x_val, y_val)
        elif x_val >= self.domain[0] and x_val <= self.domain[1] and\
             y_val >= self.domain[0] and y_val <= self.domain[1]:

            #WHAT'S THE ERROR?
            if color in ('black', 'white', 'star'):
                self.plane[int(round(x_val) - self.domain[0])][int(
                    self.domain[1] - round(y_val))].marker = color

    def erase_point(self, x_val, y_val):
        """
        Erase point at x, y.
        """
        x_val, y_val = int(round(x_val)), int(round(y_val))

        #if self.is_hoshi(x_val, -y_val):
        #    self.plane[x_val + self.max_domain][-y_val +\
        #        self.max_domain].marker = 'hoshi'
        #el
        indices = self.point_to_indices(Point(x_val, y_val))
        if (x_val != 0) and (y_val != 0):
            self.plane[indices[0]][indices[1]].marker = 'empty'
        elif (x_val == 0) and (y_val != 0):
            self.plane[indices[0]][indices[1]].marker = 'y_axis'
        elif (y_val == 0) and (x_val != 0):
            self.plane[indices[0]][indices[1]].marker = 'x_axis'
        else:
            self.plane[indices[0]][indices[1]].marker = 'origin'

    def print_points(self):
        """
        Print the graph as a table of ordered pairs.  Used for debugging or non-
        Euclidean space.
        """
        for v_val in range(self.size):
            for h_val in range(self.size):
                txt_str = self.plane[h_val][v_val].__repr__()
                if self.pt_at_cursor() is not None and\
                   self.plane[h_val][v_val] == self.pt_at_cursor():
                    txt_str = '>%s<' % txt_str
                easycat.write('{:>15} '.format(txt_str))
            Terminal.output('')

    def pt_at_cursor(self):
        """
        returns Point object where cursor is located
        """
        if self.domain[0] <= self.cursor[0] <= self.domain[1] and\
           self.domain[0] <= self.cursor[1] <= self.domain[1]:

            # not sure what this error is about.
            # this is an overly-lazy fix.
            indices = self.point_to_indices(Point(*self.cursor))
            #print(self.plane[indices[0]][indices[1]])
            return self.plane[indices[0]][indices[1]]

    def indices_to_point(self, index1, index2):
        """Maybe the reverse would be more useful.
        Also, give it the ability to take either
        a tuple or pair of args.
        """
        return Point(index1 + self.domain[0], self.domain[1] - index2)

    def point_to_indices(self, point):
        return int(point.x - self.domain[0]), int(self.domain[1] - point.y)

    
     #################
     #  POLYNOMIALS  #
     #################
    def list_functs(self):
        """
        Currently lists all attached polynomials; add ability to list
        'auto-shapes, etc.'
        """
        enum = Enumeration(self.fx_list, 'attached functions')
        # fix this in terminal class
        if self.sh_obj == 'term':
            Terminal.output(enum)
            self.sh_obj.wait()
        else:
            # change this
            self.sh_obj.wait(str(enum))

    def add_polynomial(self):
        """
        Use the Polynom.wizard() and attach result to the goban
        """
        try:
            color = self.color_chooser()
            f_x = Polynom([])
            f_x.wizard(sh_class=self.sh_obj)

            # Attach function
            if self.sh_obj == 'term':
                self.sh_obj.text_splash(
                    'Preview goes here', flashes=3, duration=.5)
                self.sh_obj.output("\nAttach '{}'?".format(f_x))
                ans = self.sh_obj.get_keypress()
            else: ans = 'y'
            if ans == 'y' and color != -1:
                self.plot_funct(f_x, color)
                self.fx_list.append(f_x)
        except (KeyboardInterrupt, OverflowError):
            pass

    def plot_funct(self, funct_a, color):
        """
        Any numerical function will do:
        native python functions, Polynom objects, or whatever....
        """
        self.funct_cnt += 1
        for var in range(self.domain[0], self.domain[1] + 1):
            try:
                self.plot_point(var, int(round(funct_a(var))), color)
            except (TypeError, ValueError):
                continue

     ############
     #  SHAPES  #
     ############
    def prompt_circle(self, color):
        """
        Prompt user for specifications and draw circle
        """
        radius = float(self.sh_obj.input('radius: '))
        # center = 0, 0
        center = tuple(eval(self.sh_obj.input('center (x, y): ')))  # safe?
        self.add_ellipse(radius, radius, color, (float(center[0]), float(
            center[1])))

    def prompt_ellipse(self, color):
        """
        Prompt user for attributes and draw ellipse
        """  # shoudl a Point object be used here?
        semiaxes = tuple(eval(self.sh_obj.input('semiaxes (H, V): ')))
        center = tuple(eval(self.sh_obj.input('center (x, y): ')))
        self.add_ellipse(float(semiaxes[0]), float(semiaxes[1]), color, (float(
            center[0]), float(center[1])))

    def add_ellipse(self, semiaxis_a=None, semiaxis_b=None, color='black',
                    center=(0, 0)):
        """
        draw ellipse on the plane; use a Point object instead of a tuple
        """
        if semiaxis_a is None:  # make sure this works
            semiaxis_a = self.max_domain
        if semiaxis_b is None:  # make sure this works
            semiaxis_b = semiaxis_a
        self.funct_cnt += 1
        for x_val in range(-self.domain[1], self.domain[1] + 1):
            try:
                self.plot_point(x_val, int(center[1] + round(math.sqrt(
                    semiaxis_b ** 2 - semiaxis_b ** 2 * (x_val - center[0]) **
                    2 / semiaxis_a ** 2))), color)
            except ZeroDivisionError:
                pass
            except ValueError:
                pass
            try:
                self.plot_point(x_val, int(center[1] - round(math.sqrt(
                    semiaxis_b ** 2 - semiaxis_b ** 2 * (x_val - center[0]) **
                    2 / semiaxis_a ** 2))), color)
            except ZeroDivisionError:
                pass
            except ValueError:
                pass

    def prompt_wave(self, color):
        """
        Prompt user for attributes, and draw sine wave on plane.
        """
        self.add_sinewave(
            float(self.sh_obj.input('wavelength: ')),
            float(self.sh_obj.input('amplitude: ')),
            float(self.sh_obj.input('h_shift: ')),
            color)

    def add_sinewave(self, wlength=None, amplitude=None, h_shift=0,
                     color='black'):
        """
        Draw sine wave onto plane.
        """
        if wlength is None:
            wlength = (2 * self.max_domain)
        if amplitude is None:
            amplitude = self.max_domain
        for x_val in range(-1 * self.max_domain, self.max_domain + 1):
            try:
                self.plot_point(
                    x_val,
                    int(round(amplitude * math.sin(
                        2.0 * x_val * math.pi / wlength - (h_shift/math.pi)))),
                    color)
            except ZeroDivisionError:
                pass


     ###########
     #  FILES  #
     ###########
    def write_sgf(self, basename):
        """
        Save the current board position as SGF.
        """
        #header = {'GM':1, 'SZ':self.BOARD_SIZE, 'KM':6.5}

        #Generate string
        sequence_list = []
        for cols in range(self.size):
            for rows in range(self.size):
                # this could be improved
                if self.plane[rows][cols].marker == 'white':
                    sequence_list.append(' AW[%s%s]' % (chr(rows+97), chr(cols+97)))
                elif self.plane[rows][cols].marker == 'black':
                    sequence_list.append(' AB[%s%s]' % (chr(rows+97), chr(cols+97)))

        #Write to file
        sequence = ''.join(sequence_list)
        if sys.version_info.major == 3:
            self._save(
                basename,
                'sgf',
                lambda f: f.write(
                    bytes('(;GM[1] SZ[{}] KM[6.5] AP[go_test.py] {} ;)'.format(
                        self.size, sequence), 'UTF-8')))
        elif sys.version_info.major == 2:
            self._save(basename, 'sgf', lambda f: f.write(
                '(;GM[1] SZ[{}] KM[6.5] AP[go_test.py] {} ;)'.format(
                    self.size, sequence)))

    def save_skin(self, basename):
        """
        Save skin as JSON
        """  # error
        #return_val = self._save(basename, 'json', lambda: json.dump(
        #    self.skin_dict, basename + '.json', indent=2))
        # try:
        json.dump(self.skin_dict, basename + '.json', indent=2)
        # except:  # No idea what kind...
        #    return -1
        # else:         # ? ?
        return 0  # ? purely a guess
