#!/usr/bin/env python
#coding=utf8
"""
Contains DialogGui class, which is needed for: android, dialog, zenity.
"""
import os
import random
import subprocess
import sys

try:
    import androidhelper as android
except ImportError:
    try:
        import android
    except ImportError:
        pass

import easycat
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class DialogGui(Terminal):
    """
    Provides common methods needed by dialog-type shells.
    (i.e., android, dialog, zenity).  Inherits from Shellib.
    """

    def __init__(self, *args):
        """
        Create main window for graphical application;
        args[0] is the interface name, e.g., 'zenity'.
        """
        super(DialogGui, self).__init__()
        if self.__class__.platform == 'android':
            self.__class__.interface = 'SL4A'
            self.__class__.droid = android.Android()
        else:
            if len(args) >= 1:
                self.__class__.interface = args[0]
            else:
                self.__class__.interface = [
                    'dialog', 'zenity'][random.randint(0, 1)
                ]

        #self.__class__.clear()
        #if __name__ == '__main__':
        #    cli.ellipses(
        #        'Starting {} interface.'.format(self.__class__.interface))


    ##################
    # SHARED METHODS #
    ##################
    @classmethod
    def output(cls, msg, heading='Output', width=None, height=None):
        """Display output dialog. Identical to message()."""
        msg = str(msg).replace('$', '\$')
        if cls.interface == 'dialog':
            if not width:
                width = 41
            if not height:
                height = 16
            wide, high = width, height
            cls.message(msg, heading, wide, high)
        elif cls.interface == 'SL4A':
            cls.droid.dialogCreateAlert(title=heading, message=str(msg))
            cls.droid.dialogShow()
            cls.droid.dialogGetResponse()
            cls.droid.dialogDismiss()
        elif cls.interface == 'zenity':
            cls.message(msg, heading)

    @classmethod
    def outputf(cls, **kwargs):
        """
        Output dialog with mono font.
        """
        # There should really be an operator....
        try:
            msg = kwargs['msg']
        except:
            pass
        try:
            heading = kwargs['heading']
        except:
            pass
        try:
            width = kwargs['width']
        except:
            pass
        try:
            height = kwargs['height']
        except:
            pass
        try:
            file_ = kwargs['file_']
        except:
            pass
        if cls.interface == 'dialog':
            cls.output(msg, heading, width, height)
        elif cls.interface == 'SL4A':
            print(heading + '\n')  # pylint: disable=C0325
            print(msg + '\n')  # pylint: disable=C0325
        elif cls.interface == 'zenity':
            if 'file_' not in kwargs.keys():
                with open('tmp', 'w') as file_handler:
                    file_handler.write(msg)
                    file_handler.close()
                os.system('zenity --text-info --filename=tmp --font=mono ' +
                    '--text={0} --title={0}'.format(heading))
            else:
                os.system('zenity --text-info --filename={0} --font=mono ' +
                    '--text={1} --title={1} --width=800 --height=700'.format(
                    file_, heading))

    @classmethod
    def input(cls, prompt='Enter something:'):
        """Input dialog"""
        if cls.interface == 'dialog':
            os.system('dialog --title "Inputbox - To take input from you"\
                --backtitle "{}" --inputbox "{}" 8 40 2> tmp'.format(
                    sys.argv[0], prompt))
            string = easycat.cat(files=['tmp'], quiet=True, return_str=True)
            os.remove('tmp')
            return string.strip()
        elif cls.interface == 'SL4A':
            try:
                response = cls.droid.dialogGetInput('Input', prompt)
                cls.droid.dialogDismiss()
                result = None
                if 'which' in response:
                    result = response['which']
                if result == 'negative':
                    raise Exception('Aborted.')
                return response.result
            except 'Aborted.':
                sys.exit()
        elif cls.interface == 'zenity':
            cmd = 'zenity --entry --text "{}" --title "Input" > tmp'.format(
                prompt)
            os.system(cmd)
            string = easycat.cat(files=['tmp'], quiet=True, return_str=True)
            os.remove('tmp')
            return string.strip()

    @classmethod
    def wait(cls, msg='Continue'):
        """Requires that user click 'OK' before going on."""
        if cls.interface in ['dialog']:
            os.system('dialog --pause "{}" 10 40 3'.format(msg))
        else: cls.message(msg)

    @classmethod
    def width(cls):
        """if using 'dialog', returns terminal width"""
        if cls.interface == 'dialog':
            return super(DialogGui, cls).height()
        elif cls.interface == 'SL4A':
            return super(DialogGui, cls).width()
        elif cls.interface == 'zenity':
            return # Hmmm...

    @classmethod
    def height(cls):
        """if using 'dialog', returns terminal height"""
        if cls.interface == 'dialog':
            return Terminal.height()
        elif cls.interface == 'SL4A':
            return super(DialogGui, cls).height()
        elif cls.interface == 'zenity':
            return # Hmmm...

    @classmethod
    def message(cls, msg, heading='', width=40, height=10):
        """Identical to cls.output()"""
        if cls.interface in ['dialog']:
            os.system('dialog --title "{}" --clear --msgbox "{}" {} {}'.format(
                heading, msg, height, width))
        elif cls.interface in ['SL4A']:
            cls.droid.dialogCreateAlert(title=heading, message=str(msg))
            cls.droid.dialogSetPositiveButtonText('OK')
            cls.droid.dialogShow()
            cls.droid.dialogGetResponse()
            cls.droid.dialogDismiss()
        elif cls.interface in ['zenity']:
            command = 'zenity --info --text="{}" --title="{}"'.format(
                msg, heading) # --width={} --height={}'.format(msg, he
                              #ading, width, height)
            os.system('{}'.format(command))

    @classmethod
    def list_menu(cls, list_obj, prompt='Make a selection:'):
    #, t="Menu Widget"):
        """List-type prompt"""
        if cls.interface in ['dialog']:
            list_str = ""
            for index, item in enumerate(list_obj.items):
                list_str += '{} "{}" '.format(index + 1, item)
                if index == 0:
                    list_str += 'on '
                else: list_str += 'off '
            cmd_str = 'dialog --radiolist "{}" 25 30 {} {}2> tmp'.format(
                prompt, len(list_obj), list_str)
            os.system(cmd_str)
            string = easycat.cat(files=['tmp'], quiet=True, return_str=True)

            #this is an error?
            #try:
            return int(string)
            #except: #Type?
            #    print("cmd_str: " + cmd_str)

        elif cls.interface in ['SL4A']:
            return cls.radio_button_dialog(list_obj.label, list_obj.items)
        elif cls.interface in ['zenity']:
            cmd = 'zenity --list --text="View list:" --column="{0}" --title="{0\
                }" --height=300 --hide-header'.format(list_obj.label)
            for item in list_obj:
                cmd += ' "{}"'.format(item)
            ans_str = subprocess.check_output("bash -c '{}'".format(
                cmd), shell=True)
            number = list_obj.items.index(ans_str.decode('utf-8').split(
                '|')[0].strip()) + 1
            return number

    @classmethod
    def save_prompt(cls, filename, dir_name):
        if cls.interface == 'SL4A':
            cls.droid.dialogCreateAlert(message="Save as {}'{}'?".format(
                dir_name, filename))
            cls.droid.dialogSetPositiveButtonText('Yes')
            cls.droid.dialogSetNegativeButtonText('No')
            cls.droid.dialogShow()
            response = cls.droid.dialogGetResponse().result
            cls.droid.dialogDismiss()
            print("response = '{}'".format(response))  # pylint: disable=C0325
        else: super(DialogGui, cls).save_prompt(filename, dir_name)

    @classmethod
    def radio_button_dialog(cls, question, options):
        """Lets user select a single option."""
        cls.droid.dialogCreateAlert(question)
        cls.droid.dialogSetSingleChoiceItems(options)
        cls.droid.dialogSetPositiveButtonText('OK')
        cls.droid.dialogSetNegativeButtonText('Cancel')
        cls.droid.dialogShow()
        response = cls.droid.dialogGetResponse().result
        if 'which' in response:
            result = response['which']
        if result == 'negative':
            raise Exception('Aborted.')
        selected_items = cls.droid.dialogGetSelectedItems().result
        cls.droid.dialogDismiss()
        return selected_items.pop() + 1

    @classmethod
    def notify(cls, msg, **kwargs):
        """Pops up a breif notification."""
        if cls.interface in ['SL4A']:
            cls.droid.makeToast(msg)
        elif cls.interface in ['zenity']:
            os.system('zenity --notification --text "{}"'.format(msg))
        elif cls.interface in ['dialog']:
            cls.message(msg)

    @classmethod
    def exit(cls):
        return

    @classmethod
    def view_info(cls, get_str=False):
        text = super(DialogGui, cls).view_info(get_str=True)
        lines = text.split('\n')[2:]
        msg = ''
        for line in lines:
            msg += line + '\n'
        if get_str is True:
            return msg
        else:
            cls.output(msg, heading='Shell Info')
