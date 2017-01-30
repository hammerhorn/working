#!/usr/bin/env python
#coding=utf8
"""
TONEROW EDITOR
"""
import argparse
import os
import sys

from cjh.misc import notebook
from cjh.tonerow import Tonerow

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal, ListPrompt

def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument(
        '-C', action='store_true', help="see developer's comments")
    parser.add_argument(
        '-n', '--length', help="notes/scale, row, etc....", nargs='?')
    if __name__ == '__main__':
        args = parser.parse_args()
    else: args = None
    return args


def build_main_menu():
    """
    Populate and return the main menu as a ListPrompt object
    """
    menu_list = [
        'Play',
        'Transform',
        'Visualize',
        'Play as MIDI',
        'Shuffle',
        'Quit (Ctrl-C)']
    for index in range(1, 4):
        menu_list[index] = SHELL.emphasis(menu_list[index])
    menu = ListPrompt(menu_list)
    menu_obj = menu
    return menu_obj


REMARKS = """
    - generate full 2-d matrix
    - the ability to input specific rows instead of generating them
    - Figure out how to write abc without all the redundant natural signs
    - Save as text
    - Save as audio file
    - Save and open pickle
    - Get to work with wx, dialog, zenity, sl4a, html, ....
    + Hide X features when there is no X
    + zeroth note should be down an octave
    + Fix Tk

    * Add animation to diagram and freq list (bouncing ball)"""

CONFIG = Config()
TERM = Terminal()
ARGS = _parse_args()
SHELL = CONFIG.launch_selected_shell('term')

if __name__ == '__main__':
    SHELL = CONFIG.start_user_profile()
    if SHELL.interface in ['Tk']:
        SHELL.msg.config(font=('mono', 10, 'bold'))
        SHELL.center_window(width_=400, height_=300)

    notebook(REMARKS)

def find_tonecount():
    """
    return default value of 12, unless specified in command-line args
    """
    try:
        if ARGS is not None and ARGS.length is not None:
            return int(ARGS.length)
        else: return 12
    except ValueError:
        return 12


TONE_COUNT = find_tonecount()
HEADER = 'TONE ROW EDITOR'
MICROTONE_WARNING = """
 
 
 
     ABC, PS, and MIDI functions do not
     currently support microtones.
     Therefore these results are merely
     approximate.
 
 
 
""" + '\n' * (TONE_COUNT - 5)

def main():
    """
    Main function
    """
    menu_obj = build_main_menu()
    main_func = lambda: SHELL.list_menu(menu_obj)

    row = Tonerow(length=TONE_COUNT, sh_obj=SHELL)
    obj_str = row.draw(get_str=True)#[1:-1]


    # trans_head
    # menu_obj.items[1] = emphasis(menu_obj.items[1])

    trans_head = menu_obj.items[1] # i need these mnemonics dammit....

    # vmenu_head
    # menu_obj.items[2] = emphasis(menu_obj.items[2])

    vmenu_head = menu_obj.items[2]


    # midi_head
    # menu_obj.items[3] = emphasis(menu_obj.items[3])

    midi_head = menu_obj.items[3]
 
    while True:
        if SHELL.interface == 'term':
            pressed = TERM.make_page(HEADER, obj_str, main_func)
        elif SHELL.interface == 'Tk':
            SHELL.main_window.title(HEADER)
            SHELL.output(obj_str)
            pressed = main_func()
        else: sys.exit('Sorry, {} is not yet supported'.format(SHELL.interface))

        if pressed == menu_obj.index('Play') + 1:
            row.play()
        elif pressed == menu_obj.index('Shuffle') + 1:
            # insert tonerow.c
            #in_str = subprocess.check_output('./tonerow', shell=True)
            #in_list = [int(i) for i in in_str.split()]
            row = Tonerow(length=TONE_COUNT, sh_obj=SHELL)
            obj_str = row.draw(get_str=True)#[1:-2]
            continue


#        elif pressed == menu_obj.index(emphasis('Visualize')) + 1:
        elif pressed == menu_obj.index(vmenu_head) + 1:
            menu_entries = [
                '..', 'Tone matrix (text-based)', 'Notenames, frequencies',
                'ABC notation']
            if 'DISPLAY' in os.environ:
                menu_entries += [
                    'Pyplot         (X only)', 'Staff notation (X only)']
            view_menu = ListPrompt(menu_entries)

            if 12 % len(row) != 0:
                obj_str = MICROTONE_WARNING

            while True:
                ##try:
                #pressed = TERM.make_page('VISUALIZE', obj_str, view_menu.input)
                if SHELL.interface == 'term':
                    pressed = TERM.make_page(
                        'VISUALIZE', obj_str, lambda: SHELL.list_menu(
                            view_menu))

                elif SHELL.interface == 'Tk':
                    SHELL.main_window.title('VISUALIZE')
                    SHELL.output(obj_str)
                    pressed = SHELL.list_menu(view_menu)


                ##except KeyboardInterrupt:
                ##    break
                if pressed == 1:
                    break

                elif pressed == 2:
                    obj_str = row.draw(get_str=True)#[1:-2]

                elif pressed == 3:
                    obj_str = '\n' * 2 + row.listfreqs(get_str=True) + '\n' * 4

                elif pressed == 4:
                    obj_str = '\n'#TERM.hrule(string=True)
                    obj_str += row.generate_abc_str().strip()
##                k = len(row) + 3 - len(obj_str)
                    k = len(row) + 7 - len(obj_str.split('\n'))
                    obj_str += '\n' * k #TERM.hrule(string=True)

                elif pressed == 5:
                    row.plot()

                elif pressed == 6:
                    row.write_abc_file()
                    row.abc2postscript()
                    basename = row.generate_basename()

                    obj_str = '\n' * 9
                    obj_str += '** {}.abc written **'.format(
                        basename).center(TERM.width())
                    obj_str += '\n'
                    obj_str += '** {}.ps written **'.format(
                        basename).center(TERM.width())
                    obj_str += '\n' * 8

        elif pressed == menu_obj.index(midi_head) + 1:

            #heading = 'PLAY MIDI'
            menu_entries = ['..', 'Play MIDI     (timidity)']
            if 'DISPLAY' in os.environ:
                menu_entries += ['Play MIDI     (audacious, X only)']
            play_menu = ListPrompt(menu_entries)
                
            while True:
                if SHELL.interface == 'term':
                    pressed = TERM.make_page(
                        'PLAY AS MIDI', obj_str,
                        lambda: SHELL.list_menu(play_menu))
                elif SHELL.interface == 'Tk':
                    SHELL.main_window.title('PLAY AS MIDI')
                    SHELL.output(obj_str)
                    pressed = SHELL.list_menu(play_menu)
                if pressed == 1:
                    break
                else:
                    row.write_abc_file()
                    if pressed == 2:
                        row.play_midi()
                    elif pressed == 3:
                        row.play_midi('audacious')
#
        elif pressed == menu_obj.index(trans_head) + 1:
            trans_menu = ListPrompt(
                ['..', 'retrograde', 'invert', 'rotate', 'transpose'])
            while True:
                if SHELL.interface == 'term':
                    pressed = TERM.make_page(
                        'TRANSFORM', obj_str,
                        lambda: SHELL.list_menu(trans_menu))
                elif SHELL.interface == 'Tk':
                    SHELL.main_window.title('TRANSFORM')
                    SHELL.output(obj_str)
                    pressed = SHELL.list_menu(trans_menu)
                if pressed == 1:
                    break
                elif pressed == 2:
                    row.reverse()
                    obj_str = row.draw(get_str=True)#[1:-2]
                elif pressed == 3:
                    row.invert()
                    obj_str = row.draw(get_str=True)#[1:-2]
                elif pressed == 4:
                    row.rotate()
                    obj_str = row.draw(get_str=True)#[1:-2]
                elif pressed == 5:
                    halfsteps = float(TERM.input('+'))
                    row.transpose(halfsteps)
#
        else:
            #print "pressed = " + str(pressed)
            break

if __name__ == '__main__':
    main()
