#!/usr/bin/env python
#coding=utf8
import time

import colortrans

from fiziko.waves import kelvin_to_rgb
import easycat
from versatiledialogs.terminal import Terminal


# def ansi_colorbox(color, colortype='ansi', tc_on=False):
#     """
#     Print a box of a certain ANSI color to the screen (0-255).
#     """
#     Terminal.clear(0)
#     easycat.write('  ')
#     write(15, 'ansi', 0, 'ansi', '{:>4}'.format(color), truecolor=tc_on)
#     write(color, colortype, color, colortype, ' ' * 16, truecolor=tc_on)
#     Terminal.output('')
#     for _ in range(9):
#         easycat.write('  ')
#         write(
#             color, 'ansi', color, 'ansi', ' ' * 20, truecolor=tc_on)
#         Terminal.output('')


def cycle_thru_ansiboxes(start=0, end=255, delta_t=0.25, tc=False):
    try:
        for i in range(start, end + 1):
            Color(i, 'ansi').draw_box(tc_on=tc, label_type='ansi')
            time.sleep(delta_t)
            if i != end:
                Terminal.cursor_v(10)
    except KeyboardInterrupt:
        Terminal.clear(0)


def color_ansi_to_hex(ansi_code):
    ansi_code = str(ansi_code)
    if len(ansi_code) == 1:
        ansi_code = ansi_code.zfill(2)
    return '#' + colortrans.short2rgb(ansi_code).upper()


def color_dec_to_hex(red, green, blue):
    hex_color_str = '#'
    hex_color_str += hex(red).split('x')[1].zfill(2)
    hex_color_str += hex(green).split('x')[1].zfill(2)
    hex_color_str += hex(blue).split('x')[1].zfill(2)
    hex_color_str = hex_color_str.upper()
    return hex_color_str


def color_hex_to_dec(hexstring):
    red = int(hexstring[1:3], 16)
    green = int(hexstring[3:5], 16)
    blue = int(hexstring[5:7], 16)
    return red, green, blue


def color_hex_to_ansi(hexstring):
    return int(colortrans.rgb2short(hexstring[1:])[0])

def nm_to_rgb(wavelength):
    gamma = 0.80
    intensity_max = 255
    factor = 1.0
    red, green, blue = 0, 0, 0
    if 380 <= wavelength < 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength < 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength < 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 -490)
    elif 510 <= wavelength < 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength < 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0

    elif 645 <= wavelength < 781:
        red = 1.0
        green = 0.0
        blue = 0.0

    #  Let the intensity fall off near the vision limits
    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)

    elif 420 <= wavelength < 701:
        factor = 1.0
    elif 701 <= wavelength < 781:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
    else:
        factor = 0.0

    red = int(round(red * factor ** gamma * intensity_max))
    blue = int(round(blue * factor ** gamma * intensity_max))
    green = int(round(green * factor ** gamma * intensity_max))
    return red, green, blue


def write(fgvalue, fgtype, bgvalue, bgtype, text, truecolor=False,
          get_str=False):
    out_str = '\x1b[38;'
    if fgtype.lower() == 'hex':
        if truecolor is True:
            out_str += '2;{};{};{}'.format(*color_hex_to_dec(fgvalue))
        else:
            fgvalue = color_hex_to_ansi(fgvalue)
            out_str += '5;{}'.format(fgvalue)
    else:
        out_str += '5;{}'.format(fgvalue)

    out_str += ';'

    if bgtype.lower() == 'hex':
        if truecolor is True:
            out_str += '48;2;{};{};{}'.format(*color_hex_to_dec(bgvalue))
#            print out_str
        else:
            bgvalue = color_hex_to_ansi(bgvalue)
            out_str += '48;5;{}'.format(bgvalue)
    else:
        out_str += '48;5;{}'.format(bgvalue)

    out_str += 'm{}\x1b[0m'.format(text)
    if get_str is True:
        return out_str
    else:
        easycat.write(out_str)


class Color(object):
    def __init__(self, value, color_type):
        if color_type == 'hex':
      	    #print color_type
            self.ansi = color_hex_to_ansi(value)
            self.hexstring = value
            self.kelvins = None
        elif color_type == 'ansi':
            if value < 10:
                self.ansi = str(value).zfill(2)
            else:
                self.ansi = value
            self.hexstring = color_ansi_to_hex(value)
            self.kelvins = None
        elif color_type == 'kelvin':
            self.kelvins = value
            dec_tuple = kelvin_to_rgb(value)
            self.hexstring = color_dec_to_hex(*dec_tuple)
            self.ansi = color_hex_to_ansi(self.hexstring)

        #elif color_type == 'freq':
        #    pass
        else:
            self.ansi, self.hexstring = None, None
        #self.hexstring = ''
        #self.ansi = 0
        #self.em_freq = 0
        return

    def __str__(self):
        out_str = '\n{} {}'.format('ANSI escape:', self.ansi)
        out_str += '\n{} {}'.format('RGB hexcode:', self.hexstring)
        if self.kelvins is not None:
            out_str += '\n{} {}K'.format(
                'color temperature:', self.kelvins)
        return out_str

    def draw_box(self, tc_on=False, label_type='hex'):
        """
        Print a box of a certain ANSI color to the screen (0-255).
        """
        Terminal.clear(0)
        easycat.write('  ')
        if label_type == 'ansi':
            caption = self.ansi
            spacing = 4, 16
        elif label_type == 'hex':
            caption = self.hexstring
            spacing = 8, 12
        elif label_type == 'kelvin':
            caption = self.kelvins
            spacing = 8, 12
        else: label_type = None
        
        write(15, 'ansi', 0, 'ansi', ('{:>' + str(spacing[0]) + '}').format(caption), truecolor=tc_on)
        write(self.hexstring, 'hex', self.hexstring, 'hex', ' ' * spacing[1], truecolor=tc_on)
        Terminal.output('')
        for _ in range(9):
            easycat.write('  ')
            write(self.hexstring, 'hex', self.hexstring, 'hex', ' ' * 20, truecolor=tc_on)
            Terminal.output('')
