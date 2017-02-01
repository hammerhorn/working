#!/usr/bin/env python
#coding=utf8
"""
Methods for dialogs and common actions with wxWidgets.
"""
#import sys

try:
    import wx
except ImportError:
    #print("Could not import module 'wx'.")
    pass

from versatiledialogs.windowed_app import WindowedApp

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class WxTemplate(WindowedApp):
    """
    Dialogs and common methods for wx.
    """

    def __init__(self):
        """
        Creates a plain application window.
        """
        print("Enter '__init__'")
        super(WxTemplate, self).__init__('wx')
        print("Exit '__init__'")
        
    @classmethod
    def declare_main_window(cls, width=500, height=25, x=0, y=400):
        mod_name = super(WxTemplate, cls).declare_main_window()
        cls.app = wx.App()
        cls.main_window = wx.Frame(None, -1, mod_name)
        height = 25
        cls.center_window(width_=width, height_=height, x_offset=x, y_offset=y)
        cls.main_window.Show()

    @classmethod
    def add_message_widget(cls):
        return

    @classmethod
    def create_menu(cls):
        cls.mainmenu = wx.MenuBar()
        cls.__create_exit_menu()
        cls.__create_language_menu()
        cls.main_window.SetMenuBar(cls.mainmenu)

    @classmethod
    def __create_exit_menu(cls):
        cls.quit_menu = wx.Menu()
        qitem = cls.quit_menu.Append(wx.ID_EXIT, 'Quit', 'Quit program')
        cls.mainmenu.Append(cls.quit_menu, '&File')
        cls.main_window.Bind(wx.EVT_MENU, cls.__onQuit, qitem)

    @classmethod
    def __create_language_menu(cls):
        cls.languagemenu = wx.Menu()
        litems = []
        litems.append(cls.languagemenu.Append(wx.NewId(), 'English (en)',\
            kind=wx.ITEM_RADIO))
        litems.append(cls.languagemenu.Append(wx.NewId(), 'Esperanto (eo)',\
            kind=wx.ITEM_RADIO))
        cls.mainmenu.Append(cls.languagemenu, '&Language')

    @classmethod
    def __onQuit(cls, event):
        cls.main_window.Close()

    @classmethod
    def start_app(cls):
        cls.app.MainLoop()

    @classmethod
    def center_window(
        cls, width_=400, height_=0, x_offset=0, y_offset=200, win=None):
        if win is None:
            win = cls.main_window
        win.Centre()
        win.SetSize((width_, height_))
        win.Move((y_offset, x_offset))

    @classmethod
    def input(cls): return

    @classmethod
    def message(cls, msg, heading=''):
        return

    @classmethod
    def output(cls, text, **kwargs): return

    @classmethod
    def outputf(cls): return    

    @classmethod
    def mainloop(cls):
        cls.app.MainLoop()

    @classmethod
    def exit(cls):
        cls.main_window.Close()

    @classmethod
    def width(cls):
        return None

    @classmethod
    def height(cls):
        return None    
