#!/usr/bin/env python
#coding=utf8
"""
Contains the Angle class.
"""
import decimal
import math

from cjh.fiziko.scalars import Scalar  # , Unit
from cjh.letterator import Letter

from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Angle(Scalar):
    """
    Converts units and performs operations on angles.
    """

    letter_seq = Letter.caps_gen()

    def __init__(self, degrees=0.0, units_='deg', shell=Terminal()):
        self.units = None #?
        super(Angle, self).__init__(degrees, units_)
        self.shell_obj = shell
        if units_ == '(pi) rad':
            self.units.abbrev = 'π rad'
        self.label = u'∠ {}'.format(next(self.__class__.letter_seq))
        if Terminal.platform == 'Windows' and Terminal.interface == 'term':
            self.label = self.label.replace('∠', 'angle')

    def __add__(self, other):
        if self.units.label == 'degrees':
            degrees_flag = True
        else: degrees_flag = False
        my_sum = Angle(self.radians + other.radians, 'rad')
        if degrees_flag == True:
            self.deg()
            my_sum.deg()
        return my_sum

    def __mul__(self, multiplier):
        if self.units.label == 'degrees':
            degrees_flag = True
        else: degrees_flag = False
        prod = Angle(
            decimal.Decimal(self.radians) * decimal.Decimal(multiplier), 'rad')
        if degrees_flag == True:
            self.deg()
            prod.deg()
        return prod

    def __div__(self, divisor):
        if self.units.label == 'degrees':
            degrees_flag = True
        else: degrees_flag = False
        quot = Angle(decimal.Decimal(self.radians) / decimal.Decimal(divisor), 'rad')
        if degrees_flag == True:
            self.deg()
            quot.deg()
        return quot

    def __floordiv__(self, divisor):
        quot = self / divisor
        quot.mag = int(quot.mag)
        return quot

    def __eq__(self, other):
        if self.radians == other.radians:
            return True
        else: return False

    def __gt__(self, other):
        if self.radians > other.radians:
            return True
        else: return False

    def __ge__(self, other):
        if self.radians >= other.radians:
            return True
        else: return False

    def __lt__(self, other):
        if self.radians < other.radians:
            return True
        else: return False

    def __le__(self, other):
        if self.radians <= other.radians:
            return True
        else: return False

    def __str__(self):
        #if self.units.abbrev == 'deg':
        #    return '{:.4g}°'.format(self.mag)
        #else: return '{:.4g} {}'.format(self.mag, self.units.abbrev)
        if self.units.abbrev == 'deg' and not (Terminal.platform == 'Windows' and Terminal.interface == 'term'):
            return '{}°'.format(round(self.mag, 4))
        else:
            return '{} {}'.format(round(self.mag, 4), self.units.abbrev)

    def __repr__(self):
        #if Terminal.platform == 'Windows' and Terminal.interface == 'term':
        #    label = self.label.replace('∠', 'angle')
        #else:
        #    label = self.label
        return '{} {{{}}}'.format(self.label, self)

    @property
    def degrees(self):
        """
        returns a float
        """
        return float(self.deg().mag)

    @degrees.setter
    def degrees(self, deg):
        """
        takes a float
        """
        self.mag = decimal.Decimal(deg)
        self.units.name = 'deg'

    def deg(self):
        """
        Converts self to degrees and returns self.
        """
        if self.units.label == 'radians':
            self.mag = decimal.Decimal(math.degrees(self.mag))
            self.units.name = 'degrees'
        return self

    @property
    def radians(self):
        """
        returns a float
        """
        return float(self.rad().mag)

    @radians.setter
    def radians(self, rads):
        """
        takes a float
        """
        self.mag = decimal.Decimal(rads)
        self.units.name = 'rad'

    def rad(self):
        """
        Converts self to radians, and returns self.
        """
        if self.units.label == 'degrees':
            self.mag = decimal.Decimal(math.radians(self.mag))
            self.units.name = 'radians'
        return self

    @property
    def minutes(self):
        """
        Returns the total number of minutes as a float.
        """
        return float(decimal.Decimal(self.degrees) * decimal.Decimal(60.0))

    @minutes.setter
    def minutes(self, min_):
        """
        Define the angle by total number of minutes.
        """
        self.mag = decimal.Decimal(min_) / decimal.Decimal(60.0)
        self.units.name = 'deg'

    @property
    def seconds(self):
        """
        Returns the total number of seconds as a float.
        """
        return float(decimal.Decimal(self.degrees) * decimal.Decimal(3600.0))

    @seconds.setter
    def seconds(self, sec):
        """
        Define the angle by total number of seconds.
        """
        self.mag = decimal.Decimal(sec) / 3600.0
        self.units.name = 'deg'

    def degs_mins_secs(self):
        """
        Degrees, minutes, and seconds; as a formatted string
        """
        degs, mins, secs = self.tuple()
        return '''{}° {}' {:.5g}"'''.format(degs, mins, secs)

    def pi_radians(self):
        """
        Radians divided by PI
        """
        return Angle(self.radians / math.pi, '(pi) rad')

    def dual_format(self):
        """
        Degrees / radians
        """
        return str(Scalar(self.degrees, self.deg().units)) + ' / ' +\
            str(Scalar(self.radians, self.rad().units))

    def tuple(self):
        """
        Degrees, minutes, seconds; as a tuple
        """
        dms = []
        dms.append(self.degrees)
        dms.append(self.minutes % 60)
        #dms.append(decimal.Decimal(self.seconds) % decimal.Decimal(3600) -\
        #    decimal.Decimal(dms[1]) * decimal.Decimal(60))
        dms.append(self.seconds % 60)
        return (int(dms[0]), int(dms[1]), float(dms[2]))

    def slope(self):
        """
        returns float; returns None if no slope
        """
        if  decimal.Decimal(self.degrees) % decimal.Decimal(180) == 0.0:
            return 0.0
        elif decimal.Decimal(self.degrees) % decimal.Decimal(90) == 0.0:
            return None #"no slope"
        else: return round(math.tan(self.radians), 4)

    def slope_str(self):
        """
        Returns self.__str__() or the string 'no slope'.
        """
        slope_m = self.slope()
        if slope_m is None:
            return 'no slope'
        else: return '%g' % slope_m

    def compliment(self):
        """
        Returns the complimentary Angle object.
        """
        return Angle(decimal.Decimal(90) - decimal.Decimal(self.degrees), 'deg')

    def supplement(self):
        """
        Returns the supplementary Angle object.
        """
        return Angle(
            decimal.Decimal(180) - decimal.Decimal(self.degrees), 'deg')

    def summarize(self, get_str=False):
        """
        Print out a brief summary
        """
        string = u"""m = {}
[{}]

      {:7g}° = {:6.4g} (i.e., {:5.3g}π) radian(s)
-------------------------------------------------
comp: {:.5g}° = {:6.4g} (i.e., {:5.3g}π) radian(s)
supp: {:.5g}° = {:6.4g} (i.e., {:5.3g}π) radian(s)
""".format(\
        self.slope_str(), self.degs_mins_secs(),\
        self.degrees, self.radians, self.pi_radians().mag,\
        self.compliment().mag, self.compliment().radians,\
        self.compliment().pi_radians().mag,\
        self.supplement().mag, self.supplement().radians,
        self.supplement().pi_radians().mag)
        lines = [
            line.rstrip().center(Terminal.width()) + '\n'\
            for line in string.split('\n')
        ]
        string = ''
        for line in lines:
            string += line
        #self.shell_obj.output(string)
        out_str = string
        #self.shell_obj.output('sin = {}'.format(math.sin(self.radians)))
        out_str += 'sin = {}\n'.format(math.sin(self.radians))
        out_str += 'cos = {}\n'.format(math.cos(self.radians))
        out_str += 'tan = {}'.format(math.tan(self.radians))
        if get_str is True:
            return out_str
        else:
            self.shell_obj.output(out_str)
        #self.shell_obj.output('cos = {}'.format(math.cos(self.radians)))
        #self.shell_obj.output('tan = {}'.format(math.tan(self.radians)))
