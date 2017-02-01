#!/usr/bin/env python
"""A test of the Cli.tty method.  Writes text to the screen one char at a time,
like a teletype."""


import datetime
# import sys
import textwrap

from cjh.text_fill import TextGen
from cjh.misc import catch_help_flag, notebook

from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - alter terminal.Terminal.tty() so that it automatically wraps text.
    - make the text justified"""


Terminal()

WIDTH = Terminal.width() - 10
if WIDTH > 60:
    WIDTH = 60

STRING = textwrap.fill(
    TextGen.chunk(),
    width=WIDTH,
    initial_indent=' ' * 10,
    subsequent_indent=' ' * 5)


def main():
    """
    Prints date and then a chunk of filler text.  Text "streams" onto
    the screen.
    """
    Terminal.output('\n')
    today = datetime.datetime.today()
    now = today.strftime('%c')  # This is 100% portable!
    Terminal.tty(' ' * 35 + now)
    Terminal.output('\n' * 2)
    Terminal.tty(STRING)
    Terminal.output('\n' * 3)

if __name__ == '__main__':
    notebook(REMARKS)
    catch_help_flag(__doc__)
    main()
    Terminal.start_app()
