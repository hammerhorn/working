#!/usr/bin/env python3
#coding=utf8
"""
TONEROW EDITOR
"""
import argparse
import os
import sys

from cjh.misc import notebook
from cjh.tonerow import Tonerow
from ranges import gen_range
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
    return parser.parse_args() if __name__ == '__main__' else None


def find_tonecount():
    """
    return default value of 12, unless specified in command-line args
    """
    try:
        assert ARGS is not None and ARGS.length is not None
        val = int(ARGS.length)
    except (ValueError, AssertionError):
        val = 12
    return val


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
    if SHELL == 'Tk':
        SHELL.msg.config(font=('mono', 10, 'bold'))
        SHELL.center_window(width_=400, height_=300)

    notebook(REMARKS)

TONE_COUNT = find_tonecount()
HEADER = 'TONE ROW EDITOR'
MICROTONE_WARNING = ''.join(('\n' * 4,
"""     ABC, PS, and MIDI functions do not
     currently support microtones.
     Therefore these results are merely
     approximate.""", '\n' * (TONE_COUNT - 1)))

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

    # learn the dictionary comprehension
    for index in gen_range(1, 4):
        menu_list[index] = SHELL.emphasis(menu_list[index])

    return ListPrompt(menu_list)

def visualization_menu(row_, obj_str_):
    """
    Choose a visualization: tone-matrix, notename/frequency list, ABC notation
    If you are running X: pyplot, staff notation
    """
    menu_entries = [
        '..', 'Tone matrix (text-based)', 'Notenames, frequencies',
        'ABC notation']
    if 'DISPLAY' in os.environ:
        menu_entries.extend([
            'Pyplot         (X only)',
            'Staff notation (X only)'
        ])
    view_menu = ListPrompt(menu_entries)

    if 12 % len(row_) != 0:
        obj_str_ = MICROTONE_WARNING

    while True:
        if SHELL == 'term':
            pressed = TERM.make_page(
                'VISUALIZE', obj_str_, lambda: SHELL.list_menu(
                    view_menu))

        elif SHELL == 'Tk':
            SHELL.main_window.title('VISUALIZE')
            SHELL.output(obj_str_)
            pressed = SHELL.list_menu(view_menu)

        def align_abc_txt():
            """
            Align the ABC notation code on the screen
            with the right amount of space.
            """
            objstr = '\n' + row_.generate_abc_str().strip()
            objstr += '\n' * (len(row_) - objstr.count('\n') + 6)
            return objstr
            
        def create_postscript():
            """
            Generate the postcript-format staff notation
            """
            row_.write_abc_file()
            row_.abc2postscript()
            basename = row_.generate_basename()
            return ''.join((
                '\n' * 9,
                '** {}.abc written **'.format(basename).center(TERM.width()),
                '\n',
                '** {}.ps written **'.format(basename).center(TERM.width()),
                '\n' * 8
                ))

        views_dict = {
            2: lambda: row_.draw(get_str=True),
            3: lambda: ''.join(('\n' * 2, row_.listfreqs(get_str=True), '\n' * 4)),
            4: align_abc_txt,
            5: row_.plot,
            6: create_postscript
        }

        obj_str_ = views_dict.get(pressed, lambda: obj_str_)()
        if pressed == 1:
            break
    return obj_str_


def midi_menu(row_, obj_str_):
    """
    Play midi file with timidity or audacious
    """
    menu_entries = ['..', 'Play MIDI     (timidity)']
    if 'DISPLAY' in os.environ:
        menu_entries.extend(['Play MIDI     (audacious, X only)'])
    play_menu = ListPrompt(menu_entries)

    while True:
        if SHELL == 'term':
            pressed = TERM.make_page(
                'PLAY AS MIDI', obj_str_,
                lambda: SHELL.list_menu(play_menu))
        elif SHELL == 'Tk':
            SHELL.main_window.title('PLAY AS MIDI')
            SHELL.output(obj_str_)
            pressed = SHELL.list_menu(play_menu)
        if pressed == 1:
            break
        else:
            row_.write_abc_file()
            row_.play_midi('audacious' if pressed == 3 else 'timidity')

def transform_menu(row_, obj_str_):
    """
    transformations: retrograde, invert, rotate, transpose
    """
    trans_menu = ListPrompt(
        ['..', 'retrograde', 'invert', 'rotate', 'transpose'])

    # while True:    uncomment this line and the following break statement    #
                   #     if you want this menu to hang open      #

    if SHELL == 'term':
        pressed = TERM.make_page(
            'TRANSFORM', obj_str_,
            lambda: SHELL.list_menu(trans_menu))
    elif SHELL == 'Tk':
        SHELL.main_window.title('TRANSFORM')
        SHELL.output(obj_str_)
        pressed = SHELL.list_menu(trans_menu)

    transform_dict = {
        2: lambda: row_.reverse().draw(get_str=True),
        3: lambda: row_.invert().draw(get_str=True),
        4: lambda: row_.rotate().draw(get_str=True),
        5: lambda: row_.transpose(float(TERM.input('+')))
    }

    obj_str_ = transform_dict.get(pressed, lambda: obj_str_)()

    #  if pressed == 1:
    #      break

    return obj_str_

def main():
    """
    Main function
    """
    # Data
    row = Tonerow(length=TONE_COUNT, sh_obj=SHELL)
    obj_str = row.draw(get_str=True)
    menu_obj = build_main_menu()
    main_func = lambda: SHELL.list_menu(menu_obj)

    trans_head, vmenu_head, midi_head = menu_obj[1:4]

    # Main Menu
    while True:
        if SHELL == 'term':
            pressed = TERM.make_page(HEADER, obj_str, main_func)
        elif SHELL == 'Tk':
            SHELL.main_window.title(HEADER)
            SHELL.output(obj_str)
            pressed = main_func()
        else:
            sys.exit('Sorry, {} is not supported'.format(SHELL.interface))

        if pressed == menu_obj.index('Play') + 1:
            row.play()
        elif pressed == menu_obj.index('Shuffle') + 1:
            row = Tonerow(length=TONE_COUNT, sh_obj=SHELL)
            obj_str = row.draw(get_str=True)
            continue
        elif pressed == menu_obj.index(vmenu_head) + 1:
            obj_str = visualization_menu(row, obj_str)
        elif pressed == menu_obj.index(midi_head) + 1:
            midi_menu(row, obj_str)
        elif pressed == menu_obj.index(trans_head) + 1:
            obj_str = transform_menu(row, obj_str)
        else:
            break

if __name__ == '__main__':
    main()
    SHELL.start_app()
