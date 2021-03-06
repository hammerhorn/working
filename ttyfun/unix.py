#!/usr/bin/env python
#coding=utf8

import subprocess

from versatiledialogs.terminal import Terminal

class Figlet(object):
    def __init__(self, font='ascii9', color=None):
        self.font = font
        
        self.color = '' if color is None else color

    def __str__(self):
        command = 'toilet -f {} --{} '.format(self.font, self.color)
        return command

    def output(self, text, get_str=False):
        art_str = subprocess.check_output(
            self.__str__() + text, shell=True).decode('utf8')
        if get_str is True:
            return art_str
        else:
            Terminal.output(art_str)


class Cow(object):
    def __init__(self, cow_name):
        self.name = cow_name

    def __str__(self):
        out_str = subprocess.check_output(
            'cowsay -f {} " "'.format(self.name), shell=True)
        return out_str

    def output(self, text, get_str=False):
        out_str = subprocess.check_output(
            'cowsay -f {} "{}"'.format(self.name, text), shell=True)
        out_str = '\n' + out_str.decode('utf8')
        if get_str is True:
            return out_str
        else:
            Terminal.output(out_str)
