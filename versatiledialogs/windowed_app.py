#!/usr/bin/env python
#coding=utf8
"""
Contains the WindowedApp class, for starting windowed applications
and using common dialogs.
"""
import os
import sys

from versatiledialogs.shell import Shellib

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class WindowedApp(Shellib):
    """
    This is the base class for classes TkTemplate and wxTemplate.
    It does nothing on its own.
    """

    def __init__(self, shell):
        """
        Create main window for graphical application.
        """
        super(WindowedApp, self).__init__()
        self.__class__.interface = shell
        #if __name__ == '__main__':
        self.declare_main_window()
            #self.create_menu()
        self.add_message_widget()

    @classmethod
    def declare_main_window(cls):#, width=500, height=25, x=0, y=400):
        """
        Returns the module name of __main__.
        """
        return sys.argv[0].split('/')[-1].split('.')[0]

    ##################
    # SHARED METHODS #
    ##################
    @classmethod
    def wait(cls, msg="'OK' to continue"):
        """
        Pops up a dialog that waits for a click from the user to continue.
        """
        cls.message(msg)

    @staticmethod
    def notify(msg):
        """
        Uses zenity and bash to provide notifications.
        """
        os.system('zenity --notification --timeout=1 --text "{}"'.format(msg))

    @classmethod
    def welcome(cls, script_name=sys.argv[0].split('/')[-1].split('.')[0],\
                description=''):#''): #, get_str=False):
        """
        On first run, pops up a dialog with a brief description of the script.
        """
        if cls.is_first_run():
            cls.message(description, script_name)

    @classmethod
    def start_app(cls):
        super(WindowedApp, cls).start_app()

    @classmethod
    def clear(cls):
        cls.output('')
