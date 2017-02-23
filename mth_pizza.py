#!/usr/bin/env python
#coding=utf8
"""
PIZZA PY -

Calculate the area and unit price of a circular pizza.
"""
import argparse
import decimal

from cjh.maths.geometry import Circle
from cjh.misc import notebook
from cjh.money import Money
from fiziko.kinematics import Disp
from fiziko.scalars import Unit
from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


REMARKS = """
    * A guessing mode might be fun.
    * Graphing?
    * research pizza pricing...toppings?
    * compare areas visually"""


##################
##  PROCEDURES  ##
##################
def _parse_args():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-m', '--metric', help='use centimeters instead of inches',
        action='store_true')
    parser.add_argument(
        '-d', '--diameter', type=float, help='diameter (inches by default)')
    parser.add_argument(
        '-p', '--price', type=float,
        help='price in dollars for one whole pizza')
    parser.add_argument(
        '-n', '--nox', action='store_true',
        help='force use of textual interface')
    parser.add_argument(
        '-s', '--shell', type=str,
        help="'bash', 'Tk', 'dialog', 'zenity', 'wx', etc....")
    parser.add_argument(
        '-C', action='store_true', help="read developer's comments")
    return parser.parse_args()


#def print_welcome():
#    """
#    if neither diameter nor price are known, print description
#    Docstring is duplicated because android is not detecting it properly.
#    """
#    if ARGS is None or ARGS.diameter is None and ARGS.price is None:

#        greeting = """
#        Calculate the area and unit price of a circular pizza."""
#        SHELL.welcome('Pizza Price Tool', greeting)


def linear_units():
    """
    Gets unit abbrev (cm or in.) from command line or stdin and returns as
    a str.
    """
    return 'cm' if ARGS is not None and ARGS.metric is True else 'in.'


def set_diameter(abbrev):
    """
    Gets diameter from args or stdin and return as a <cjh.kinematics.Disp>.
    """
    if ARGS is not None and ARGS.diameter is not None:
        diameter_dec = decimal.Decimal(ARGS.diameter)
    else:
        prompt = 'centimeters' if ARGS is not None and ARGS.metric is True else\
                 'inches'
        while True:
            try:
                diameter_dec = decimal.Decimal(
                    SHELL.input('{}? '.format(prompt)))
                break
            except decimal.InvalidOperation:
                Terminal.clear(1)
                continue
    return Disp(diameter_dec, u=abbrev)


def make_circle(diameter):
    """
    Takes <cjh.kinematics.Disp> diameter as argument, returns
    <cjh.geometry.Circle> circle
    """
    return Circle(diameter.mag / decimal.Decimal(2.0))

def _set_area_units(pizza):
    """
    Takes 1 arg <cjh.geometry.Circle>, returns type <cjh.geometry.Circle>
    """
    unit_str = 'cm^2' if ARGS is not None and ARGS.metric is True else 'sq. in.'
    pizza.area.units = Unit(unit_str)
    return pizza

def set_price():
    """
    Gets price from command line or stdin
    """
    if None not in (ARGS, ARGS.price):
        price = decimal.Decimal(ARGS.price)
    else:
        while True:
            try:
                price = decimal.Decimal(SHELL.input('price? $'))
                break
            except decimal.InvalidOperation:
                Terminal.clear(1)
                continue
    return Money(price)


def output_results(pizza, price):
    """
    Output area and unit price
    """
    results1 = '    Area of the pizza is {}'.format(pizza.area)
    results2 = '    The unit price of the pizza is {}/{}'.format(
        Money(decimal.Decimal(price.amount.item()) / pizza.area.mag), pizza.area.units.abbrev)
    if 'zenity' in (SHELL.interface, ARGS.shell):
        results1 = results1.replace('$', r'\\$')
        results2 = results2.replace('$', r'\\$')
    if (ARGS.diameter, ARGS.price) == (None, None) or SHELL == 'Tk':
        SHELL.output('')
        SHELL.notify(results1)
        SHELL.message(results2)
        Terminal.output('')
    else:
        SHELL.output('\n{}\n{}'.format(results1, results2))

    # Redesign this
    # pizza.area.draw()
    Terminal.output('')

#################
##  CONSTANTS  ##
#################
if __name__ == '__main__':
    ARGS = _parse_args()
    CONFIG = Config()
    
    if ARGS.nox is True:
        SHELL = Terminal()
    elif ARGS.shell is not None:
        SHELL = CONFIG.launch_selected_shell(ARGS.shell)
    else:
        SHELL = CONFIG.start_user_profile()
    ABBREV = linear_units()


############
##  MAIN  ##
############
def main():
    """
    Print welcome message then get pizza size and price and output area
    and unit price.
    """
    notebook(REMARKS)
    if ARGS.diameter is None and ARGS.price is None:
        SHELL.welcome(__doc__, 'Pizza Price Tool')
    Terminal.output('')

    while True:
        pizza_count = Circle.count + 1
        Terminal.output('\n' + Terminal.fx('un', 'Pizza {}'.format(pizza_count)))
        diameter = set_diameter(ABBREV)
        pizza = make_circle(diameter)
        pizza = _set_area_units(pizza)
        price = set_price()
        output_results(pizza, price)
        if (ARGS.diameter, ARGS.price) != (None, None):
            SHELL.exit()

if __name__ == '__main__':
    main()
    SHELL.start_app()
