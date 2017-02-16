#!/usr/bin/env python
#coding=utf8
"""
The Tk plugin for my shell model, along with classes for the necessary
types of dialog boxes.
"""
import os
import sys

try:
    import tkMessageBox
    import Tkinter as tkinter
except ImportError:
    try:
        from tkinter import messagebox as tkMessageBox
        import tkinter
    except ImportError:
        print("Could not import module 'tkinter'.")

from cjh.music import Pitch

from versatiledialogs.terminal import Terminal
from versatiledialogs.windowed_app import WindowedApp
#from cjh.music import Pitch, Note

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class TkTemplate(WindowedApp):
    """
    This is my plug-in for my shell model.
    """

    def __init__(self):
        super(TkTemplate, self).__init__('Tk')

    @classmethod
    def declare_main_window(cls, width=200, height=50, x=0, y=100):
        mod_name = super(TkTemplate, cls).declare_main_window()
        if 'DISPLAY' not in os.environ:
            Terminal.output('No X display found.  Exiting program.')
            Pitch().play()
            sys.exit()
        cls.main_window = tkinter.Tk()
        cls.main_window.wm_title(mod_name)
        cls.main_window.config(bg='#EEEEEE')
        cls.center_window(width_=width, height_=height, x_offset=x, y_offset=y)

        #cls.main_window.call(
        #    'wm', 'iconbitmap', cls.main_window._w, '../trees.xbm')
        #cls.main_window.wm_iconbitmap(bitmap='../trees.xbm')
        #if not height: height = 0

    @classmethod
    def add_message_widget(cls):
        """
        Puts the default message area on the window.
        """
        cls.msgtxt = tkinter.StringVar()
        #cls.msgtxt.set("'" + sys.argv[0].split('/')[-1] + "' is running")
        cls.msgtxt.set("'{}' is running".format(sys.argv[0].split('/')[-1]))
        cls.msg = tkinter.Message(cls.main_window, textvariable=cls.msgtxt, width=600)
        cls.msg.config(bg='white')
        cls.msg.pack(pady=10)

    @classmethod
    def create_menu(cls):
        """
        Attach an upper menu bar.
        """
        cls.mainmenu = tkinter.Menu(cls.main_window, tearoff=0)
        cls.__create_exit_menu()
        cls.main_window.config(menu=cls.mainmenu)

    @classmethod
    def __create_exit_menu(cls):
        """
        Create exit menu
        """
        cls.filemenu = tkinter.Menu(cls.mainmenu, tearoff=0)
        cls.filemenu.add_command(label='Quit', command=cls.main_window.destroy)
        cls.mainmenu.add_cascade(label='File', menu=cls.filemenu)
        cls.__create_language_menu()

    @classmethod
    def __create_language_menu(cls):
        """
        Create language menu.  curretly english and esperanto
        """
        cls.languagemenu = tkinter.Menu(cls.filemenu, tearoff=0)
        cls.languagemenu.add_command(label='English (en)')
        cls.languagemenu.add_command(label='Esperanto (eo)')
        cls.optionmenu = tkinter.Menu(cls.mainmenu, tearoff=0)
        cls.optionmenu.add_cascade(label='Language', menu=cls.languagemenu)
        cls.mainmenu.add_cascade(label='Options', menu=cls.optionmenu)

    @classmethod
    def output(cls, msg, **kwargs):
        """
        Write text to the default message area
        """
        if 'heading' in kwargs:
            msg = Terminal.ul(kwargs['heading'], symbol='-', width=20) + msg
        if 'width' in kwargs and 'height' in kwargs:
            cls.center_window(width_=kwargs['width'], height_=kwargs['height'])
        elif 'height' in kwargs:
            cls.center_window(height_=kwargs['height'])
        cls.msgtxt.set(msg)

    @classmethod
    def popup(
        cls, msg, heading='Output', width=None, height=None, x_pos=None,
        y_pos=None):
        """
        a type of pop-up dialog without an OK button.
        """
        if width is None:
            width = 200
        if height is None:
            height = 90
        if x_pos is None:
            x_pos = 0
        if y_pos is None:
            y_pos = 0
        dialog = TkDialog(cls.main_window, msg, heading, width, height)
        cls.center_window(
            width_=width, height_=height, x_offset=x_pos, y_offset=y_pos,
            win=dialog.top)
        cls.main_window.wait_window(dialog.top)

    @classmethod
    def outputf(cls, msg=None, head=None):
        """
        make the 'file' attribute work, and the heading
        """
        cls.msg.config(font=('mono', 10))
        cls.output(msg)

    @classmethod
    def input(cls, prompt='Enter something:', **kwargs):
        """
        Gets input from a dialog box.
        """
        if len(prompt) >= 10:
            W = int(len(prompt) * 8.8)
        else:
            W = 88
        input_dialog = TkInput(cls.main_window, prompt, width=W)
        cls.main_window.wait_window(input_dialog.top)
        string = input_dialog.val
        return string.strip()

    @classmethod
    def width(cls):
        """
        screen width in pixels
        """
        return cls.main_window.winfo_screenwidth()

    @classmethod
    def height(cls):
        """
        screen height in pixels
        """
        return cls.main_window.winfo_screenheight()

    @classmethod
    def welcome(cls, script_name=sys.argv[0].split('/')[-1].split('.')[0],
        description='', get_str=False):
        #if super(tk_template):
        if cls.is_first_run():
            cls.message(description, script_name)

    @classmethod
    def clear(cls):
        cls.output('')

    @classmethod
    def message(cls, msg, heading=''):#, width=40, height=10):
        """
        pop-up message dialog
        """
        #Note(Pitch('F', 5), .1).play()
        msg = str(msg)
        msg = msg.strip('"')
        tkMessageBox.showinfo(heading, msg)
        #Note(Pitch('F', ), .125).play()
        return True

    @classmethod
    def list_menu(
        cls, list_obj, prompt='Make a selection:', title='Menu Widget'):
        """
        Prompt user with a list dialog and return a natural number
        (e.g., 1, 2, 3, ...).
        """
        menu_dialog = TkList(cls.main_window, list_obj, prompt, title)
        cls.main_window.wait_window(menu_dialog.top)
        return menu_dialog.val[0] + 1

    @classmethod
    def center_window(
        cls, width_=200, height_=100, x_offset=0, y_offset=200, win=None):
        """
        Positions window in relation to the center of the screen and set
        geometry.
        """
        if not win:
            win = cls.main_window
        #if w==None: w = 400
        #if h==None: h = 0
        #if x_offset==None: x_offset = 0
        #if y_offset==None: y_offset = 200

        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        x_pos = (screenwidth - width_) // 2 - x_offset
        y_pos = (screenheight - height_) // 2 - y_offset
        win.geometry('{}x{}+{}+{}'.format(width_, height_, x_pos, y_pos))

    @classmethod
    def start_app(cls):
        super(TkTemplate, cls).start_app()
        cls.main_window.mainloop()


    @classmethod
    def exit(cls):
        cls.main_window.destroy()

    #@classmethod
    #def ellipse(cls, msg):
    #    cls.message(msg)

######################
## Tk-BASED CLASSES ##
######################
class TkPopup(object):
    def __init__(
            self, parent, msg, heading='Popup', width=200, height=90):
        self.top = tkinter.Toplevel(parent)
        self.top.title(heading)
        TkTemplate.center_window(width_=width, height_=height, win=self.top)
        tkinter.Label(self.top, text=msg).pack(pady=10)


class TkDialog(TkPopup):
    """
    A generic popup dialog with a button.
    """

    def __init__(
            self, parent, msg, heading='Dialog Widget', width=200, height=90):
        super(TkDialog, self).__init__(parent, msg, heading, width, height)
        button = tkinter.Button(self.top, text='OK', command=self.okay)
        button.pack(padx=5, side='top')
        button.focus_set()
        button.grab_set()

    def okay(self):
        """
        when button is clicked, parent is destroyed
        """
        self.top.destroy()


class TkInput(TkPopup):
    """
    An input dialog.
    """
    def __init__(self, parent, msg='Input', heading='Input Widget', width=200, height=110):
        super(TkInput, self).__init__(parent, msg, heading, width, height)
        self.entry = tkinter.Entry(self.top)
        self.entry.pack()
        self.entry.focus_set()

        #dialog is on a higher layer
        self.top.lift()
        self.top.attributes('-topmost', True)


        TkTemplate.center_window(
            win=self.top, width_=width, height_=height, x_offset=0, y_offset=-30)

        self.entry.focus_force()

        button = tkinter.Button(self.top, text='OK', command=self.okay)
        button.pack(pady=5)
        self.top.focus_set()

    def okay(self):
        """
        when button is clicked, val is set to text contained in Entry
        widget
        """
        self.val = self.entry.get()
        self.top.destroy()
        return self.val


class TkList(object):
    """
    A type of dialog which prompts the user to choose one from a list.
    """

    def __init__(
        self, parent, list_obj, prompt='Make a selection:',
        title='Menu Widget'):
        #msg = list_obj.label # * what is this supposed to be?
        list_items = list_obj.items[::-1]
        top = self.top = tkinter.Toplevel(parent)
        top.title(title)
        height = len(list_obj) *  15 + 50 #* 16 # + 8
        len_list = [len(i) for i in list_obj]
        box_width = max(len_list) + 1
        if box_width < len(prompt):
            width = int(len(prompt) * 9)
        else:
            width = int(box_width * 9)
        TkTemplate.center_window(
            win=top, x_offset=0, height_=height, width_=width, y_offset=-30)
        tkinter.Label(top, text=prompt).pack()
        #if len(list_obj) < 12:
        tall = len(list_obj)
        #else: tall = 12

        self.listb = tkinter.Listbox(top, height=tall, width=box_width)
        self.listb.focus_set()
        for item in list_items:
            self.listb.insert(0, item)
        button = tkinter.Button(top, text='OK', command=self.okay)
        button.focus_set()
        self.listb.select_set(0)
        self.listb.pack()
        button.pack(padx=5, fill='both', expand=1)

    def okay(self):
        """
        When button is clicked, val is set to whatever list item is
        highlighted.
        """
        self.val = self.listb.curselection()
        self.top.destroy()
