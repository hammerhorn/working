#!/usr/bin/env python3
#coding=utf8
"""
Simple C/C++/FORTRAN90 Interpreter/Interactive Code Runner

User can test lines of code, by inputting them and hitting EOF (^D or ^Z) to
compile and run bits of code on the fly.

This can be helpful for trying out and testing small bits of code.
"""
import argparse
import atexit
import os
import subprocess
import sys

from cjh.misc import catch_help_flag, notebook
import easycat
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - clear the screen with ^L/chr(12)
    - readline would be killer
    * This could become an IDE if you want to go that route"""

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments.
    """
    notebook(REMARKS)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--cpp', action='store_true', help='set language to C++')
    parser.add_argument(
        '--f90', action='store_true', help='set language to Fortran 90')
    parser.add_argument(
        '-C', action='store_true', help="view developer's comments")
    catch_help_flag(help_str=__doc__, argprsr=parser)
    return parser.parse_args() if __name__ == '__main__' else None


###############
#  CONSTANTS  #
###############
TERMINAL = Terminal()

if __name__ == '__main__':
    ARGS = _parse_args()

    if ARGS.f90 is True:
        if ARGS.cpp is True:
            sys.exit('Please choose one language.\n')
        else:
            EXTENSION = 'f90'
    elif ARGS.cpp is True:
        EXTENSION = 'cpp'
    else:
        EXTENSION = 'c'

def cleanup():
    """Remove temporary files."""
    for cleanup_file in ('tmp.' + EXTENSION, 'a.out'):
        try:
            os.remove(cleanup_file)
        except OSError:
            pass

atexit.register(cleanup)
notebook('')


##########
#  MAIN  #
##########
def main():
    """
    Preprocessor "include" statements are the only thing the interpreter
    remembers from previously-input commands.  ^C will discard all data, erase
    all data files, and end the program.
    """

    include_dict = {
        'f90': '',
        'cpp': '#include <iostream>\n',
        'c'  : '#include <stdio.h>\n'}

    startblock_dict = {
        'f90': 'PROGRAM Interactive\nIMPLICIT NONE\n',
        'c'  : 'int main(int argc, char* argv[])\n{\n',
        'cpp': 'using namespace std;\nint main(int argc, char* argv[])\n{\n'}

    prompt_dict = {
        'f90': '+',
        'cpp': '%%',
        'c': '%'}

    endblock_dict = {
        'f': 'END PROGRAM Interactive',
        'c': '\n\treturn 0;\n}'}

    compiler_dict = {
        'f90': 'gfortran',
        'c': 'gcc',
        'cpp': 'g++'}

    includes = include_dict[EXTENSION]

    try:
        while True:
            block = startblock_dict[EXTENSION]
            prompt = prompt_dict[EXTENSION]
            easycat.write(prompt)
            while True:
                try:
                    line = TERMINAL.input('', hide_form=True)
                    if line.startswith('#include'):
                        includes = ''.join((includes, line, '\n'))
                    else:
                        block = ''.join((block, '\t{}\n'.format(line)))

                except EOFError:
                    block = ''.join((block, endblock_dict[EXTENSION[0]]))
                    break

            filename = ''.join(('./tmp.', EXTENSION))

            with open(filename, 'w') as file_ptr:
                file_ptr.write('{}\n{}'.format(includes, block))

            command_list = [compiler_dict[EXTENSION]]
            if EXTENSION == 'c' and 'math.h' in includes:
                command_list.append(' -lm')
            command_list.extend((' ./tmp.', EXTENSION))
            command = ''.join(command_list)

            try:
                return_val = subprocess.check_call(command, shell=True)
            except subprocess.CalledProcessError:
                return_val = None

            if return_val == 0:
                proc = subprocess.Popen('./a.out', shell=True)
                proc.wait()

    except KeyboardInterrupt:
        easycat.write('\b\b\b')


if __name__ == '__main__':
    main()
