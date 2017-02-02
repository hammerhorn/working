#!/usr/bin/env python
#coding=utf8
"""
DOCSTRING
"""
import glob
import os

from versatiledialogs.terminal import Terminal, ListPrompt
import easycat
#from cjh.cli import Cli, ListPrompt
#from cjh.lists import ItemList

__author__ = 'Chris Horn'
__license__ = 'GPL'

class Fileman(object):
    """
    emulate basic unix-type file management commands
    """

    def __init__(self):
        Terminal()

    @classmethod
    def pwd(cls, getstr=False):
        """
        Emulate 'pwd' command
        """
        string = os.getcwd()
        if getstr:
            return string
        else:
            Terminal.output(string)

    @classmethod
    def commander(cls):
        """
        inspired by midnight commander
        """
        list_prompt = ListPrompt(['..'] + cls.list_files(opts=['B'], get_list=True))
        if len(list_prompt) > Terminal.height():
            easycat.less(str(list_prompt))
        response = Terminal.make_page(
            header=cls.pwd(getstr=True),
            func=list_prompt.input)
        if response == 1:
            os.chdir(list_prompt[response - 1])
            cls.commander()
        elif list_prompt[response - 1].endswith('/'):
            os.chdir(list_prompt[response - 1][:-1])
            cls.commander()
        else: return list_prompt[response - 1]

    @staticmethod
    def list_files(*args, **kwargs):
        """
        Emulate 'ls' command
        """
        file_list = []

        # if no args, add all files in dir to list
        if len(args) == 0:
            cwd = os.getcwd()
            file_list = os.listdir(cwd)

        # else, add the requested files
        else:
            for arg in args:
                file_list += glob.glob(arg)

        # if opts='B', filter out emacs backup files
        if 'opts' in kwargs and 'B' in kwargs['opts']:
            file_list = [
                file_ for file_ in file_list if not file_.endswith('~')
            ]

        # sort
        file_list.sort(key=str.lower)

        # opts='F' ->  'directory/', 'executable*'
        dir_list = []
        if 'opts' in kwargs and 'F' in kwargs['opts']:
            for index, file_ in enumerate(file_list):
                if os.path.isdir(file_):
                    dir_list.append(file_ + '/')
                    del file_list[index]
                elif os.access(file_, os.X_OK):
                    file_list[index] = file_ + '*'

        if 'get_list' not in kwargs or kwargs['get_list'] is not True:
            string = ''

            def create_list(items):
                """turn a Python list into a str with an item on each line"""
                list_str = ''
                for item in items:
                    list_str += (item + '\n')
                return list_str

            string += create_list(dir_list)
            string += create_list(file_list)

            if len(dir_list) + len(file_list) + 1 > Terminal.height():
                easycat.less(string)
            else:
                easycat.write(string.strip())
        else:
            return dir_list + file_list
