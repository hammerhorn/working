#!/usr/bin/env python
#coding=utf8
"""
die-rolling simulator

Roll a single n-sided die.  Number of sides can be specified on the
command line; default is 6.
"""
import argparse
import atexit  # omg i'm so lazy
import sys

try:
    if sys.version_info.major == 2:
        import Tkinter as tk
    elif sys.version_info.major == 3:
        import tkinter as tk
except ImportError:
    sys.exit('Tk could not be loaded.  Ending program.')

from cjh.misc    import notebook
from cjh.statset import DataSet
from cjh.tablegames.die     import Die

from versatiledialogs.config   import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse Args
    """
    parser = argparse.ArgumentParser(
        description='Variable-sided die simulator.')
    parser.add_argument(
        '-C', action='store_true', help="developer's comments")
    parser.add_argument(
        '-q', '--quiet', help='suppress ascii art', action='count')
    parser.add_argument(
        '-d', '--sides', type=int, help='number of sides on the current die')
    parser.add_argument(
        '-a', '--anim', action='store_true',
        help='animated effect (command-line only)')
    parser.add_argument(
        '-s', '--shell', type=str, help='term, dialog, sh, Tk, zenity')
    parser.add_argument(
        '-k', '--keep', action='store_true',
        help="don't overwrite previous rolls")
    return parser.parse_args()


def roll_and_output():
    """
    Roll die and show result
    """
    global _toggle

    if SHELL.interface == 'Tk':
        SHELL.msg.config(font=('mono', 10, 'bold'))
    DIE.roll()
    if ARGS.quiet is not None and ARGS.quiet > 2:
        sys.exit(0)
    elif ARGS.quiet == 2:
        SHELL.output(DIE.value)
    elif ARGS.quiet == 1:
        SHELL.output(DIE.__str__())
    elif SHELL.interface == 'Tk':
        _toggle = not _toggle # make this into a generator
        if _toggle is True:
            SHELL.msg.config(fg='#FF00FF')#, bg='black')
        else: SHELL.msg.config(fg='chartreuse')#, bg='black')

        #if _toggle is True:
        #    SHELL.msg.config(fg='white', bg='black')
        #    SHELL.main_window.config(bg='black')
        #else:
        #    SHELL.msg.config(fg='black', bg='white')
        #    SHELL.main_window.config(bg='white')

        SHELL.msgtxt.set(DIE.draw_face(
            verbose=True, get_str=True, shellib=SHELL))
        SHELL.main_window.title(DIE)
    else:
        DIE.draw_face(verbose=True, shellib=SHELL)
    return DIE.value

##########
#  DATA  #
##########
if __name__ == '__main__':
    notebook("""
    - Pyplot histogram

    * Why not make a full Yahtzee or Craps game""")
    ARGS = _parse_args()
else:
    ARGS = None

CONFIG = Config()
if ARGS is not None and ARGS.shell is True:
    SHELL = CONFIG.launch_selected_shell(ARGS.shell)
else:
    SHELL = CONFIG.start_user_profile()
SHELL_NAME = SHELL.interface
LANG = CONFIG.get_lang_key()

atexit.register(SHELL.start_app)

def change_lang(lang_code):
    """DOCSTRING"""
    global LANG, MAIN_MENU
    LANG = lang_code
    BUTTON.config(text={'EN':'Roll', 'EO':'Ruligi'}[LANG])
    MAIN_MENU.destroy()
    MAIN_MENU = tk.Menu(SHELL.main_window, tearoff=0)
    lang_menu = tk.Menu(MAIN_MENU, tearoff=0)
    lang_menu.add_command(label='English', command=lambda: change_lang('EN'))
    lang_menu.add_command(label='Esperanto', command=lambda: change_lang('EO'))
    MAIN_MENU.add_cascade(
        label={'EN':'Language', 'EO':'Lingvo'}[LANG], menu=lang_menu)
    MAIN_MENU.add_command(
        label={'EN':'Exit', 'EO':'Eliri'}[LANG],
        command=SHELL.exit)
    SHELL.msg.config(
        width=150, font=('mono', 12, 'bold'), bg='black', fg='white')
    SHELL.msgtxt.set(
        {'EN':'Click to roll.', 'EO':'Klaku por ruligi.'}[LANG])
    SHELL.main_window.title({'EN':'dice', 'EO':'ĵetkuboj'}[LANG])

# Set up Tk window
if SHELL.interface == 'Tk':
    if LANG == 'EO':
        SHELL.main_window.title('ĵetkuboj')
    SHELL.main_window.config(bg='black')
    SHELL.msg.config(font=('mono', 12, 'bold'), bg='black', fg='white')
    SHELL.msgtxt.set(
        {'EN':'Click to roll.', 'EO':'Klaku por ruligi.'}[LANG.upper()])

    BUTTON = tk.Button(
        SHELL.main_window, text={'EN':"Roll", 'EO':'Ruligi'}[LANG.upper()],
        command=roll_and_output)
    BUTTON.config(
        underline=0, bg='black', fg='white', activeforeground='white',
        activebackground='black', relief=tk.FLAT, highlightcolor='white')
    BUTTON.pack(side='top')
    BUTTON.focus_set()

    MAIN_MENU = tk.Menu(SHELL.main_window, tearoff=0)
    lang_menu = tk.Menu(MAIN_MENU, tearoff=0)

    # english_checked = tk.IntVar()
    # esperanto_checked = tk.IntVar()
    # english = tk.Checkbutton(
    #     lang_menu, text='English', variable=english_checked)
    # esperanto = tk.Checkbutton(lang_menu, variable=esperanto_checked)

    lang_menu.add_checkbutton(
        label='English', command=lambda: change_lang('EN'))
    lang_menu.add_checkbutton(
        label='Esperanto', command=lambda: change_lang('EO'))

    MAIN_MENU.add_cascade(
        label={'EN':'Language', 'EO':'Lingvo'}[LANG], menu=lang_menu)
    MAIN_MENU.add_command(
        label={'EN': 'Exit', 'EO': 'Eliri'}[LANG],
        command=SHELL.exit)

#    menu.add_command(label='English')
#    menu.post(tk.event.x_root, tk.event.y_root)


def main_callback(event):
    """DoCstring"""
    # SHELL.main_window.focus_set()
    MAIN_MENU.tk_popup(event.x_root, event.y_root, 0)
    # print "clicked at", event.x, event.y
# frame = Frame(root, width=100, height=100)
# frame.bind("<Key>", key)
if SHELL.interface == 'Tk':
    SHELL.main_window.bind('<Button-3>', main_callback)
#frame.pack()

if SHELL_NAME in ['wx', 'Tk']:
    SHELL.center_window(width_=200, height_=200, x_offset=100)

if ARGS is not None and ARGS.sides is not None and ARGS.sides > 0:
    DIE = Die(ARGS.sides)
else: DIE = Die()
_toggle = False

def main():
    """
    In a text environment, roll one die with or without animation,
    according to command-line flags.  In Tk, run the main loop.
    """
    notebook('')
    value_list = []

    if SHELL_NAME != 'Tk':
        try:
            for _ in range(100):
                if SHELL_NAME in ['term', 'dialog', 'zenity']:
                    if ARGS is not None and ARGS.anim:
                        DIE.animate() # make this return a value
                    else:
                        value_list += [roll_and_output()]

                    Terminal.clear(1)
                    Terminal.output(str(value_list) + '\n') # write to titlebar
                                                            # for dialog &
                                                            # window styles
                Terminal.wait('Press a key, ^C to end and see stats')

                if ARGS.keep is False and ARGS.quiet is None:
                    Terminal.clear(11)

        except KeyboardInterrupt:
            Terminal.clear(1)
            Terminal.output('\n')
            Terminal.clear(2)
            Terminal.output('\r')
            data_set = DataSet(value_list)
            Terminal.output(data_set.averages_str())
            data_set.histogram()


if __name__ == '__main__':
    main()
