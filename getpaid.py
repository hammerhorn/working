#!/usr/bin/env python3
#coding=utf8
"""
Helps workers predict what their net pay will be.
"""
import argparse
import datetime
import sys
import time

from cjh.misc import bye, catch_help_flag, notebook
from cjh.paystub import PayPeriod, WorkWeek

from versatiledialogs.config import Config
from versatiledialogs.lists import PlainList
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

REMARKS = """
    - there is an issue with opening pickles in Windows
    - make this more automated
    - you will add the ability to edit punches
    - learn how to use locale properly
    - estimating pay based on a rough number of hours
    + loading saved pickles does not work

    * Tk support"""


def _parse_args():
    """
    Parse arguments.
    """
    def setup_template():
        """
        Prepare data structures.
        """
        global PAYCHECK
        if args.input_file:
            PAYCHECK = PayPeriod(sh_obj=SHELL)
            try:
                PAYCHECK = Terminal.open_p_file(args.input_file)
                Terminal.print_header(str(PAYCHECK.est_net_pay()))
                SHELL.output(PAYCHECK.__str__(), width=500, height=600)
                time.sleep(2)
            except IOError:
                sys.exit('Failed to load {}.'.format(args.input_file))
            startdate = PAYCHECK.start_date

        # if no input file and no start date, exit program
        elif not args.start_date:
            SHELL.message(
                'usage: pay_calc.py [-h] [-i INFILE|-s START] [-w WAGE]' +
                ' [-p PERCENT]')
            SHELL.exit()  # bye()

        # if there is a startdate but no infile, then parse startdate
        else:
            startdate_array = args.start_date.split('/')

            # initialize pay_period object
            startdate = datetime.date(
                int(startdate_array[2]), int(startdate_array[0]),
                int(startdate_array[1]))
            if args.percent:
                p = float(args.percent)
            elif args.input_file:
                pass
            else:
                p = PayPeriod.withholding_wizard()
            PAYCHECK = PayPeriod(startdate, percent=p, sh_obj=SHELL)

            if args.wage:
                PAYCHECK.wage = float(args.wage)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='load file')
    parser.add_argument(
        '-s', '--start_date', type=str, help='date pay period starts')
    parser.add_argument('-w', '--wage', type=float, help='dollars per hour')
    parser.add_argument('-p', '--percent', type=float, help='percent withheld')
    parser.add_argument(
        '-C', action='store_true', help="read developer's comments")
    catch_help_flag(help_str=__doc__, sh_obj=SHELL, argprsr=parser)
    args = parser.parse_args()
    Terminal.default_splash('== pay calc ==', 2014)
    setup_template()
    return args


def print_title(title='PAYCHECK CALCULATOR'):
    """
    Print title.
    """
    Terminal.print_header()
    Terminal.output('')
    Terminal.output(title.center(Terminal.width()))
    Terminal.output(('=' * 25).center(Terminal.width()))

print_range = lambda: print_title('  {} — {}'.format(
        PAYCHECK.start_date, PAYCHECK.start_date + datetime.timedelta(14)))
    

def view_pay_period():
    """
    View pay period.
    """
    SHELL.output(PAYCHECK)
    SHELL.wait()


def input_shifts():
    """
    Input shifts.
    """
    print_range()
    startdate = PAYCHECK.start_date
    for i in range(14):
        day_number = (startdate.weekday() + i) % 7
        day_str = WorkWeek.weekday_name(day_number)
        print('{}/{} ({})'.format((startdate + datetime.timedelta(i)).month, (
            startdate + datetime.timedelta(i)).day, day_str))
        str1 = (PAYCHECK.shift_dict.get(datetime.date(
            (startdate + datetime.timedelta(i)).year,
            (startdate + datetime.timedelta(i)).month,
            (startdate + datetime.timedelta(i)).day)))
        if str1:
            SHELL.output(str1)
        try:
            PAYCHECK.add_shift((startdate + datetime.timedelta(i)).month, (
                startdate + datetime.timedelta(i)).day)
            print_range()
            SHELL.output(PAYCHECK)
        except ValueError:
            continue
        except KeyboardInterrupt:
            break
        finally:
            Terminal.output('')

def save_state():
    """
    Save paycheck as a pickle and json.
    """
    PAYCHECK.save_p_file(str(PAYCHECK.start_date))
    #paycheck.save_as_json(str(paycheck.start_date) + ".json")

def estimate_paycheck():
    if not(ARGS.percent) and PAYCHECK.percent == None:
        sub_menu = PlainList(['continue', 'withholding wizard'])
        sel1 = SHELL.list_menu(sub_menu)
        if sel1 == 2:
            PayPeriod.withholding_wizard()
    Terminal.print_header(str(PAYCHECK.est_net_pay()))

    # Use Cli.money()?
    out_str = 'Gross pay: {}\n  Net pay: {}'.format(
        PAYCHECK.gross_pay(), PAYCHECK.est_net_pay())
    SHELL.output(out_str)
    SHELL.wait()

#def withholding_wizard():
#    Terminal.print_header()
#    print("Withholdings Wizard")
#    print('-' * 30)
#    print('Please enter the following fields from a recent pay stub.')
#    gross = float(input('Gross pay: $'))
#    net   = float(input('  Net pay: $'))
#    paycheck.percent = 100.0 * (1.00 - net / gross)
#    print("Percent withheld: %.3g%%" % (paycheck.percent))
#    Terminal.wait()


##############
# Start Here #
##############

#percent_withheld = 33.333 # Use 'withhoding wizard' to change.

CONFIG = Config()
SHELL = CONFIG.start_user_profile()

#SHELL.msg.config(bg='white', font=('courier', 12, 'bold'))

if SHELL.interface == 'Tk':
    SHELL.msg.config(font=('courier', 9))

if __name__ == '__main__':
    notebook(REMARKS)
    ARGS = _parse_args()
    try:
        print_range()
    except NameError:
        pass

# Main Menu
MAIN_MENU = PlainList(('view pay period',
                       'input shifts',
                       'estimate paycheck amount',
                       '(add shift)',
                       '(edit/remove shift)',
                       'save',
                       'load pay period'))


def open_file():
    filename = SHELL.input('file name: ')
    PAYCHECK = PayPeriod.open_p_file(filename)

def not_implemented(something):
    SHELL.message('feature not yet implemented\n')
    time.sleep(1)


#############
# Main Loop #
#############
def main():
    global PAYCHECK
    while True:
        sel = SHELL.list_menu(MAIN_MENU)
        print_range()

        cmd_dict = {
            1   : view_pay_period,
            2   : input_shifts,
            3   : estimate_paycheck,
            6   : save_state,
            7   : open_file,
            None: None
        }

        try:
            cmd_dict.get(sel, not_implemented)()
        except TypeError:
            SHELL.exit()
        print_range()


if __name__ == '__main__':
    main()
    SHELL.start_app()
