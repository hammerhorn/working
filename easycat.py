#!/usr/bin/env python3
#coding=utf8
"""
Collection of input/output functions which are similar to the cat
command
"""
import os
import pydoc
import sys

try:
    import colorama
    from termcolor import colored
except:
    pass

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
    keywords: files, quiet, return_list, return_str

    (This should be improved; re-write without **kwargs?)
    """
    def read_from_files(filelist):
        """
        Reads from files if any filenames given.
        """
        lines = []
        for file_ in filelist:
            filehandler = open(file_)
            lines.extend(filehandler.readlines())
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
                line = raw_input() if sys.version_info.major == 2 else input() # pylint: disable=bad-builtin
                line = line.rstrip()
                lines.append(line)
                if not ('quiet'in kwargs and kwargs['quiet'] is True):
                    write(line + '\n')
        except EOFError:
            pass

    if 'return_list' in list(kwargs.keys()) and \
       kwargs['return_list'] is True:
        return lines
    elif 'return_str' in list(kwargs.keys()) and \
         kwargs['return_str'] is True:
        string_list = []
        for line in lines:
            string_list.extend((line, '\n'))
        return ''.join(string_list)
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
        text_list = []
        for arg in args:
            text_list.extend([' ', str(arg)])
        text = ''.join(text_list)
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
    write(''.join((colored(src, attrs=['underline']),
                   ':\n',
                   get_src_str(src),
                   '\n')))


def write(text, stream=1):
    """
    Writes something to stdout, suppressing final endline.
    """
    if stream == 1:
        stream = sys.stdout
    elif stream == 2:
        stream = sys.stderr
    stream.write(text)
    stream.flush()
