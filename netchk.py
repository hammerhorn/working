#!/usr/bin/env python3
"""
usage: netchk.py [-s]

Ping google to determine if the Internet connection is working.

optional arguments:
  -s          sound (audible signal when Internet is working)

Dependencies: espeak; cjh.misc, easycat, versatiledialogs
"""

import atexit
import subprocess
import sys
import time

from cjh.misc import current_time, speak, catch_help_flag

import easycat
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

#This script should be optimized for speed
TERM = Terminal()
atexit.register(TERM.unhide_cursor)
catch_help_flag(__doc__, TERM)


def main():
    """ Ping google"""
    TERM.hide_cursor()
    TERM.output(
        '\nChecking for Internet @ {}....(^C will terminate)'.format(
            current_time()))
    TERM.hrule()

    try:
        while True:
            try:
                subprocess.check_call(
                    'ping -c 2 google.com > /dev/null 2>&1', shell=True)
                connected = True
                easycat.write('\n[+]{}--Internet available @ '.format(
                    TERM.fx('bn', 'Connected')))
            except subprocess.CalledProcessError:
                connected = False
                easycat.write('\n[!] No Internet     @    ')
            easycat.write(current_time())


            if connected is True:
                if '-s' in sys.argv[1:]:
                    speak('on line')
                time.sleep(10)
            else:
                # Slows the loop down when there is no local network (I think)
                proc = subprocess.Popen(
                    'ping -c 1 192.168.1.1 > /dev/null 2>&1', shell=True)
                return_val = proc.wait()

                if return_val == 2:  # I guess 2 means fail?
                    # Alter this to use python regex
                    return_val_str = subprocess.check_output(
                        'ifconfig|tail -8|head -1|grep 192|wc -l',
                        shell=True)
                    return_val = int(return_val_str)
                    if return_val == 0:
                        time.sleep(5)

    except KeyboardInterrupt:
        TERM.output('\n')

if __name__ == '__main__':
    main()
    TERM.start_app()
