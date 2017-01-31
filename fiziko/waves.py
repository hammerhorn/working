#!/usr/bin/env python
#coding=utf8
"""
Classes 'Wave', 'SoundWave', 'EMWave'
"""
#import decimal
import math

from fiziko.kinematics import Disp, Velocity
from fiziko.scalars import Scalar, Unit
from things import Thing

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

SPEED_OF_LIGHT = 3e8
SPEED_OF_SOUND = 343.0  # Depends on factors like temperature, et al,
                        # if you want to complicate things.
PLANCK_H = 6.626e-34


class Wave(Thing):
    """
    Generic Wave object
    """
    def __init__(self, spd, freq):
        super(Wave, self).__init__()
        self.freq = Scalar(freq, Unit('Hz'))
        self.speed = Velocity(spd)
        f_wlength = self.speed.mag / self.freq.mag
        self.wlength = Disp(f_wlength)
        #self.wave_tuple = freq, speed, wlength

    def __str__(self):
        """
        was having trouble with Disp.to_scalar() so i did this ugly thing :-/
        """
        return '{}{{ f={}; λ={}; c={} }}\n'.format(
            self.label, self.freq, '{:.5g}'.format(
                self.speed.mag / self.freq.mag).lower() + ' m',
            self.speed.to_scalar())


class SoundWave(Wave):
    """
    SoundWave object; basis for cjh.music.Pitch, etc. ...
    """
    def __init__(self, f):
        super(SoundWave, self).__init__(SPEED_OF_SOUND, f)


class EMWave(Wave):
    """
    Electromagnetic Waves
    """

    def __init__(self, magnitude, unit_obj):
        if unit_obj.abbrev == 'Hz':
            super(EMWave, self).__init__(SPEED_OF_LIGHT, magnitude)
        self.label = self.emr_type()

    def __str__(self):
        """
        A lot of str manip until i can get Scalar to work properly
        """
        return super(EMWave, self).__str__()[:-16] + '; E={:.5g} J }}'.format(
            float(self.freq.mag) * PLANCK_H)

    def emr_type(self):
        """
        returns a string describing the type of radiation
        """
        wavelength = self.wlength.meters().mag
        if wavelength < 3.0e-7:
            type_str = 'x-ray/gamma ray'
        elif wavelength < 4.0e-7:
            type_str = 'ultraviolet ray'
        elif wavelength < 4.2e-7:
            type_str = 'violet light'
        elif wavelength < 4.4e-7:
            type_str = 'indigo light'
        elif wavelength < 5.0e-7:
            type_str = 'blue light'
        elif wavelength < 5.2e-7:
            type_str = 'cyan light'
        elif wavelength < 5.65e-7:
            type_str = 'green light'
        elif wavelength < 5.9e-7:
            type_str = 'yellow light'
        elif wavelength < 6.25e-7:
            type_str = 'orange light'
        elif wavelength < 7.0e-7:
            type_str = 'red light'
        elif wavelength < 1.4e-6:
            type_str = 'near-infrared'
        else:
            type_str = 'radio wave/microwave'
        return type_str


def kelvin_to_rgb(kelvins):
    temp = float(kelvins) / 100.0

    #red
    if temp < 66:
        red = 255
    else:
        red = temp - 55
        red = 351.97690566805693 + 0.114206453784165 * red +\
            -40.25366309332127 * math.log(red)
        if red < 0:
            red = 0
        elif red > 255:
            red = 255

    #green
    if temp <= 66:
        green = temp - 2
        green = -155.25485562709179 - 0.44596950469579133 * green + \
            104.49216199393888 * math.log(green)
    else:
        green = temp - 50
        green = 325.4494125711974 + 0.07943456536662342 * green - \
            28.0852963507957 * math.log(green)

    if green < 0:
        green = 0
    elif green > 255:
        green = 255

    #blue
    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = temp - 10
        blue = -254.76935184120902 + 0.8274096064007395 * blue + \
            115.67994401066147 * math.log(blue)
        if blue < 0:
            blue = 0
        elif blue > 255:
            blue = 255
   #print '{{red={}, green={}, blue={}}}'.format(red, gre
    red = int(round(red))
    green = int(round(green))
    blue = int(round(blue))
    return red, green, blue

