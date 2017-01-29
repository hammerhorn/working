#!/usr/bin/python
#coding=utf8
"""
cli.money() should be incorporated into Money.__str__()
"""
try:
    import numpy as np
except ImportError:
    pass

def money(dollars):
    """
    Takes a float and returns a str, formatted as dollars.
    Belongs in the class Money
    """
    dollars = int(dollars * 100) / 100.0
    return'${:,.2f}'.format(dollars)

class Money(object):
    """
    Handles formatting of dollars; also calculates interest and sales tax
    """
    def __init__(self, amount, unit='USD'):
        self.amount = amount
        self.unit = unit

    def __str__(self):
        if self.unit == 'USD':
            return money(self.amount)
        else:
            return self.unit + ' ' + money(self.amount)[1:]

    def __sub__(self, other):
        if self.unit == other.unit:
            return Money(self.amount - other.amount)
        else:
            return None

    def __div__(self, other):
        return Money(self.amount / other)

    def __lt__(self, other):
        if self.amount < other.amount:
            return True
        else:
            return False

    def __mul__(self, other):
        return self.amount * other

    def interest(self, rate, years, periods_per_yr=None):
        """ calcultate compound interest """
        if periods_per_yr is None:
            amt = self.amount * np.e ** (rate * years)
        else:
            # an unfortunate hacky way of doing things
            # in order to be compatible with numpy
            amt = self.amount * (1 + rate / periods_per_yr) ** np.round(
                periods_per_yr * years - 0.49)
        return Money(amt)

    def sales_tax(self, rate=0.07):
        """ calculate sales tax """
        return Money(self.amount * (1 + rate))
