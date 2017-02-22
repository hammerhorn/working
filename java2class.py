#!/usr/bin/env python
#coding='utf8'
"""
Compile all JAVA source files into CLASS bytecode files
"""
import os
import subprocess
import sys

import easycat
from versatiledialogs.lists import PlainList
from versatiledialogs.terminal import Terminal, ListPrompt

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def process_file(classname):
    """
    attempt to compile filename.java -> filename.class
    If success, prints 'OK'; if fail, writes filename.errors
    """
    # Generate command string
    command = 'javac {0}.java 2> {0}.errors'.format(classname)

    # Verbose feedback for the user
    easycat.write(Terminal.fx('un', 'Compiling class '))
    easycat.write('<{}>'.format(classname))
    easycat.write(Terminal.fx('u', ': '))

    # Compile *.java -> *.class
    proc1 = subprocess.Popen(command, shell=True)
    proc1.wait()

    # Write *.errors file
    stats = os.stat('{}.errors'.format(classname))

    # If *.errors file is empty, delete it and print "OK"
    if stats.st_size == 0:
        proc2 = subprocess.Popen(
            'rm -f {}.errors'.format(classname), shell=True)
        proc2.wait()
        Terminal.output('OK')

    # Otherwise give an error message
    else:
        Terminal.output('[!] Errors/warnings detected (see {}.errors).'.format(classname))

    bytecode_name = '{}.class'.format(classname)

    # Report on 'Was the bytecode created?'
    if bytecode_name in get_file_list():
        easycat.write(Terminal.fx('bn', '[+] '))
        Terminal.output('Bytecode created.')
    else:
        easycat.write(Terminal.fx('bn', '[!] '))
        Terminal.output('Compilation aborted')


def get_file_list():
    """
    return all files in directory as sorted list
    """
    flist = os.listdir(os.getcwd())
    flist.sort()
    return flist


def logview_loop():
    """Navigate error logs using menus"""
    Terminal.clear()
    log_files = []
    for filename in get_file_list():
        if len(filename.split('.')) > 1:
            if filename.split('.').pop() == 'errors':
                log_files.append(filename.split('.')[0])

    log_files.reverse()
    log_files.append('-Main Menu-')
    log_files.append('-End Program-')
    log_files.reverse()

    err_menu = ListPrompt(log_files)
    while True:
        Terminal.clear()
        Terminal.output(Terminal.fx('u', 'View error logs:'))
        option = err_menu.input()
        if option == 1:
            sys.exit('Bye')
        elif option == 2:
            break
        else:
            easycat.less(file_='{}.errors'.format(log_files[option - 1]))


def menu_loop():
    """
    Runs the main menu and carries out selected actions
    """
    while True:
        Terminal.clear()
        selection = MAIN_MENU.input()
        if selection == 2:
            Terminal.clear()
            proc3 = subprocess.Popen('rm -f *.errors', shell=True)
            proc3.wait()
            file_list = get_file_list()
            for filename in file_list:
                if len(filename.split('.')) > 1:
                    if filename.split('.').pop() == 'java':
                        CLASS_LIST.append(filename.split('.')[0])
            for classname in CLASS_LIST:
                if classname + '.class' not in file_list or\
                   classname + '.errors' in file_list:
                    process_file(classname)
                    print
            Terminal.output('Pass complete.')
            Terminal.wait()
        elif selection == 3:
            logview_loop()
        else:
            sys.exit('Bye')


#################
# BEGIN PROGRAM #
#################
FILE_LIST = []
CLASS_LIST = []

OPTIONS = PlainList([
    '-End Program-', 'Compile all Java classes in the current directory',
    'View error logs'])
MAIN_MENU = ListPrompt(OPTIONS)

Terminal()

if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        CLASS_LIST = sys.argv[1:]
        for class_name in CLASS_LIST:
            FILE_LIST = get_file_list()
            if (class_name + '.java') not in FILE_LIST:
                sys.exit("Class '{}' not found.".format(class_name))
            Terminal.output('')
            proc4 = subprocess.Popen('rm -f {}.class'.format(class_name), shell=True)
            proc4.wait()
            # os.system('rm -f ' + classname + '.errors')
            process_file(class_name)
        Terminal.input('\nPass complete.\nPress <ENTER>.')

    menu_loop()
