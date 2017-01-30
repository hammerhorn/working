
#!usr/bin/env python
#coding=utf8
"""
Base class for most classes
"""
import os
import pickle
import sys

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


class Thing(object):
    """
    Parent class for most classes in this package;
    provides str 'label' and class int 'count'
    Contains methods for saving as txt or pickle.
    """

    count = 0

    def __init__(self):
        """
        increments instance counter "count" and sets a default label.
        """
        self.__class__.count += 1
        self.label = self.__default_label()


    def __repr__(self):
        """
        returns a str 'self.label'
        """
        return self.label

    def __eq__(self, other):
        """How should this work?  What should it do?"""
        try:
            return self.label == other.label
        except AttributeError:
            return self.label == other

    def __ne__(self, other):
        return not self == other  # pylint: disable=C0113

    def __default_label(self):
        """
        Generates a generic label
        """
        return '{} #{}'.format(
            self.__class__.__name__.lower(), self.__class__.count)

    @staticmethod
    def _save(basename, ext, save_func):
        """
        Open the file, perform the appropriate save action and close the file.
        things to add: confirm filename and check for overwrite
        """
        filename = basename + '.' + ext
        dir_name = os.getcwd()
        if dir_name != '/':
            dir_name += '/'
#        # See if exists
#        #if sh_class is not None and\
#        #    sh_class.interface in ['sh', 'bash', 'dialog', 'zenity']:
#
#            # Confirm filename
#            #try:
#            #    filename = sh_class.save_prompt(filename, dir_name)
#            #except KeyboardInterrupt:
#            #    return
        if ext == 'p':
            handler = open(filename, 'wb')
        else:
            handler = open(filename, 'w')
        save_func(handler)
        handler.close()


    def write_txt(self, basename, ext='txt'):  # , sh_class=None):
        """
        Cast object as str and write to a txt file.
        """
        #if sys.version_info.major == 3:
        #    self._save(\
        #        basename, ext, lambda f: f.write(bytes(str(self) + '\n',\
        #        'UTF-8')))#, sh_class)
        #elif sys.version_info.major == 2:
        self._save(\
            basename, ext, lambda f: f.write(str(self) + '\n'))

    def save_p_file(self, basename):
        """
        Save instance as a pickle.  (Use Shell.open_p_file() to open.)
        """
        self._save(basename, 'p', lambda f: pickle.dump(self, f))

    def sizeof(self):
        """
        trying to get the size in memory of the object
        """
        return sys.getsizeof(self)
