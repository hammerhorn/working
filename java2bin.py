#!/usr/bin/env python
#coding='utf8'
"""
   1) Compile Java source ($*.java -> .$*.class).
   2) Compile to an executable binary
   3) strip
   4) mark as executable.

   Dependencies: gcj
   Note: In many cases, using ant to compile to a JAR file is a better idea.
"""

import os
import sys

from cjh.misc import catch_help_flag, notebook
# from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

DEV_COM = """
    - It works.
    - It would be nice if it could detect the necessary files automatically.
"""
notebook(DEV_COM)
catch_help_flag(__doc__)


def initialize_all():
    """
    Initializing all of our values to default values
    """
    return '', '', ''

def main():
    """
    1) Compile Java source ($*.java -> .$*.class).
    2) Compile to an executable binary
    3) strip
    4) mark as executable.

    Dependencies: gcj
    Note: In many cases, using ant to compile to a JAR file is a better idea.
    """
    #global command


    def compile_java_src():
        """*$.java -> $*.class"""
        os.system('javac {} 2>&1 >/dev/null|more'.format(javafiles))

    def create_binary():
        """
        Compile to an executable, strip, and mark as executable.
        """
        command = 'gcj-5 -c -g -O'
        command += '{} && gcj-5 --main={}'.format(classfiles, sys.argv[1])
        command += '{0} -o {1} && rm -f {0} && '.format(ofiles, sys.argv[1])
        command += 'strip -s {0} && chmod +x {0}'.format(sys.argv[1])
        os.system(command)

    javafiles, classfiles, ofiles = initialize_all()

    for arg in sys.argv[1:]:
        javafiles += ' {}.java'.format(arg)
        classfiles += ' {}.class'.format(arg)
        ofiles += ' {}.o'.format(arg)

    compile_java_src()
    create_binary()

main()
# I don't remember how to make jar files
