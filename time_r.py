#!/usr/bin/env python3
#coding=utf8
"""
Takes an argument in the form of ss or mm:ss, uses mmss.py to convert
it and uses the time module to maintain accuracy.  Default time span is
5 minutes 30 minutes.

  use: coffee.py [-h] [-q] TIME_STR

where TIME_STR is of the form SS, :SS, MM:, or MM:SS.

* I think there are portable libraries for voice synth?  This script
should be modified to not depend on mmss.py and to convert bytes to
string if running under python3.
"""
import argparse
import sys
import time

from cjh import misc
from cjh.music import Note, Pitch
import easycat
from ttyfun.unix import Figlet
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com'
__license__ = 'GPL'

REMARKS = """
    + incorporate mmss.py
    + use note class
    + use toilet class
    + misc.current_time
    + misc.speak"""

misc.notebook(REMARKS)

################
#  PROCEDURES  #
################
def _parse_args():
    """
    -h             get help on these options
    -q, --quiet    suppress audible alert
    TIME_STR       (seconds), :(seconds), (minutes):, or (minutes):(seconds)
    """
    parser = argparse.ArgumentParser(description="""
        Accurate Coffee Timer.  Takes an argument is the form SS, MM:, or
        MM:SS.  Default time = 5:30)""")
    parser.add_argument('-q', '--quiet', help='no sound', action='store_true')
    misc.catch_help_flag(help_str=__doc__, argprsr=parser)

    #supposedly there is an equivalent generator expression which would be
    #better
    if len([i for i in sys.argv[1:] if not i.startswith('-')]) > 0:
        parser.add_argument('time_str', type=str)
        return parser.parse_args()


def alert():
    """
    Print a visual alert using the toilet(/figlet) command.
    Print an audible alert using espeak speech synthesizer.
    """
    Figlet().output('Done')
    Terminal.output('Finished at {}.'.format(misc.current_time()))

    if ARGS is not None and ARGS.quiet is False:
        Note(Pitch(freq=1000), 0.5).play(voice='sin')
        misc.speak('Your coffee is ready')


###############
#  CONSTANTS  #
###############
ARGS = _parse_args() if __name__ == '__main__' else None
TIME_STR = ARGS.time_str if ARGS is not None and ARGS.time_str is not None\
           else '330'

if TIME_STR[0] == ':':
    TIME_STR = '0' + TIME_STR

SECONDS = float(TIME_STR) if TIME_STR.isdigit() else float(
    misc.mmss_convert(TIME_STR))
_SINCE = time.time()


##########
#  MAIN  #
##########
def main():
    """
    Starts the countdown timer, continually double-checking against clock
    time to maintain accuracy.
    """
    Terminal()
    remaining = SECONDS
    string = misc.mmss_convert(int(remaining))

    Terminal.hide_cursor()
    easycat.write('{} remaining'.format(string.rstrip()))
    while remaining >= 0:
        time.sleep(.5)
        remaining = SECONDS - time.time() + _SINCE
        string = misc.mmss_convert(int(remaining))
        easycat.write('\r{:>3s}'.format(string.strip()))
    alert()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Terminal.output('\nInterrupted at {}.'.format(misc.current_time()))
    finally:
        Terminal.unhide_cursor()
