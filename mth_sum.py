#!/usr/bin/env python
#coding=utf8
"""
Sum of a list.  Gets input from the command line or from stdin.
"""
import argparse
import decimal
import math
import sys

from cjh.misc import catch_help_flag, notebook
from cjh.statset import DataSet

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - Test with wx and SL4A;
    - Dynamic ranking of summing functions, fastest to slowest
    - Output formats: html, LaTeX, toilet, cow
    - file i/o
    - random dataset
    - verify input
    - develop statistical functions
    + Works with python 3.  
    + Works in English and Esperanto.
    + Works with bash, dialog, zenity, or Tk.
    + Most of the functionality has been moved to the StatSet class.
    + added variance and standard deviation
    + timer feature added
    """


#############
# FUNCTIONS #
#############
def _parse_args():
    """
    Parse arguments
    """
    doc_str = {
        'EN':__doc__,
        'EO': "Sumo de nombraro.  Ricevas datumon de aŭ la komandlinio aŭ el 'stdin'."
    }

    parser = argparse.ArgumentParser()  # description=doc_str[LANG.upper()])
    parser.add_argument(
        '-n', '--nox', action='store_true', help='print to stdout')
    parser.add_argument(
        '-s', '--shell', type=str, help="e.g., 'bash', 'Tk', 'zenity'....")
    parser.add_argument('-w', action='store_true', help='"windowed mode"')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='display min, max, mean, median, mode')
    parser.add_argument(
        '-C', action='store_true', help="see developer's comments")
    parser.add_argument("ADDENDS", help="numbers to be summed", nargs="*")
    catch_help_flag(help_str=doc_str[LANG.upper()].lstrip(),
                    title='Data Set Demo', argprsr=parser)
    return parser.parse_args() if __name__ == '__main__' else None


def getdata_stdin():
    """
    Input numerical data line by line until EOF
    """
    eof_key = '^D' if Terminal.os_name == 'posix' else '^Z[enter]'
    s_dict = {
        'EN': "Enter addends, followed by '{}'".format(eof_key),
        'EO': "Provizu adiciatojn, finigita de '{}'".format(eof_key)}
    Terminal.output(s_dict[LANG.upper()])
    input_str = sys.stdin.read().strip()
    return input_str.split()


def reset_frame():
    """
    clear screen and draw titlebar
    """
    Terminal.clear()
    Terminal.titlebar()


def main():
    """
    Get a list of numbers from the user, and sum them up three ways.
    """
    if ARGS.w is True and SHELL == 'term':
        reset_frame()

    str_list = getdata_stdin() if len(ARGS.ADDENDS) == 0 else ARGS.ADDENDS
    num_list = [decimal.Decimal(i) for i in str_list]
    stats = DataSet(num_list)

    if SHELL == 'term':
        Terminal.output('')
        if ARGS.w is True:
            Terminal.output('')
    out_str1 = '{}\n\n{}'.format(stats, stats.sum_str())

    if ARGS.verbose:
        out_str1 = out_str1[:-1]
        out_str1 = ''.join((out_str1, Terminal.hrule(string=True), '\n'))
        if ARGS.w is True and SHELL == 'term':
            reset_frame()
        Terminal.output(out_str1)
        Terminal.wait()

    s_dict = {'EN':'std. deviation', 'EO':'norma diferenco'}
    out_str2 = '\n'.join(('\n{}'.format(stats.range_str(LANG)),
                          '{}'.format(stats.averages_str(LANG)),
                          '{} = {}'.format(s_dict[LANG.upper()], stats.std_dev)))

    if SHELL == 'term':
        SHELL.output(out_str2 + '\n')
        if ARGS.w is True:
            stats.histogram()
            Terminal.wait()
    else:
        # "Hang up" on main Tk window when done
        SHELL.message(''.join((out_str1, out_str2, stats.__str__())))
        # SHELL.exit()

    Terminal.hrule()
    Terminal.output('')
    try:
        while True:
            member = SHELL.input('outcome: ')
            zscore = (
                decimal.Decimal(member) - stats.mean)/decimal.Decimal(stats.std_dev)
            out_str = ''.join(
                ('z-score: {:g}\n'.format(zscore),
                 'normal pdf(x): {}'.format(
                     (decimal.Decimal(2.0 * math.pi) * stats.variance * decimal.Decimal(
                         math.e) ** (zscore ** 2)) ** decimal.Decimal(-0.5)),
                 '\n')
            )
            SHELL.output(out_str, height=67, width=400)
    except KeyboardInterrupt:
        pass
    finally:
        SHELL.start_app()


#################
# SET CONSTANTS #
#################
CONFIG = Config()
LANG = CONFIG.get_lang_key()
ARGS = _parse_args()

if ARGS is not None and ARGS.nox is True:
    SHELL = Terminal()
elif ARGS is not None and ARGS.shell is not None:
    SHELL = CONFIG.launch_selected_shell(ARGS.shell)
else:
    SHELL = CONFIG.start_user_profile()
    if SHELL.interface in ('wx', 'Tk'):
        SHELL.center_window()


###################
# RUN THE PROGRAM #
###################
if __name__ == '__main__':
    notebook(REMARKS)
    if ARGS.w:
        SHELL.welcome(description=__doc__)
    main()
