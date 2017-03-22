#!/usr/bin/python3
#coding=utf8
"""
Config objects stores configuration information and methods to read/write the
./config.json file.
"""
import json
import sys
import time
import traceback

from cjh import misc
from ttyfun import blocks
from versatiledialogs.dialog_gui import DialogGui
from versatiledialogs.terminal import Terminal
from versatiledialogs.tk_template import TkTemplate
from versatiledialogs.wx_template import WxTemplate

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Config(object):
    """
    This should be combined with Shellib
    """

    def __init__(self):
        """
        Get directory name of config file.
        """
    # '/storage/sdcard0/com.hipipal.qpyplus/lib/python2.7/site-packages/cjh'
        self.basedir = 'versatiledialogs' if Terminal().platform != 'android'\
            else '/storage/emulated/0/qpython/lib/python2.7/site-packages/versatiledialogs'
        self.sh_class = Terminal()


        try:
            self.read_config_file()
        except IOError:
            self.config_dict = {
                'editor'  : './tk_text.py',
                'shell'   : 'term',
                'terminal': 'gnome-terminal -x',
                'language': 'eo'
            }
            self.write_to_config_file(**self.config_dict)

    def read_config_file(self):
        """
        Find the config.json file and load its contents into this object.
        """
        # Load json file and retrieve data.
        self.config_dict = misc.read_json_file('%s/config.json' % self.basedir)


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
        def try_to_open(sh_obj):

            def fallback():
                blocks.ellipses("Display not found.  Defaulting to 'term'.")
                Terminal.output('')
                sh_class = Terminal()
                sh_class.output(traceback.format_exc())
                time.sleep(4)
                return sh_class

            try:
                sh_class = sh_obj()
            except SystemExit:
                sh_class = fallback()
            return sh_class

        if shl in ('dialog', 'SL4A', 'zenity'):
            sh_class = DialogGui(shl)
        elif shl == 'Tk':
            sh_class = try_to_open(TkTemplate)
        elif shl == 'wx':
            sh_class = try_to_open(WxTemplate)
        else:
            sh_class = Terminal()
        return sh_class
