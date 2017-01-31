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
    args = parser.parse_args()
    return args


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
    if ARGS is not None and ARGS.metric is True:
        abbrev = 'cm'
    else:
        abbrev = 'in.'
    return abbrev


def set_diameter(abbrev):
    """
    Gets diameter from args or stdin and return as a <cjh.kinematics.Disp>.
    """
    if ARGS is not None and ARGS.diameter is not None:
        diameter_dec = decimal.Decimal(ARGS.diameter)
    else:
        if ARGS is not None and ARGS.metric is True:
            prompt = 'centimeters'
        else:
            prompt = 'inches'
        #Cli.output('')
        while True:
            try:
                diameter_dec = decimal.Decimal(SHELL.input('{}? '.format(prompt)))
                break
            except decimal.InvalidOperation:
                Terminal.clear(1)
                continue
    diameter = Disp(diameter_dec, u=abbrev)
    return diameter


def make_circle(diameter):
    """
    Takes <cjh.kinematics.Disp> diameter as argument, returns
    <cjh.geometry.Circle> circle
    """
    radius = diameter.mag / decimal.Decimal(2.0)
    pizza = Circle(radius)
    return pizza


def _set_area_units(pizza):
    """
    Takes 1 arg <cjh.geometry.Circle>, returns type <cjh.geometry.Circle>
    """
    if ARGS is not None and ARGS.metric is True:
        pizza.area.units = Unit('cm^2')
    else:
        pizza.area.units = Unit('sq. in.')
    return pizza


def set_price():
    """
    Gets price from command line or stdin
    """
    if ARGS is not None and ARGS.price is not None:
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
        Money(price / pizza.area.mag), pizza.area.units.abbrev)
    if SHELL.interface in ['zenity'] or ARGS.shell == 'zenity':
        results1 = results1.replace('$', r'\\$')
        results2 = results2.replace('$', r'\\$')
    if ARGS.diameter is None and ARGS.price is None or SHELL.interface == 'Tk':
        SHELL.output('')
        SHELL.notify(results1)
        SHELL.message(results2)

        Terminal.clear(1)
        Terminal.output('')
    else:
        SHELL.output('\n{}\n{}'.format(results1, results2))

    pizza.area.draw()
    Terminal.output('')

#################
##  CONSTANTS  ##
#################
if __name__ == '__main__':
    ARGS = _parse_args()
    CONFIG = Config()

    if ARGS is not None and ARGS.nox is True:
        SHELL = Terminal()
    elif ARGS is not None and ARGS.shell is not None:
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
    #    #Cli.print_header()
        SHELL.welcome(__doc__, 'Pizza Price Tool')
    #    pass
    #else:
    Terminal.output('')

    while True:
        pizza_count = Circle.count + 1
        Terminal.output(Terminal.fx('un', 'Pizza {}'.format(pizza_count)))
        diameter = set_diameter(ABBREV)
        pizza = make_circle(diameter)
        pizza = _set_area_units(pizza)
        price = set_price()
        output_results(pizza, price)
        if ARGS.diameter is not None or ARGS.price is not None:
            SHELL.exit()


if __name__ == '__main__':
    main()
    SHELL.start_app()
