#coding=utf8
"""
Parent class for all shell template objects in this package.
Stores data about the system and common methods for user interaction.
"""
# Standard Library
import datetime
import os
import subprocess
import sys
import textwrap
import time

# Add-ons
import ctypes
try:
    from termcolor import colored
except:
    pass
try:
    import colorama
    from colorama import Fore, Back, Style
except:
    pass

# Local modules
from colorful.ansi import Ansi
import easycat
from ranges import gen_range
from versatiledialogs.lists import Enumeration, PlainList
from versatiledialogs.shell import Shellib


__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


# class TxtFx(object)
# class Cursor
# class Widgets
# class Cat
# class Boxes
# AnimatedText? TuiBits?
# Windows only


class _CursorInfo(ctypes.Structure):
    """
    Windows OS stuff
    """
    _fields_ = [
        ("size", ctypes.c_int),
        ("visible", ctypes.c_byte)]

    def __init__(self):
        super(_CursorInfo, self).__init__()
        self.visible = True


class Terminal(Shellib):
    """
    Eliminate dependencies
    """

    def __init__(self):
        """
        Get system info, see if bash is installed, start colorama
        """
        # Get OS and system info.
        super(Terminal, self).__init__()
        self.msg, self.msgtxt, self.main_window = None, None, None

        # Fixes unicode for Python 2
        if self.py_version == 2:
            reload(sys)
            sys.setdefaultencoding('utf8')

        #Use bash if available
        self.__class__.bash_available = bool(
            'bin' in os.listdir('/') and 'bash' in os.listdir('/bin'))
        self.__class__.interface = 'term'
        try:
            colorama.init()
        except:
            pass

    @classmethod
    def get_arrow_key(cls, arrows_only=False):
        """
        distinguish between arrow keys being pressed
        """
        code_dict = {
            'A': 'up',
            'B': 'down',
            'C': 'right',
            'D': 'left'
        }
        direction = None
        pressed = cls.get_keypress(fast=True)
        if pressed == chr(27):
            pressed = cls.get_keypress(fast=True)
            if pressed == '[':
                pressed = cls.get_keypress(fast=True)
                direction = code_dict.get(pressed, None)
            else:
                return None  # -1
        elif arrows_only is False:
            return pressed  # -1
        return direction

    @classmethod
    def center_window(cls, *args, **kwargs):
        """
        a dummy function
        """
        pass

    @classmethod
    def clear(cls, *args):
        """
        Clear screen; cross-platform; 0 means clear current line,
        else clear n previous lines
        """
        # use termcolor, figure out what is best for Windows

        # if no args, clear the screen
        if len(args) == 0:
            if cls.os_name == 'posix':
                # clear screen and leave cursor                
                easycat.write('\033[2J\033[H', stream=2)  
            elif cls.os_name == 'nt':           # at the top
                proc = subprocess.Popen('cls', shell=True)
                proc.wait()

        # if arg == 0, clear the current line
        elif args[0] == 0:
            easycat.write('\r\033[K\r', stream=2)

        # if arg > 0, erase that many lines back (.i.e., up)
        elif args[0] > 0:
            easycat.write('\r\033[K', stream=2)
            for _ in gen_range(args[0]):
                cls.cursor_v(1)
                easycat.write('\r\033[K', stream=2)

        # if arg < 0, add that many newlines
        elif args[0] < 0:
            easycat.write('\n' * abs(args[0]), stream=2)


    @staticmethod
    def cursor_h(x_disp, *args):
        """
        Move cursor in the x direction
        """
        if x_disp < 0:
            easycat.write('\033[{}D'.format(abs(x_disp)), stream=2)
        elif x_disp > 0:
            easycat.write('\033[{}C'.format(x_disp), stream=2)
        if len(args) >= 1:
            easycat.write(args[0], stream=2)

    @staticmethod
    def cursor_v(y_disp, *args):
        """
        Move cursor in the y direction
        """
        if y_disp > 0:
            easycat.write('\033[{}A'.format(y_disp), stream=2)
        elif y_disp < 0:
            easycat.write('\033[{}B'.format(abs(y_disp)), stream=2)
        if len(args) >= 1:
            easycat.write(args[0], stream=2)

    @classmethod
    def default_splash(cls,
                       title=sys.argv[0].split('.')[0].split('/')[-1].title(),
                       year=datetime.date.today().year, duration=.5):
        """
        There is probably a simpler syntax for getting the default title
        """
        copyleft = '(ↄ)' if cls.os_name == 'posix' else '(copyleft)'
        cls.text_splash(title, duration, 1)
        cls.text_splash('{}{} {}'.format(
            copyleft, int(year), __author__), .5, 1)
        cls.clear()


    @staticmethod
    def exit(quiet=False):
        out_str = '\nBye' if quiet is False else ''
        sys.exit(out_str)

    @staticmethod
    def fx(cmds, text):
        """
        p = print to stdout (otherwise, return as str)
        b = bold
        u = underline
        n = suppress newline
        """
        out_str = text
        attributes = []

        if 'b' in cmds:
            attributes.append('bold')

        if 'u' in cmds:
            attributes.append('underline')

        if 'n' not in cmds:
            out_str += '\n'

        out_str = colored(out_str, attrs=attributes)

        if 'p' in cmds:
            easycat.write(out_str)
        else:
            return out_str

    @classmethod
    def get_keypress(cls, prompt='', fast=False, hide=True):
        """
        Accepts one char of input.  If bash is available, it is not necessary to
        hit <ENTER>.
        """
        key = None
        if cls.bash_available is True and fast is False:
            easycat.write(prompt)

        if cls.platform == 'Windows':
            try:
                key = cls.input(prompt, hide_form=True)[0]
                cls.cursor_v(1)
            except IndexError:
                key = ' '
        elif cls.os_name == 'posix':
            key = subprocess.check_output("bash -c 'read -s -n 1 x;\
                echo -en \"$x\"'", shell=True)
        if len(key) > 1:
            key = key.rstrip('\n')
        if len(key) == 0:
            key = b' '
        #key = key[0]
        #time.sleep(0.05) # keys it stablish?
        if (cls.platform, fast, hide) == ('Linux', False, True):
            easycat.write('\b \b ')
        if hide is False:
            easycat.write(key)
        #cls.cursor_v(-2)
        return key.decode('utf-8')

    # is it possible to be a classmethod AND a property?
    # Maybe this should not be a classmethod.
    @classmethod
    def height(cls):
        """
        Terminal height.  Only accurate for bash.
        """
        sizey = None
        if cls.bash_available is True:
            sizey = int(subprocess.check_output('tput lines', shell=True))
        elif cls.platform == 'Windows':
            from ctypes import windll, create_string_buffer

            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

            if res:
                import struct
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom, maxx, maxy) = struct.unpack(
                     "hhhhHhhhhhh", csbi.raw)
                sizey = bottom - top + 1
        if sizey is None:
            sizey = 25
        return sizey

    @classmethod
    def hide_cursor(cls):
        """Hide cursor"""
        if cls.platform == 'Windows':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(
                handle, ctypes.byref(ci))
            ci.visible = False
            ctypes.windll.kernel32.SetConsoleCursorInfo(
                handle, ctypes.byref(ci))

        elif cls.os_name == 'posix':
            easycat.write('\033[?25l', stream=2)

    @classmethod
    def hrule(cls, width=None, symbols='_', centered=False, string=False):
        """
        Draw a horizontal line to the screen of 'width' size, made up of
        'symbols' str, centered or not, to stdout or as a str.

        (*Add 'position' keyword.)
        """
        width_ = cls.width()
        if not width:
            width = int(width_)
        elif (0.0 <= width < 1.0) or (isinstance(width, float)):
            width = int(round(width_ * width, 0))
        line = symbols * (width // len(symbols))
        if centered is True:
            line = line.center(width_)
        if string is False:
            cls.output(line)
        else:
            return '\n{}'.format(line)

    @classmethod
    def input(cls, prompt='>', hide_form=False):
        """
        Get input using the appropriate version of Python.
        """
        stripped = Ansi.strip_ansi(prompt)
        if isinstance(stripped, bytes):
            stripped = stripped.decode('utf8')
        try:
            if hide_form is False:  # and cls.platform == 'Linux':
                cls.output(''.join(
                    (' ' * (len(stripped) - 1), '┌', '─' * 22, '┐')))
            easycat.write(prompt)
            if hide_form is False:  # and cls.platform == 'Linux':
                easycat.write(
                    ''.join((
                        '[', colored(
                            ' ' * 20, 'yellow', 'on_grey', attrs=['underline', 'bold']),
                        ']│', ' ' * (cls.width() - (len(stripped) + 23)), '\n')))
                #write('\033[G')
                if cls.platform == 'Windows':
                    cls.cursor_v(1)
                cls.output(''.join(
                    (' ' * (len(stripped) - 1), '└', '─' * 22, '┘')))
                easycat.write('\r')

                cls.cursor_v(2)
                cls.cursor_h(len(stripped) + 1)
                easycat.write(''.join(
                    (Fore.YELLOW, Back.BLACK, Style.BRIGHT, Ansi.UNDERLINE)))
            return_str = input() if cls.py_version == 3 else raw_input()

        except KeyboardInterrupt:
            cls.cursor_v(2)
            easycat.write('\r\n')
            cls.exit()
        else:
            cls.cursor_v(-2)
            return return_str
        finally:
            easycat.write(Style.RESET_ALL)




    @staticmethod
    def list_menu(list_obj):
        """
        Synonym: ListPrompt.input()
        """
        list_prompt = ListPrompt(list_obj.items, list_obj.label)
        return list_prompt.input()

    @classmethod
    def make_page(cls, header=None, obj='', func=lambda: 0):
        """
        Make a header, print something to the screen, and call a function.
        """
        cls.print_header(header)
        cls.output(obj)
        return func()

    @classmethod
    def message(cls, msg='', heading=''):  # , **kwargs): #add width and height
        """
        Like cls.notify(), but with an optional heading.
        """
        if heading:
            easycat.write(cls.ul(heading, position=1))
        cls.notify(msg)
        cls.wait()

    @classmethod
    def notify(cls, msg, get_str=False):  # , *args, **kwargs):
        """
        Prints message like this:

        [+]"some message"
        """
        message = ' [+] *** {} ***'.format(msg)
        if get_str is True:
            return message
        else:
            cls.output(message)

    @staticmethod
    def output(msg, heading=None, **kwargs):  # add width and height
        """
        Print text to stdout with an optional heading.
        """
        if heading is not None:
            print(heading)  # pylint: disable=C0325
        print(msg)  # pylint: disable=C0325

    @classmethod
    def outputf(cls, msg=None, head=""):
        """
        cls.output() + '\n'
        """
        cls.output(''.join(('\n', msg, '\n')), head)

    @classmethod
    def print_header(cls, message=None):
        """
        Clears screen; prints a bracketed heading in the
        top left of the screen.
        """
        cls.clear()
        if message is None:
            message = sys.argv[0]
        if '\n' in message or (len(message) + 2) > cls.width():
            string = colored(message, attrs=['reverse', 'bold'])
        else:
            string = colored('[{}]{}'.format(
                message, ' ' * (cls.width() - (len(message) + 2))), attrs=[
                    'reverse', 'bold'])
        cls.output(string + '\n')

    @classmethod
    def start_app(cls):
        """
        When this function is called, a file named [script_name].tmp is written
        in the current directory
        """
        if cls.platform != 'android':
            super(Terminal, cls).start_app()
            #file_name = sys.argv[0].split('/')[-1].split('.')[0] + '.tmp'
            #fhandler = open(file_name, 'w')
            #fhandler.close()

    @classmethod
    def text_splash(cls, text, duration=2.0, flashes=1, v_center=True):
        """
        make it sleep while it does this on mobile
        """
        dur_dict = {'secs': duration}
        #duration = duration
        def message_on():
            """
            centered string on a cleared screen, for an amount of time
            'duration'
            """

            cls.clear()

            if v_center is True:
                cls.output('\n' * (cls.height() // 2 - 2))
            cls.output(text.center(cls.width()))

            if flashes > 1:
                #duration /= (2.0 * flashes - 1.0)
                dur_dict['secs'] /= (2.0 * flashes - 1.0)
            time.sleep(dur_dict['secs'])

        def message_off():
            """
            blank screen, for an amount of time 'duration'
            """
            cls.clear()

            if flashes > 1:
                dur_dict['secs'] /= (2.0 * flashes - 1.0)
            time.sleep(dur_dict['secs'])

       # message_on()
        cls.hide_cursor()
        try:
            for _ in gen_range(int(flashes)):
                message_on()
                message_off()
        finally:
            cls.unhide_cursor()

    # it would be good if this could be combined with stuff,
    # e.g., print_header()
    @classmethod
    def titlebar(cls, text=sys.argv[0].split('/')[-1].split('.')[0]):
        """Writes some text--the name of the running script by
        default--centered, in brackets, flanked by '='s.

        e.g.,
=================================[ some text ]=================================

        or
================================[ program_name ]===============================
        """
        cls.clear()
        bracketed = '[ {} ]'.format(text)
        length = (cls.width() - len(bracketed)) // 2

        symbol = colored(' ', attrs=['reverse', 'bold']) if cls.os_name ==\
                 'posix' else colored(' ', 'white', 'on_white')
        hemibar = symbol * length
        easycat.write('{0}{1}{0}'.format(hemibar, bracketed))
        total_len = 2 * length + len(bracketed)

        #print 'while {} < {}'.format(total_len, cls.width())

        # Does this work?
        while total_len < cls.width():
            easycat.write(symbol)
            total_len += 1
        cls.output('\n')

    @classmethod
    def tty(cls, msg):
        """
        Type a message to stdout one letter at a time, like a teletype
        printout.
        """
        try:
            cls.hide_cursor()

            for char in msg:
                easycat.write(char)
                time.sleep(.019)
        finally:
            cls.output('')
            cls.unhide_cursor()

    @classmethod
    def ul(cls, text, symbol='=', position=None, width=None):
        """
        Return some text, as a str, underlined by some symbol ('=' by default).
        """
        text_width = len(text) + 2
        understroke = (symbol * (text_width // len(symbol)))

        if position is not None and position >= 0:
            indent_pad = ' ' * position
            understroke = indent_pad + understroke
            text = indent_pad + text
        else:
            screen_width = width if width is not None else cls.width()
            if position and position < 0:
                screen_width += (2 * position)
            understroke = understroke.center(screen_width)
            text = text.strip().center(screen_width)[1:-1]
        return "\n  {}\n {}".format(text, understroke)

    @classmethod
    def unhide_cursor(cls):
        if cls.platform == 'Windows':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(
                handle, ctypes.byref(ci))
            ci.visible = True
            ctypes.windll.kernel32.SetConsoleCursorInfo(
                handle, ctypes.byref(ci))

        elif cls.os_name == 'posix':
            easycat.write('\033[?25h', stream=2)

#    @classmethod
#    def view_info(cls, get_str=False):
#        lines = super(Terminal, cls).view_info(get_str=True).split('\n')
#        lines = lines[2:]
#        text = ''
#        for line in lines: # convert to list
#            text = ''.join((text, line, '\n'))
#        text = ''.join(('\n', cls.fx('u', 'Shell Info'), text))
#        if get_str is True:
#            return text
#        else:
#            cls.output(text)

    @classmethod
    def wait(cls, text=None):
        """
        Wait for a key press
        """
        try:
            cls.hide_cursor()
            if text is None:
                what2press = 'a key' if cls.bash_available is True else 'enter'
                text = 'Press {}'.format(what2press)
            text = ''.join(
                ('\n', ' ' * 5, Fore.BLUE, Back.WHITE, '[', Ansi.UNDERLINE,
                 text[0], '\033[24m', text[1:], ']', Style.RESET_ALL))
            cls.get_keypress(text)
            cls.clear(1)
            def blink():
                if cls.platform == 'Windows':
                    cls.clear(1)
                time.sleep(.1)  # .15
                easycat.write(text)
                time.sleep(.1)  # .3
                cls.clear(1)
            #new_thread = threading.Thread(target=blink)
            #new_thread.start()
            blink()
        finally:

            cls.unhide_cursor()
            if cls.platform == 'Linux':
                easycat.write(Ansi.RESET)



    @classmethod
    def welcome(cls, description='', get_str=False):
        """
        It would be good if this could capture the main docstring properly.
        """
        if cls.platform == 'android':
            return
        script_name = sys.argv[0].split('/')[-1].split('.')[0].title()
        formatted = textwrap.dedent(description).strip()
        #if cls.width() >= 40:
        #    width_ = 40
        #else:
        #    width_ = cls.width() - 5
        width_ = 40 if cls.width() >= 40 else cls.width() - 5

        formatted = textwrap.fill(formatted, initial_indent=' ' * 5,
                                  subsequent_indent=' ' * 5, width=width_)
        formatted = ''.join(
            (cls.ul(script_name, symbol='-', width=width_), '\n', formatted)
        )

        if get_str:
            return formatted
        if cls.is_first_run():
            cls.default_splash()
            cls.titlebar()
            cls.output('\n%s\n' % formatted)
            cls.wait()
            cls.clear()
            cls.titlebar()

    # is it possible to be a classmethod AND a property?
    # Maybe this should not be a classmethod.
    @classmethod
    def width(cls):
        """
        terminal width.  works on: bash, android sh
        """
        if cls.platform == 'Linux':
            return int(subprocess.check_output('tput cols', shell=True))
        elif cls.os_name == 'posix':
            try:  # not sure why the following line doesn't always work
                return int(
                    subprocess.check_output('echo $COLUMNS', shell=True))
                #return eval(os.system('echo $COLUMNS'))
            except: # ValueError:
                return 50
        #    return int(os.environ['COLUMNS'])
        elif cls.platform == 'Windows':
            from ctypes import windll, create_string_buffer

            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12

            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

            if res:
                import struct
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom, maxx, maxy) = struct.unpack(
                     "hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                #sizey = bottom - top + 1
            else:
                # sizex, sizey = 80, 25  # can't determine actual size -
                sizex = 80               # return default values
            #print sizex, sizey
            return sizex

        else:
            return 80


#######################
## MENU-type CLASSES ##
#######################
class CompactMenu(PlainList):
    """
    Compact form of a multiple-choice prompt
    """
    def __init__(self, options):
        super(CompactMenu, self).__init__(options)
        self.label = sys.argv[0].split('/')[-1].capitalize() + ' commands:'

    def __str__(self):
        """work on this"""
        str_list = [self.label]
        options = self.items
        used_letters = []
        for option in options:
            if option[0] not in used_letters:
                used_letters.append(option[0])
                option = '[{}]{}'.format(option[0], option[1:])
            str_list.append(' {},'.format(option))
        return ''.join(str_list)[:-1]

    def input(self):
        """Gets the users selection"""
        Terminal.output(self)
        Terminal()
        char = Terminal.get_keypress(sys.argv[0].split('/')[-1].lower() + '>')
        return char  # this will be improved in future


class ListPrompt(Enumeration):
    """
    An enumeration that asks the user to make a choice.
    """

    def __init__(self, l, heading=None):
        # , **kwargs):
        super(ListPrompt, self).__init__(l)  # , '')  implement heading
        Terminal()
        if len(l) > 0 and heading is None:
            self.label = 'Make a choice (1-{})'.format(len(self))
        else:
            self.label = heading

    def input(self, prompt='>', hidden=False):
        """
        Get a choice from the user.
        """
        ## Find out if it's a long list ##
        if len(self) > 10:
            long_ = True
            prompt = 'Type a number and press [ENTER]:'
        else:
            long_ = False

        self.show_heading = not hidden

        if hidden is False:
            if len(self) > Terminal.height() - 4:
                self.label = Terminal.fx(
                    'bn',
                    "Press 'q', then make a choice (1-{})".format(
                        len(self)))
                easycat.less(self.__str__())
            else:
                Terminal.output(self)
        else:
            easycat.write(self.label)

        if len(self) > 0:
            try:
                sel_str = Terminal.input(prompt, hide_form=True) if long_ else\
                          Terminal.get_keypress(prompt)
                sel = int(sel_str) if sel_str.isdigit() else None
            except KeyboardInterrupt:
                Terminal.output('')
                return None

            while sel is None or 1 > sel > len(self):
                try:
                    if (sel is None or sel < 1) and\
                        10 > len(self) > 0:
                        sel_str = Terminal.get_keypress(prompt)
                    else:
                        sel_str = Terminal.input(prompt, hide_form=True)
                    sel = int(sel_str) if sel_str.isdigit() else None

                except KeyboardInterrupt:
                    Terminal.output('')
                    return_val = None
            return_val = sel
        else:
            return_val = None
        return return_val
