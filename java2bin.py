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
import subprocess
import sys

from cjh.misc import catch_help_flag, notebook

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

DEV_COM = """
    - It works.
    - It would be nice if it could detect the necessary files automatically."""

notebook(DEV_COM)
catch_help_flag(__doc__)


def initialize_all():
    """
    Initializing all of our values to default values
    """
    return [], [], []

def main():
    """
    1) Compile Java source ($*.java -> .$*.class).
    2) Compile to an executable binary
    3) strip
    4) mark as executable.

    Dependencies: gcj
    Note: In many cases, using ant to compile to a JAR file is a better idea.
    """

    def compile_java_src():
        """*$.java -> $*.class"""

        proc = subprocess.Popen('javac {} 2>&1 >/dev/null|more'.format(
            ' '.join(javafiles)), shell=True)
        # proc = subprocess.Popen('javac {} |more'.format(
        #    ' '.join(javafiles)), shell=True)
        proc.wait()

    def create_binary():
        """
        Compile to an executable, strip, and mark as executable.
        """
        cmd_tup = ('gcj-5 -c -g -O ',
                   '{} && gcj-5 --main={} '.format(
                       ' '.join(classfiles), sys.argv[1]),
                   '{0} -o {1} && rm -f {0} && '.format(
                       ' '.join(ofiles), sys.argv[1]),
                   'strip -s {0} && chmod +x {0}'.format(sys.argv[1]))
        command = ''.join(cmd_tup)
        proc = subprocess.Popen(command, shell=True)
        proc.wait()

    javafiles, classfiles, ofiles = initialize_all()

    for arg in sys.argv[1:]:
        javafiles.append('{}.java'.format(arg))
        classfiles.append('{}.class'.format(arg))
        ofiles.append('{}.o'.format(arg))

    compile_java_src()
    create_binary()

if __name__ == '__main__':
    main()
# I don't remember how to make jar files
