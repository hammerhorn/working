#!/usr/bin/env python
#coding=utf8
"""
g to $, or $ to g

DISCOUNTS
--family
--shake
"""
import decimal
import sys
import time

from cjh.fiziko.scalars import Scalar
from cjh.misc import catch_help_flag, notebook
from cjh.money import Money

from ttyfun.unix import Figlet

from versatiledialogs.config import Config
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

###############
#  CONSTANTS  #
###############
REMARKS = """
    - draw a graph with PyPlot or my Graph class
    - make into a full-fledged POS system
    + make functs available from inerpretor
    + Money object

    * above a certain amount, maybe it should round to the nearest $5
    * unit conversions
    * research business software
    * records encryption
    * include unit price
    * LaTeX?"""


class Herbo(object):
    """
    dollars -> grams
    grams -> dollars
    """
    def __init__(self, str_arg, sh_obj=Terminal()):
        #DISCOUNT, SHAKE = process_discounts()
        if sh_obj.interface == 'term' and sh_obj.platform == 'Linux':
            fig_writer = Figlet('mono9', 'metal')

        # gramoj -> dolaroj
        if str_arg.endswith('g'):
            str_arg = str_arg.rstrip('g')
            float_g = float(str_arg.rstrip())
            self.grams = Scalar(float_g, 'g')
            self.dollars = Herbo.grams_to_dollars(self.grams)
            if sh_obj.interface in ['wx', 'Tk']:
                sh_obj.message(self.dollars)
            elif sh_obj.interface == 'term' and sh_obj.platform == 'Linux':
                fig_writer.output('\\' + str(self.dollars))
                time.sleep(2)
                Terminal.clear(10)
            else:
                sh_obj.output(self.dollars)

        # dolaroj -> gramoj
        elif str_arg.startswith('$'):
            str_arg = str_arg.lstrip('$')
            self.dollars = Money(float(str_arg))
            self.grams = Herbo.dollars_to_grams(self.dollars)
            if sh_obj.interface in ['wx', 'Tk']:
                sh_obj.message('{}'.format(self.grams))
            elif sh_obj.interface == 'term' and sh_obj.platform == 'Linux':
                fig_writer.output(self.grams.__str__())
                time.sleep(2)
                Terminal.clear(10)
            else:
                sh_obj.output('{}'.format(self.grams))

    @staticmethod
    def grams_to_dollars(mass_g):
        """
        Takes Scalar mass_g; returns decimal.Decimal or Money dollars
        """
        if isinstance(mass_g, float):
            mass_g = Scalar(mass_g, 'g')
        if DISCOUNT is True:
            d_float = mass_g.mag * decimal.Decimal(8.4507042253521)
        elif mass_g < Scalar(3.5, 'g'):
            d_float = mass_g.mag * decimal.Decimal(11.267605633802)
        else:
            d_float = mass_g.mag * decimal.Decimal(8.4507042253521) + 10
        dollars = Money(int(round(d_float)))
        if SHAKE is True:
            dollars /= decimal.Decimal(2.0)
        return dollars

    @staticmethod
    def dollars_to_grams(dol):
        """
        Takes float dol (dollars); returns Scalar grams
        """
        if DISCOUNT is True:
            g_float = (dol / 8.4507042253521).amount
        elif dol < Money(40):
            g_float = dol * 0.08875
        else:
            g_float = ((dol - Money(10)) / 8.4507042253521156).amount
        grams = Scalar(g_float, 'g')
        if SHAKE is True:
            grams *= 2.0
        grams *= 10
        grams_int = int(grams.mag)
        grams_float = float(grams_int)
        grams_float /= 10.0
        return Scalar(grams_float, 'g')


def process_discounts():
    """
    Parse flag arguments: --family (-d), --shake (-s)
    """
    inter_set = {'-d', '--family', '-ds', '-sd'} & set(sys.argv[1:])
    if len(inter_set) > 0:
        discount = True

        if list(inter_set)[0] not in ['-ds', '-sd']:
            del sys.argv[sys.argv.index(list(inter_set)[0])]
    else:
        discount = False

    inter_set = {'--shake', '-ds', '-sd', '-s'} & set(sys.argv[1:])
    if len(inter_set) > 0:
        shake = True
        del sys.argv[sys.argv.index(list(inter_set)[0])]
    else:
        shake = False
    return discount, shake


def main():
    """
    main function
    """
    try:
        str_arg = sys.argv[1]
        assert str_arg.endswith('g') or str_arg.startswith('$')
        Herbo(str_arg, SHELL)
#        return

    except (IndexError, AssertionError):
        catch_help_flag(__doc__, SHELL, condition=True)



if __name__ == '__main__':
    CONFIG = Config()
    if {'-n', '--nox'} & set(sys.argv):
        SHELL = Terminal()
    else:
        SHELL = CONFIG.start_user_profile()
        if SHELL.interface in ['wx', 'Tk']:
            SHELL.center_window()
    notebook(REMARKS)
    DISCOUNT, SHAKE = process_discounts()
    main()




