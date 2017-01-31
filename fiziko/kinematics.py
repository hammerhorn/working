#!/usr/bin/env python
#coding=utf8
"""
Perform addition with vectors, displacements, and velocities.
"""
import decimal
import math
import sys

from fiziko.scalars import Scalar, Unit
from cjh.maths.angles import Angle
from cjh.letterator import Letter

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

SPEED_C = 3e8

class Vector(Scalar):
    """
    Plain vector
    """
    letter_seq = Letter.caps_gen()

    def _resolve(self):
        """
        Break vector down into X and Y components.
        """
#        print 'resolving {}'.format(self.theta)
#        print 'which is {} in radians'.format(self.theta.radians)
        #print "self.theta is type {}".format(type(self.theta))
        #print type(self.theta)
        x_mag = decimal.Decimal(self.mag) * decimal.Decimal(math.cos(
            self.theta.radians))
        y_mag = decimal.Decimal(self.mag) * decimal.Decimal(math.sin(
            self.theta.radians))
        return x_mag, y_mag

    def __init__(self, mag, th=Angle()):
        super(Vector, self).__init__(mag)
        #if th == None: self.theta = Angle()
        #else:
        self.theta = th

        self.x_mag, self.y_mag = self._resolve()
        self.label = next(self.__class__.letter_seq)

    def __repr__(self):
        return '⟶  {{{}; {}}}'.format(Scalar(self.mag, self.units), self.theta)

    def __str__(self):
        mag_str = '{:10,.5g}'.format(self.mag)
        mag_str.rstrip('0')
        return '{} {} at {}'.format(mag_str, self.units, self.theta.deg())

    def __add__(self, addend):
        x_sum = self.x_mag + addend.x_mag
        y_sum = self.y_mag + addend.y_mag
        try:
            myvector1 = Vector(
                math.sqrt(x_sum ** 2 + y_sum ** 2), Angle(math.atan(
                y_sum / x_sum), 'rad'))
        except (ZeroDivisionError, DivisionUndefined):
            return Vector(0, Angle())
        if x_sum < 0.0:
            myvector1.mag *= decimal.Decimal(-1.0)
        if self.theta.units.label == 'degrees':
            myvector1.theta = myvector1.theta.deg()
        return myvector1

    def __mul__(self, mul_end):
        return Vector(self.mag * mul_end, self.theta)

    def __rmul__(self, mul_end):
        return Vector(self.mag * mul_end, self.theta)

    def to_scalar(self):
        """
        Return scalar part (no angle or direction).
        """
        return Scalar(self.mag, self.units)


class Disp(Vector):
    """
    displacement vector
    """
    def __init__(self, mag=0.0, th=Angle(0), u='m'):
        super(Disp, self).__init__(mag, th)
        self.label = "disp_{}".format(self.label)
        self.units = Unit(u)

    def __add__(self, addend):
        # if units of Angle are different, change both to degrees
        if self.theta.units != addend.theta.units:
            self.theta = self.theta.degrees()
            addend.theta = addend.theta.degrees()

        # if units of Disp are different, change both to meters
        if self.units != addend.units:
            self = self.meters()
            addend = addend.meters()

        # if self.theta.units == addend.theta.units and :
        x_sum = self.x_mag + addend.x_mag
        y_sum = self.y_mag + addend.y_mag

        try:
            myvector1 = Disp(math.sqrt(x_sum ** 2 + y_sum ** 2), th=Angle(
                math.atan(y_sum / x_sum), 'rad'), u=self.units.abbrev)
        except ZeroDivisionError:
            return Disp(0.0, self.units.abbrev, Angle(90))

        if x_sum < decimal.Decimal(0.0):
            myvector1.mag *= decimal.Decimal(-1.0)
        if self.theta.units.label == 'degrees':
            myvector1.theta = myvector1.theta.deg()
        return myvector1

    def __div__(self, divisor):
        pass

    def __mul__(self, mul_end):
        """This will need to be improved"""

        return Disp(self.mag * mul_end, self.theta, self.units.abbrev)


#    def __mul__(self, mul_end):
#        return Vector(self.mag * mul_end, self.theta)

    def __rmul__(self, mul_end):
        """This will need to be improved"""
        return Disp(self.mag * mul_end, self.units.abbrev, self.theta)

    def meters(self):
        """
        returns Disp object in meters
        """
        if self.units.label == 'feet':

            d = Disp(.3048 * float(self.mag), self.theta, 'm')
            #print d
            return d
        elif self.units.label == 'meters':
            return self
        elif self.units.label == 'inches' or\
            self.units.label == 'miles':
            return (self.feet()).meters()
        elif self.units.label == 'centimeters':
            return Disp(float(self.mag) / 100.0, self.theta, 'm')
        else:
            sys.exit("Sorry, I don't know how to convert from {}.".format(
                self.units.label))

    @property
    def nanometers(self):
        return float(self.mag) * 10e8

    def feet(self):
        if self.units.label == 'meters':
            return Disp(float(self.mag) / .3048, self.theta, 'ft.')
        elif self.units.label == 'feet':
            return self
        elif self.units.label == 'inches':
            return Disp(self.mag / 12.0, self.theta, 'ft.')
        elif self.units.label == 'miles':
            return Disp(self.mag * 5280.0, self.theta, 'ft.')
        else:
            sys.exit("Sorry, I don't know how to convert from {}.".format(\
                self.units.label))


    def inches(self):
        inches = self.feet() * 12
        inches.units = Unit('in.')
        return inches

    def miles(self):
        return Disp(self.feet().mag / decimal.Decimal(5280.0), 'mi.', self.theta)


class Velocity(Vector):
    def __init__(self, mag=0.0, u='m/s', th=Angle(0.0, 'deg')):
        super(Velocity, self).__init__(mag, th)
        self.units = Unit(u)
        if (self.mps()).mag > SPEED_C:
            self.mag = SPEED_C
            self.units = Unit('m/s')

    def __add__(self, addend):
        sum_ = Velocity(float(self.mps().mag + addend.mps().mag) / (1 + float(self.mps().mag * addend.mps().mag) / SPEED_C**2), 'm/s')
        if self.units.abbrev == 'mph':
            sum_ = sum_.mph()
        return sum_

    def __mul__(self, other):
        total = Velocity()
        for _ in range(other):
            total += self
        return total

    def mph(self):
        if self.units.abbrev == 'mph':
            return self
        elif self.units.abbrev == 'm/s':
            return Velocity(float(self.mag) * 2.2369363, 'mph', self.theta)
        else:
            sys.exit("Sorry, I don't know how to convert from {}.".format(
                self.units.label))

    def mps(self):
        if self.units.abbrev == 'm/s':
            return self
        elif self.units.abbrev == 'mph':
            return Velocity(float(self.mag) / 2.2369363, 'm/s', self.theta)
        else: sys.exit("Sorry, I don't know how to convert from {}.".format(
                self.units.label))

