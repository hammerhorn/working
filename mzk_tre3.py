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
    args = parser.parse_args() if __name__ == '__main__' else None
    return args


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

TONE_COUNT = find_tonecount()
HEADER = 'TONE ROW EDITOR'
MICROTONE_WARNING = """



     ABC, PS, and MIDI functions do not
     currently support microtones.
     Therefore these results are merely
     approximate.



""" + '\n' * (TONE_COUNT - 5)


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

def visualization_menu(row_, obj_str_):
    """
    Choose a visualization: tone-matrix, notename/frequency list, ABC notation
    If you are running X: pyplot, staff notation
    """
    menu_entries = [
        '..', 'Tone matrix (text-based)', 'Notenames, frequencies',
        'ABC notation']
    if 'DISPLAY' in os.environ:
        menu_entries += [
            'Pyplot         (X only)', 'Staff notation (X only)']
    view_menu = ListPrompt(menu_entries)

    if 12 % len(row_) != 0:
        obj_str_ = MICROTONE_WARNING

    while True:
        if SHELL.interface == 'term':
            pressed = TERM.make_page(
                'VISUALIZE', obj_str_, lambda: SHELL.list_menu(
                    view_menu))

        elif SHELL.interface == 'Tk':
            SHELL.main_window.title('VISUALIZE')
            SHELL.output(obj_str_)
            pressed = SHELL.list_menu(view_menu)

        if pressed == 1:
            break

        elif pressed == 2:
            obj_str_ = row_.draw(get_str=True)

        elif pressed == 3:
            obj_str_ = '\n' * 2 + row_.listfreqs(get_str=True) + '\n' * 4

        elif pressed == 4:
            obj_str_ = '\n'
            obj_str_ += row_.generate_abc_str().strip()
            k = len(row_) + 7 - len(obj_str_.split('\n'))
            obj_str_ += '\n' * k

        elif pressed == 5:
            row_.plot()

        elif pressed == 6:
            row_.write_abc_file()
            row_.abc2postscript()
            basename = row_.generate_basename()

            obj_str_ = '\n' * 9
            obj_str_ += '** {}.abc written **'.format(
                basename).center(TERM.width())
            obj_str_ += '\n'
            obj_str_ += '** {}.ps written **'.format(
                basename).center(TERM.width())
            obj_str_ += '\n' * 8

def midi_menu(row_, obj_str_):
    """
    Play midi file with timidity or audacious
    """
    menu_entries = ['..', 'Play MIDI     (timidity)']
    if 'DISPLAY' in os.environ:
        menu_entries += ['Play MIDI     (audacious, X only)']
    play_menu = ListPrompt(menu_entries)

    while True:
        if SHELL.interface == 'term':
            pressed = TERM.make_page(
                'PLAY AS MIDI', obj_str_,
                lambda: SHELL.list_menu(play_menu))
        elif SHELL.interface == 'Tk':
            SHELL.main_window.title('PLAY AS MIDI')
            SHELL.output(obj_str_)
            pressed = SHELL.list_menu(play_menu)
        if pressed == 1:
            break
        else:
            row_.write_abc_file()
            if pressed == 2:
                row_.play_midi()
            elif pressed == 3:
                row_.play_midi('audacious')

def transform_menu(row_, obj_str_):
    """
    transformations: retrograde, invert, rotate, transpose
    """
    trans_menu = ListPrompt(
        ['..', 'retrograde', 'invert', 'rotate', 'transpose'])
    while True:
        if SHELL.interface == 'term':
            pressed = TERM.make_page(
                'TRANSFORM', obj_str_,
                lambda: SHELL.list_menu(trans_menu))
        elif SHELL.interface == 'Tk':
            SHELL.main_window.title('TRANSFORM')
            SHELL.output(obj_str_)
            pressed = SHELL.list_menu(trans_menu)
        if pressed == 1:
            break
        elif pressed == 2:
            row_.reverse()
            obj_str_ = row_.draw(get_str=True)
        elif pressed == 3:
            row_.invert()
            obj_str_ = row_.draw(get_str=True)
        elif pressed == 4:
            row_.rotate()
            obj_str_ = row_.draw(get_str=True)
        elif pressed == 5:
            halfsteps = float(TERM.input('+'))
            row_.transpose(halfsteps)

def main():
    """
    Main function
    """
    # Data
    row = Tonerow(length=TONE_COUNT, sh_obj=SHELL)
    obj_str = row.draw(get_str=True)
    menu_obj = build_main_menu()
    main_func = lambda: SHELL.list_menu(menu_obj)
    trans_head = menu_obj.items[1]
    vmenu_head = menu_obj.items[2]
    midi_head = menu_obj.items[3]


    # Main Menu
    while True:
        if SHELL.interface == 'term':
            pressed = TERM.make_page(HEADER, obj_str, main_func)
        elif SHELL.interface == 'Tk':
            SHELL.main_window.title(HEADER)
            SHELL.output(obj_str)
            pressed = main_func()
        else: sys.exit('Sorry, {} is not supported'.format(SHELL.interface))

        if pressed == menu_obj.index('Play') + 1:
            row.play()
        elif pressed == menu_obj.index('Shuffle') + 1:
            row = Tonerow(length=TONE_COUNT, sh_obj=SHELL)
            obj_str = row.draw(get_str=True)
            continue
        elif pressed == menu_obj.index(vmenu_head) + 1:
            visualization_menu(row, obj_str)

        elif pressed == menu_obj.index(midi_head) + 1:
            midi_menu(row, obj_str)

        elif pressed == menu_obj.index(trans_head) + 1:
            transform_menu(row, obj_str)

        else:
            break

if __name__ == '__main__':
    main()
    SHELL.start_app()
