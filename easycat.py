#!/usr/bin/env python
#coding=utf8
"""
Collection of input/output functions which are similar to the cat command
"""
import os
import pydoc
import sys

import colorama
from termcolor import colored
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_for_filename
    from pygments.formatters.terminal import TerminalFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

def cat(**kwargs):
    """
    This should be improved; re-write without **kwargs?
    """
    def read_from_files(filelist):
        """
        Reads from files if any filenames given.
        """
        lines = []
        for file_ in filelist:
            filehandler = open(file_)
            lines += filehandler.readlines()
            filehandler.close()
        lines = [line.strip() for line in lines]
        return lines

    if 'files' in kwargs:
        lines = read_from_files(kwargs['files'])
    else:
        lines = []
        line = ''

        try:
            while True:
                if sys.version_info.major == 2:
                    line = raw_input()
                else:
                    line = input()  # pylint: disable=bad-builtin
                line = line.rstrip()
                lines += [line]
                write(line + '\n')
        except EOFError:
            pass

    if 'return_list' in list(kwargs.keys()) and \
       kwargs['return_list'] is True:
        return lines
    elif 'return_str' in list(kwargs.keys()) and \
         kwargs['return_str'] is True:
        string = ''
        for line in lines:
            string += (line + '\n')
        return string
    elif not ('quiet' in kwargs and kwargs['quiet'] is True):
        write('\n')
        for line in lines:
            write(line + '\n')

def emph(text):
    """
    returns '[[ some text ]]' as a str
    """
    return '[[ {} ]]'.format(text)


def get_src_str(file_=None, color=True):
    """
    Returns file as ANSI colored string
    color option depends on pygments library.
    """
    colorama.init()
    if file_ is None:
        file_ = sys.argv[0]
    handler = open(file_)
    code = handler.read()
    if (color and PYGMENTS_AVAILABLE) is True:
        lexer = get_lexer_for_filename(file_)
        color_string = highlight(code, lexer, TerminalFormatter())
        return color_string
    else:
        return code


def less(*args, **kwargs):
    """
    takes either:
         1) a str arg or
         2) file_=FILENAME
    """
    filename = kwargs.get('file_', None)
    if filename is not None:
        with open(filename, 'r') as file_handler:
            text = file_handler.read()            
    elif len(args) > 0:
        text = ''
        for arg in args:
            text += (' ' + str(arg))
        # text = text.lstrip('\n')

    if os.path.exists('/usr/bin/less'):
        pydoc.pipepager(text, cmd='less -R')
    else:
        # works for text, but not for colors
        pydoc.pager(text)


def view_source(src=sys.argv[0]):
    """
    Display source
    """
    write(colored(src, attrs=['underline']))
    write(':\n')
    write(get_src_str(src) + '\n')


def write(text):
    """
    Writes something to stdout, suppressing final endline.
    """
    sys.stdout.write(text)
    sys.stdout.flush()
