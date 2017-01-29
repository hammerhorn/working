#!/usr/bin/env python
#coding=utf8
"""
DATA SET SUM & STATS -

Sum of a list.  Gets input from the command line or from stdin.
"""
import argparse
import decimal
import math
import sys

from cjh.misc import notebook
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
    parser = argparse.ArgumentParser(
        description={
            'EN':__doc__,
            'EO':"""DATA SET SUM/STATS
            
            Sumo de nombraro.  Ricevas datumon de aŭ la komandlinio aŭ el
            'stdin'."""}[LANG.upper()])
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

    if __name__ == '__main__':
        args = parser.parse_args()
    else: args = None
    return args

#def _enable_notebook():
#    """
 #   View developer's comments
 #   """
 #   if ARGS.C is True:
 #       notebook(REMARKS)

def getdata_stdin():
    """
    Input numerical data line by line until EOF
    """
    if Terminal.os_name == 'posix':
        eof_key = '^D'
    else:
        eof_key = '^Z[enter]'
    s_dict = {
        'EN':"Enter addends, followed by '{}'".format(eof_key),
        'EO':"Provizu adiciatojn, finigita de '{}'".format(eof_key)}
    Terminal.output(s_dict[LANG.upper()])
    input_str = sys.stdin.read().strip()
    str_list = input_str.split()
    return str_list

def reset_frame():
    """
    clear screen and draw titlebar
    """
    Terminal.clear()
    Terminal.titlebar()
    #Terminal.output('')

def main():
    """
    Get a list of numbers from the user, and sum them up three ways.
    """

    if ARGS.w is True and SHELL.interface == 'term':
        reset_frame()
    if len(ARGS.ADDENDS) == 0:
        str_list = getdata_stdin()
    else:
        str_list = ARGS.ADDENDS
    num_list = [decimal.Decimal(i) for i in str_list]
    stats = DataSet(num_list)

    if SHELL.interface == 'term':
        Terminal.output('')
        if ARGS.w is True:
            Terminal.output('')
    out_str1 = '{}\n\n{}'.format(stats, stats.sum_str())

    if ARGS.verbose:
        out_str1 = out_str1[:-1]
        out_str1 += Terminal.hrule(string=True) + '\n'
        if ARGS.w is True and SHELL.interface == 'term':
            reset_frame()
             #Cli.print_header()
        Terminal.output(out_str1)
        Terminal.wait()
#

    out_str2 = '\n{}'.format(stats.range_str(LANG))
    out_str2 += '\n{}'.format(stats.averages_str(LANG))
        #s_dict = {'EN':'variance', 'EO':'varieco'}
        #out_str += '\n'#      {} = {:.4}'.format(s_dict[LANG], stats.variance)
    s_dict = {'EN':'std. deviation', 'EO':'norma diferenco'}
    out_str2 += '\n{} = {}'.format(s_dict[LANG], stats.std_dev)

    if SHELL.interface == 'term':
        SHELL.output(out_str2 + '\n')
        if ARGS.w is True:
#            Cli.output('')
            stats.histogram()
            Terminal.wait()
    else:
		#"Hang up" on main Tk window when done
        #if
        SHELL.message(out_str1 + out_str2, stats.__str__())#:

        #SHELL.main_window.destroy()
        SHELL.exit()
        #sys.exit()
        return


    Terminal.hrule()
    while True:
        member = SHELL.input('outcome: ')
        zscore = (
            decimal.Decimal(member) - stats.mean)/decimal.Decimal(stats.std_dev)
        SHELL.output('z-score: {:g}'.format(zscore))
        SHELL.output('normal pdf(x): {}'.format(
            (decimal.Decimal(2.0 * math.pi) * stats.variance * decimal.Decimal(
                math.e) ** (zscore ** 2)) ** decimal.Decimal(-0.5)))

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
    if SHELL.interface in ['wx', 'Tk']:
        SHELL.center_window()


###################
# RUN THE PROGRAM #
###################
if __name__ == '__main__':
    notebook(REMARKS)
    if ARGS.w:
        SHELL.welcome(description=__doc__)
    main()
