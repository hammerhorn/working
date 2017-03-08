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
    return'${:,.2f}'.format(int(dollars * 100) / 100.0)

class Money(object):
    """
    Handles formatting of dollars; also calculates interest and sales tax
    """
    def __init__(self, amount, unit='USD'):
        self.amount = np.float32(amount)
        self.unit = unit

    def __float__(self):
        return self.amount

    def __str__(self):
        return money(self.amount) if self.unit == 'USD' else\
            ' '.join((self.unit, money(self.amount)[1:]))

    def __sub__(self, other):
        return Money(self.amount - other.amount) if self.unit == other.unit\
            else None

    def __truediv__(self, other):
        #if not isinstance(other, float):
        result = self.amount / float(other)
        if not isinstance(other, Money):
            #print other, 'is not Money'
            result = Money(result)
        return result

    def __lt__(self, other):
        return True if self.amount < other.amount else False

    def __mul__(self, other):
#        return self.amount * other
        return Money(self.amount * other)

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
