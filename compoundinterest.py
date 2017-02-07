#!/usr/bin/env python
#coding=utf8
"""
Calculate continuously-compounded interest
"""
# Std Lib
import argparse
import atexit

# Add-ons
import numpy as np  # only needed for plotting

# Local
from cjh.misc import notebook
from cjh.money import Money
from ttyfun.unix import Figlet
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn'
__license__ = 'GPL'

REMARKS = """
    - accept input from stdin
    + get this to work with Tk
    + e.g., display plot for yearly compounding as a stairstep
    + add PyPlot
    + add periodic compounding

    * add LaTeX
    * figure out how to do parallel processes so the action doesn't have to stop
      for PyPlot"""


def _parse_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('PRINCIPAL', type=float, help='initial amount invested')
    parser.add_argument(
        'RATE',
        type=float,
        help='interest rate (0.001 for a typical savings account)')
    parser.add_argument('TIME', type=float, help='after this many years')
    parser.add_argument(
        '-p', '--plot', action='store_true', help='plot using PyPlot')
    parser.add_argument(
        '-n', '--nox', action='store_true',
        help='force use of textual interface')
    parser.add_argument(
        '-C', action='store_true', help="see developer's comments")
    parser.add_argument('-s', '--shell', type=str, help="'term', 'Tk', etc....")
    parser.add_argument(
        'PERIOD', type=str, nargs='?',
        help='y=yearly, s=semiannually, m=monthly, d=daily, c=continuously')
    args = parser.parse_args()
    return args


### DATA ###
notebook(REMARKS)
ARGS = _parse_args() if __name__ == '__main__' else None
CONFIG = Config()

if ARGS is not None and ARGS.nox is True:
    SHELL = Terminal()
elif ARGS is not None and ARGS.shell is not None:
    SHELL = CONFIG.launch_selected_shell(ARGS.shell)
else:
    SHELL = CONFIG.start_user_profile()

if SHELL.interface in ['wx', 'Tk']:
    SHELL.center_window()

# This seems abusive, but it seems to work
atexit.register(SHELL.start_app)

PRINCIPAL = Money(ARGS.PRINCIPAL)
RATE = ARGS.RATE
TIME = ARGS.TIME

def main():
    """
    Calculate interest and print out the new total.
    """
    def plot():
        """
        If GUI is available, plot the increase with respect to time, using
        PyPlot
        """
        Terminal.output('')
        Terminal.notify(
            Terminal.fx('bn', 'Close PyPlot window to continue...'))
        domain = np.arange(0.0, TIME, 0.1)
        plt.figure(1)
        plt.plot(domain, PRINCIPAL.interest(RATE, domain, ppy).amount, 'r')
        plt.show()
        Terminal.clear(2)

    time_dict = {
        'c': None,
        'y': 1.0,
        'd': 365.24,
        's': 2.0,
        'm': 12.0}

    ppy = time_dict[ARGS.PERIOD] if ARGS.PERIOD is not None else None
    result = PRINCIPAL.interest(RATE, TIME, ppy)

    if ARGS.plot is True:
        import matplotlib.pyplot as plt
        Terminal.clear()

    result_str = result.__str__()

    # Move this to Money class
    if SHELL.interface in ['term', 'dialog', 'zenity'] and\
       SHELL.platform != 'Windows':
        result_str = '\\' + result_str

    if SHELL.interface == 'term' and SHELL.platform == 'Linux':
        SHELL.output(
            '\n\n{}\n'.format(Figlet('future').output(
                result_str, get_str=True)))
    else:
        SHELL.message(result_str)

    if ARGS.plot is True:
        plot()

    SHELL.exit()

if __name__ == '__main__':
    main()
    SHELL.start_app()
