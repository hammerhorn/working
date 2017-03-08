#!/usr/bin/env python
# coding: utf-8
"""
Provides a convenient interface for launching or editing scripts in pkg cjh.
"""
import argparse
import os
import subprocess
import sys

try:
    import Tkinter as tk
except ImportError:
    try:
        import tkinter as tk  # pylint: disable=F0401
    except ImportError:
        print('Unable to import Tk toolkit.')  # pylint: disable=C0325

from cjh.misc import notebook
from versatiledialogs.config import Config
from versatiledialogs.lists import PlainList
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'

REMARKS = """
    fix errors
    - does not work with zenity"""

def _parse_args():
    """
    Scan for --shell option and handle --help option.
    """
    parser = argparse.ArgumentParser(
        description="Run programs in various test environments.")
    parser.add_argument("-s", "--shell", type=str)
    parser.add_argument('-C', action='store_true')
    return parser.parse_args() if __name__ == '__main__' else None

def run_script(scriptname_, shellname_):
    """
    Run selected script in selected shell.
    """
    os.system('chmod +x {}'.format(scriptname_))
    scriptname_ = './' + scriptname_
    cmd_list = [scriptname_]
    original_shell = CONFIG.read_config_file()
    CONFIG.write_to_config_file(shell=shellname_)
    os.system('chmod +x {}'.format(scriptname_))
    if checked is not None and (SHELL.interface, checked.get()) == ('Tk', 1):
        cmd = [
            #word.encode('utf-8') for word
            word.encode('utf-8') for word
            in CONFIG.config_dict['terminal'].split()
        ]
        cmd.append(cmd_list)
        print(str(cmd))
        proc = subprocess.Popen(cmd) # , shell=True)
    else:
        proc = subprocess.Popen(cmd_list, shell=True)
    SHELL.output('')
    proc.wait()
    SHELL.wait()
    CONFIG.write_to_config_file(shell=original_shell)


def open_in_editor(scriptname_):
    """
    Open selected script in preferred editor.
    """
    #add properties to the class
    #if sh.interface == 'Tk':
        #val = menu1.curselection()
        #scriptname = script_list[val[0]]
    os.system('{} {}'.format(CONFIG.config_dict['editor'], scriptname_))


def setup_tk_window():
    """
    Declare/initialize all Tk objects which will be used.
    """
    global shellvar, menu1, checked

    SHELL.main_window.wm_title('Simple Script Runner')
    SHELL.center_window(width_=460, height_=400, y_offset=250)
    SHELL.msgtxt.set('Select a script and a shell.')
    SHELL.msg.config(font=('serif', 15, 'italic'), width=310)
    scriptvar = tk.StringVar(SHELL.main_window)
    scriptvar.set('-Choose a script-')

    menu1 = tk.Listbox(SHELL.main_window, height=20)
    menu1.focus_set()
    reversed_list = SCRIPT_LIST[::-1]
    for item in reversed_list:
        menu1.insert(0, item)
    menu1.select_set(0)
    menu1.pack(side=tk.LEFT, padx=20)

    cmd_frame = tk.Frame(SHELL.main_window)
    shellframe = tk.Frame(cmd_frame)
    shellvar = tk.StringVar(SHELL.main_window)
    shellvar.set('term')
    shell_label = tk.Label(shellframe, text="Select shell:")
    shell_label.pack(side=tk.LEFT)
    menu2 = tk.OptionMenu(shellframe, shellvar, *SHELL_LIST)
    menu2.pack(side=tk.TOP)
    shellframe.pack(side=tk.TOP)

    checked = tk.IntVar()
    check_frame = tk.Frame(cmd_frame, bd=2, relief='groove')

    argframe = tk.Frame(check_frame)
    args_label = tk.Label(argframe, text='args:')
    args_label.pack(side=tk.LEFT)
    entry = tk.Entry(argframe)
    entry.pack()
    argframe.pack(pady=20, padx=20)

    checkbox1 = tk.Checkbutton(
        check_frame, text='in a new terminal', variable=checked)
    checkbox1.pack(side=tk.TOP, fill=tk.X)
    checkbox2 = tk.Checkbutton(check_frame, state=tk.DISABLED, text='Python3')
    checkbox2.pack(side=tk.TOP, fill=tk.X)
    check_frame.pack(side=tk.LEFT, pady=20, ipady=10)
    cmd_frame.pack(side=tk.TOP, fill=tk.X)

    # buttonbar
    buttonbar = tk.Frame(SHELL.main_window)
    run_button = tk.Button(buttonbar, text='Run',
                           command=lambda: run_script(choose_file(SCRIPT_LIST),
                                                      select_shell(SHELL_LIST)))
    run_button.pack(side=tk.LEFT)
    edit_button = tk.Button(
        buttonbar, text='Edit',
        command=lambda: open_in_editor(choose_file(SCRIPT_LIST)))
    edit_button.pack(side=tk.LEFT)
    buttonbar.pack(side=tk.TOP)


def choose_file(script_list_):
    """
    Choose file to run.
    """
    if SHELL == 'Tk':
        val = menu1.curselection()
        scriptname_ = script_list_[val[0]]

    elif SHELL.interface in ('dialog', 'term'):
        listobj = PlainList(script_list_)
        script_menu = lambda: SHELL.list_menu(listobj)
        number = Terminal.make_page(func=script_menu)
        scriptname_ = script_list_[number - 1]
    return scriptname_


def select_shell(shell_list_):
    """
    Select shell to use.
    """
    if SHELL.interface in ('dialog', 'term'):
        listobj = PlainList(shell_list_)
        shell_menu = lambda: SHELL.list_menu(listobj)
        number = Terminal.make_page(func=shell_menu)
        shell_name_ = shell_list_[number - 1]
    elif SHELL == 'Tk':
        shell_name_ = shellvar.get().strip()
    return shell_name_


###############
#  CONSTANTS  #
###############

ARGS = _parse_args()
CONFIG = Config()
SHELL = CONFIG.launch_selected_shell(ARGS.shell) if ARGS is not None and\
        ARGS.shell is not None else CONFIG.start_user_profile()

notebook(REMARKS)

SCRIPT_LIST = [
    s for s in os.listdir(os.getcwd())
    if (s.endswith('py') and not (s.startswith('.') or s.startswith('_')))
]
SCRIPT_LIST.sort(key=str.lower)
SHELL_LIST = ('term', 'dialog', 'zenity', 'Tk', 'wx', '-None-')

if SHELL != 'Tk':
    MENU_OPTS = PlainList([
        '-script-', '-shell-', '-args-', '[RUN]', '[EDIT]', '[EXIT]'
    ])
    checked = None
#if SHELL == 'Tk':
else:
    setup_tk_window()
#else:
#    checked = None

def main():
    """Launch an interface, i.e., main loop."""
    if SHELL.interface in ('term', 'dialog', 'zenity'):
        while True:
            menu_func = lambda: SHELL.list_menu(MENU_OPTS)
            action = Terminal.make_page(func=menu_func)
            if action == 1:
                scriptname = choose_file(SCRIPT_LIST)
                MENU_OPTS.items[0] = scriptname
            elif action == 2:
                shell_name = select_shell(SHELL_LIST)
                MENU_OPTS.items[1] = shell_name
            elif action == 3:
                pass
            elif action == 4:
                try:
                    run_script(scriptname, shell_name)
                except KeyboardInterrupt:
                    continue
            elif action == 5:
                open_in_editor(scriptname)
            elif action == 6:
                sys.exit(0)

if __name__ == '__main__':
    main()
    SHELL.start_app()
