#!/usr/bin/env python
#coding=utf8
"""
Parent class for all shell template objects in this package.
Stores data about the system and common methods for user interaction.
"""

import abc
import os
import pickle
import platform
import sys
import time

from termcolor import colored
try:
    import tkFileDialog
except ImportError:
    try:
        import tkinter.filedialog as tkFileDialog
    except ImportError:
        pass

from versatiledialogs.lists import PlainList

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Shellib(object):
    """
    Intended as an abstract parent class.  Common methods needed by ANY shell,
    graphical OR text-based.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        Initialize class (i.e., static) variables
        """
        self.__class__.os_name = os.name
        self.__class__.platform = platform.system()
        self.__class__.py_version = sys.version_info.major
        (self.__class__.kernel,
            self.__class__.hostname,
            self.__class__.release,
            self.__class__.machine,
            self.__class__.processor) = platform.uname()[:5]

        #If android os, change str platform from 'linux' to 'android'.
        global android
        try:
            import androidhelper as android
            self.__class__.platform = 'android'
        except ImportError:
            try:
                import android
                self.__class__.platform = 'android'
            except ImportError:
                pass


    @classmethod
    def emphasis(cls, in_str):
        if cls.interface == 'term' and cls.os_name == 'posix':
            out_str = cls.fx('bn', in_str)
        else: out_str = in_str.upper()
        return out_str
                       

    @classmethod
    def is_first_run(cls):
        """
        Returns True if this is the current script's first run; otherwise,
        returns False.
        """
        filename = sys.argv[0].split('/')[-1].split('.')[0]+ '.tmp'
        if cls.platform == 'Windows':  # does this hurt anything if it
                                       # runs in posix?
            filename = filename.split('\\')[1]
        if filename not in os.listdir(os.getcwd()):
            try:
                _file = open('__data__/' + filename, 'w')
                _file.close()
            except IOError:
                cls.output('unable to write to file system')
            return True
        else:
            return False

    @classmethod
    def view_info(cls, get_str=False):
        """
        Displays contained system info, formatted nicely.
        """
        minor_release = 'Python {}.{}'.format(
            cls.py_version, sys.version_info.minor)
        wxh = '{} x {}'.format(cls.width(), cls.height())
        dict_ = {'OS': cls.os_name,
             'platform': cls.platform,
             'version': minor_release,
#             'term/screen size': wxh,
             'kernel': cls.kernel,
             'hostname': cls.hostname,
             'release': cls.release,
             'machine': cls.machine,
             'processor': cls.processor}
        if cls.interface == 'Tk':
            dict_.update({'screen size':wxh})
        elif cls.interface in ['term', 'dialog']:
            dict_.update({'term size':wxh})
        keys_ = dict_.keys()
        keys_ = sorted(keys_)
        length = max([len(i) for i in keys_])
        fmt_str = '{:>' + str(length) + '}: {}'
        string = '\n'
        for value in keys_:
            string += (fmt_str.format(value, dict_[value]) + '\n')
        string = string.rstrip()
        if get_str == True:
            return string
        else:
            cls.output(
                string + '\n', heading='Shell Info', width=500, height=250,
                x=0, y=0)

    @abc.abstractmethod
    def welcome(self):
        pass

    @abc.abstractmethod
    def input(self, **kwargs):
        #return Ansi.strip_ansi(kwargs['prompt']).decode('utf8')
        pass

    @abc.abstractmethod
    def output(self):
        pass

    @abc.abstractmethod
    def outputf(self, msg=None, head=''):
        pass

    @abc.abstractmethod
    def message(self):
        pass


    ########
    # ARGS #
    ########
    current_arg_index = 1

    @classmethod
    def arg(cls, *prompt_list):
        """
        Looks for input on the command line.  If not found, promts user
        interactively.
        """
        if len(prompt_list) == 0:
            prompt_list = ('',)
            cls.output('No prompts given.')

        prompt_lengths = [len(prompt) for prompt in prompt_list]
        max_prompt_len = max(prompt_lengths)

        try:
            val = sys.argv[cls.current_arg_index]
            cls.current_arg_index += 1
            return val
        except IndexError:
            format_str = '{{:>{}}}'.format(max_prompt_len)
            if cls.current_arg_index - 1 == len(prompt_list):
                cls.current_arg_index = 1

            val = cls.input((format_str).\
                format(prompt_list[cls.current_arg_index - 1]))
            cls.current_arg_index += 1
            return val               


    ##################
    #  FILE ACTIONS  #
    ##################
    @classmethod
    def save_prompt(cls, filename, dir_name):
        """
        Confirm filename to save as.
        """
        cls.output('\n')
        response = cls.get_keypress("Save as {}'{}'? ".format(
            dir_name, filename))
        while response != 'y':
            if response == 'n':
                cls.output('')
                filename = cls.input('save to filename: ')
                break
        return filename

    @classmethod
    def open_p_file(cls, filename=None):
        """
        Loads a pickle file.  Prompts user for a file name if one is not
        provided.

        obj = cls.open_p_file()
        obj = cls.open_p_file(filename)
        """
        #if cls.interface in ['bash', 'sh']:
        #    cls.print_header('FILE: Open a pickle file')
        if filename != None:
            pass
        else:
            if cls.interface == 'Tk':
                filename = tkFileDialog.askopenfilename(
                    parent=cls.main_window, title='Choose a file', filetypes=[(
                    'Pickle files', '*.p')])
            else:
                file_list = os.listdir(os.getcwd())
                pickle_list = [_file for _file in file_list if _file.endswith(
                    '.p')]

                #Prompt user for a filename, if none given
                open_menu = PlainList(pickle_list)
                open_menu.label = 'Choose a file to open:'
                filename = pickle_list[cls.list_menu(open_menu) - 1]
        a_file = open(filename, 'rb')
        return pickle.load(a_file)

    @classmethod
    def report_filesave(cls, filename, fast=False, get_str=False):
        """
        Prints a brief message about size and modification date on a
        specified file.
        """
        stats = os.stat(filename)
        int_bytes = stats.st_size
        if int_bytes >= 1024:
            filesize_str = '{:.2g} kibibytes'.format(float(int_bytes) / 1024)
        else:
            filesize_str = '{} bytes'.format(int_bytes) 
        message = "'{}': {}, {}".format(
            filename, filesize_str, time.ctime(stats.st_ctime))

        if get_str is True:
            return colored(message, 'green')
        else:
        #elif cls.interface == 'SL4A' or fast is True:
            cls.output(colored(cls.notify(message, get_str=True), 'green'))
        if cls.interface != 'SL4A' and fast is False:
            cls.wait()
        #else:
        #    cls.message(message)

    @classmethod    
    def start_app(cls):
        filename = sys.argv[0].split('/')[-1].split('.')[0]+ '.tmp'        
        #try:
        _file = open('__data__/' + filename, 'w')
        _file.close()
        #except:
        #    cls.output('unable to write to file system')            
