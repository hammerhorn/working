#!/usr/bin/env python
#coding=utf8
"""
Config objects stores configuration information and methods to read/write the
./config.json file.
"""
import json
import sys
import time
import traceback

#from cjh import terminal
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

#try:
from ttyfun import blocks
from versatiledialogs.dialog_gui import DialogGui
from versatiledialogs.tk_template import TkTemplate
    #import cjh.tk_template
from versatiledialogs.wx_template import WxTemplate
#except ImportError:
#    sys.exit('import error')

class Config(object):
    """
    This should be combined with Shellib
    """

    def __init__(self):
        """
        Get directory name of config file.
        """
        if Terminal().platform == 'android':
            self.basedir = '/storage/emulated/0/qpython/lib/python2.7/site-packages/cjh'
            #'/storage/sdcard0/com.hipipal.qpyplus/lib/python2.7/site-packages/cjh'
                
        else:
            self.basedir = 'versatiledialogs'
        self.sh_class = Terminal()


        try:
            self.read_config_file()
        except IOError:
            self.config_dict = {
                'editor': './tk_text.py',
                'shell': 'term',
                'terminal': 'gnome-terminal -x',
                'language': 'eo'
            }
            self.write_to_config_file(**self.config_dict)

    def read_config_file(self):
        """
        Find the config.json file and load its contents into this object.
        """
        # Load json file and retrieve data.
        if sys.version_info.major == 2:
            self.config_dict = json.load(
                open('{}/config.json'.format(self.basedir), 'rb'))
        else: #i.e., if sys.version_info.major == 3:
            file_handler = open('{}/config.json'.format(self.basedir), 'rb')
            file_str = file_handler.read().decode('utf-8')
            self.config_dict = json.loads(file_str)

    def start_user_profile(self):
        """
        Launches specified shell.
        """
        self.read_config_file()
        shell = self.config_dict['shell']
        self.sh_class = self.launch_selected_shell(shell)
        return self.sh_class

    def get_lang_key(self):
        """
        Return the language code from the config file
        """
        return self.config_dict['language']

    def write_to_config_file(self, **kwargs):
        """
        Writes preferences as JSON
        """
        self.config_dict.update(kwargs)
        with open('{}/config.json'.format(self.basedir), 'w') as outfile:
            json.dump(self.config_dict, outfile, indent=2)
            outfile.close()

    @staticmethod
    def launch_selected_shell(shl):
        """
        Select appropriate UI class from cjh.shell module
        Perhaps move this to some other class, or no class.
        """
        if shl in ['dialog', 'SL4A', 'zenity']:
            sh_class = DialogGui(shl)
        elif shl == 'Tk':
            try:
                sh_class = TkTemplate()
            except SystemExit:
                blocks.ellipses("Display not found.  Defaulting to 'term'.")
                Terminal.output('')
                sh_class = Terminal()
                sh_class.output(traceback.format_exc())
                time.sleep(4)
        elif shl == 'wx':
            try:
                sh_class = WxTemplate()
            except SystemExit:
                blocks.ellipses("Display not found.  Defaulting to 'term'.")
                Terminal.output('')
                sh_class = Terminal()
                sh_class.output(traceback.format_exc())
                time.sleep(4)
        else: sh_class = Terminal()
        return sh_class
