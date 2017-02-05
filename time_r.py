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
import datetime
import subprocess
import sys
import time
import traceback

import easycat
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com'
__license__ = 'GPL'

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

    #supposedly there is an equivalent generator expression which would be
    #better
    if len([i for i in sys.argv[1:] if not i.startswith('-')]) > 0 or\
        (set(['-h', '--help']) & set(sys.argv)):
        parser.add_argument('time_str', type=str)
        return parser.parse_args()

def alert():
    """
    Print a visual alert using the toilet(/figlet) command.
    Print an audible alert using espeak speech synthesizer.
    """
    # Use toilet obj
    proc = subprocess.Popen('toilet "Done"', shell=True)
    proc.wait()

    today = datetime.datetime.today()
    now = today.strftime('%l:%M:%S %P')
    Terminal.output('Finished at {}.'.format(now))

    if ARGS is not None and ARGS.quiet == False:
        try:
            proc1 = subprocess.Popen(
                'play -n synth .5 sin 1000 vol 0.05 > /dev/null 2>&1',
                shell=True)
            proc1.wait()
        #if system call fails???
        except (OSError, subprocess.CalledProcessError):
            Terminal.fx('up', 'Problem in sox:')
            print(traceback.format_exc()) #pylint: disable=C0325
        try:
            proc2 = subprocess.Popen(
                'espeak -v en-us "Your coffee is ready"', shell=True)
            proc2.wait()
        #if system call fails???
        except (OSError, subprocess.CalledProcessError):
            Terminal.fx('up', 'Problem in espeak:')
            print(traceback.format_exc()) #pylint: disable=C0325


###############
#  CONSTANTS  #
###############
ARGS = _parse_args() if __name__ == '__main__' else None
TIME_STR = ARGS.time_str if ARGS is not None and ARGS.time_str is not None\
           else '330'
    
if TIME_STR[0] == ':':
    TIME_STR = ''.join(['0', TIME_STR])

SECONDS = float(TIME_STR) if TIME_STR.isdigit() else float(
    subprocess.check_output('./mmss.py {}'.format(TIME_STR), shell=True))
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
    string = (subprocess.check_output('./mmss.py {}'.format(
        int(remaining)), shell=True)).decode('utf-8')
    Terminal.hide_cursor()
    easycat.write('{} remaining'.format(string.rstrip()))
    while remaining >= 0:
        time.sleep(.5)
        remaining = SECONDS - time.time() + _SINCE
        string = (subprocess.check_output('./mmss.py {}'.format(
            int(remaining)), shell=True)).decode('utf-8')
        easycat.write('\r{}'.format(string.strip()))
    alert()



if __name__ == '__main__':
    try:
        main()  # use misc.current_time()
    except KeyboardInterrupt:
        today = datetime.datetime.today()
        now = today.strftime('%l:%M:%S %P')
        Terminal.output('\nInterrupted at {}.'.format(now))
    finally:
        Terminal.unhide_cursor()
