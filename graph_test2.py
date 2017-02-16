#!/usr/bin/env python
import atexit
import os
import time

from cjh.maths.geometry import Graph
from ranges import gen_range
from versatiledialogs.terminal import Terminal
from versatiledialogs.lists import PlainList

DELTA_T = 0.001

VT = Terminal()
atexit.register(Terminal.unhide_cursor)
#Terminal.clear()
skin_list = os.listdir('__data__/skins/')
skin = skin_list[VT.list_menu(PlainList(skin_list)) - 1]
Terminal.hide_cursor()



for color_ in ('black', 'white', 'star', 'empty'):
 #   Terminal.clear()
    #    Terminal.clear(19)
#    figure = Graph(size=1, skinfile=skin)
    

    for size_ in gen_range(1, 20):
        Terminal.clear()
        VT.output(''.join((
            'Skin is ', skin, '\nSize is ', str(size_), '\n\n', color_.upper(), '\n' * 5)))


        time.sleep(0.5)
        figure = Graph(size=size_, skinfile=skin)
        figure.fill(color_)
        Terminal.output(figure)
        time.sleep(DELTA_T)
  #      Terminal.clear(size_ + 7)

    time.sleep(DELTA_T)

Terminal.output('')

