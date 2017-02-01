#!/usr/bin/env python
#coding=utf8
"""
Classes for monomial and polynomial arithmetic and evaluation.
(* Output options like LaTeX, HTML?)
"""
import decimal
import sys
import traceback

from cjh.letterator import Letter
from fiziko.scalars import Minusable
from things import Thing
from versatiledialogs.lists import PlainList
from versatiledialogs.terminal import Terminal

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class Term(Thing, Minusable):
    """
    Term is a monomial expression of form coef(x)^exp.
    """

    def __init__(self, coef=0.0, exp=0.0):
        super(Term, self).__init__()
        self.coef = decimal.Decimal(coef)
        self.exp = decimal.Decimal(exp)

    def __repr__(self):
        string = ""
        if self.coef != 1.0 or self.exp == 0.0:
            if self.coef == -1.0:
                string += '-'
                if self.exp == 0:
                    string += '1'
            else: string += '{:.5g}'.format(self.coef)
        if self.coef != 0.0 and self.exp != 0.0:
            string += 'x'
            if self.exp != 1.0: # use unicode superscripts here
                string += '^{:.5g}'.format(float(self.exp))
        return string

    def __abs__(self):
        return Term(abs(self.coef), self.exp)

    def __add__(self, other):
        if type(other) == Polynom:
            return other + self
        else:
            term_list = [self, other]
            try:
                return Polynom(term_list)
            except AttributeError:
                return Polynom([self, Term(other, 0)])

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        try:
            product = Term((self.coef * other.coef), (self.exp + other.exp))
        except AttributeError:
            product = Term((self.coef * decimal.Decimal(other)), (self.exp))
        return product

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        try:
            quotient = Term((self.coef / other.coef), (self.exp - other.exp))
        except AttributeError:
            quotient = Term((self.coef / other), (self.exp))
        return quotient

    def __rdiv__(self, other):
        if type(other) == int or type(other) == float:
            return Term(other, 0) / self

    def __pow__(self, power):
        return Term(
            self.coef ** decimal.Decimal(power),
            self.exp * decimal.Decimal(power))

    def __eq__(self, other):
        try:                   # if other is a Term
            if self.coef == other.coef and self.exp == other.exp:
                value = True
            else: value = False
        except AttributeError: # if other is a float
            if self.coef == other and self.exp == 1:
                value = True
            else: value = False
        return value

    def __gt__(self, other):
        if self.exp > other.exp or\
            self.exp == other.exp and self.coef > other.coef:
            return True
        else: return False

    def __ge__(self, other):
        if self > other or self == other:
            return True
        else: return False

    def __lt__(self, other):
        if self.exp < other.exp or\
            self.exp == other.exp and self.coef < other.coef:
            return True
        else: return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        else: return False

    def __call__(self, x_val):
        """
        self(x) == self.eval(x)
        """
        return round(self.eval(x_val), 4)

    def eval(self, x_val):
        """
        self.eval(x) == self.__call__(x)
        """
        if self.exp == 0:
            return self.coef
        else: return self.coef * decimal.Decimal(x_val) ** self.exp


    def dx(self, *args):
        """
        derivative
        """
        coef_float = self.coef * self.exp
        exp_float = self.exp - 1
        result = Term(coef_float, exp_float)
        if len(args) > 0:
            args = list(args)
            value = float(args[0])
            return result(value)
        else: return result

    def S_dx(self, *args):
        """
        integral
        """
        coef_float = self.coef / (self.exp + 1)
        exp_float = self.exp + 1
        result = Term(coef_float, exp_float)
        if len(args) > 0:
            args = list(args)
            value = float(args[0])
            return result(value)
        else: return result

class Polynom(Thing, Minusable):
    """
    Polynom is a polynomial, composed of the sum of monomial Terms.
    """

    letter_maker = Letter.lower_gen(start_letter='f')

    def __init__(self, term_list=None):
        """
        term_list is of type Term[]
        """
        if term_list is None:
            term_list = [Term()]
        super(Polynom, self).__init__()
        self.dict = {}
        self.list_ = []

        for term in term_list:
            exp = term.exp

            # add to dictionary
            if exp in self.dict.keys():
                self.dict[exp] += term.coef
            else: self.dict[exp] = term.coef

        try:
            exps = list(self.dict.keys())
            #exps.sort()

            sorted(exps)
            exps = exps[::-1]

            for exp in exps:
                self.list_.append(Term(self.dict[exp], exp))
        except KeyError:
            pass
        self.letter = next(self.__class__.letter_maker)

    def __repr__(self):
        string = '{}(x) = '.format(self.letter)
        if len(self) == 0  or (len(self) == 1 and self.list_[0].coef == 0.0):
            string += '0'
        else:
            string += str(self.list_[0])
            for item in range(1, len(self)):
                if self.list_[item].coef > 0:
                    string += ' + {}'.format(self.list_[item])
                else:
                    string += ' - {}'.format(abs(self.list_[item]))
        return string

    def __add__(self, other):
        sum_ = Polynom(self.list_)

        # Create dictionary representing sum
        # if addend is Polynom
        try:
            for term in other.list_:
                if term.exp in sum_.dict.keys():
                    sum_.dict[term.exp] += term.coef
                else: sum_.dict[term.exp] = other.coef #?
        except AttributeError:

            # if addend is Term
            try:
                if other.exp in sum_.dict.keys():
                    sum_.dict[other.exp] += other.coef
                else: sum_.dict[other.exp] = other.coef
            except AttributeError:

                # otherwise, addend is int or float
                if 0 in sum_.dict.keys():
                    sum_.dict[0] += decimal.Decimal(other)
                    sum_.dict[0] = round(sum_.dict[0], 4)
                else: sum_.dict[0] = other

        # Convert dict of numbers to list of Terms
        sum_.list_ = []
        for exp in range(int(max(sum_.dict.keys())), -1, -1):
            try:
                if sum_.dict[exp] == 0.0:
                    del sum_.dict[exp]
                else: sum_.list_.append(Term(sum_.dict[exp], exp))
            except KeyError:
                pass
        return sum_

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        poly = self

        # if other is a number
        # use of float here might result in loss of precision
        poly.dict = {
            coef_:(decimal.Decimal(other) * self.dict[coef_])
            for coef_ in self.dict.keys()}

        # Convert dict of numbers to list of Terms
        poly.list_ = []
        for exp in range(int(max(poly.dict.keys())), -1, -1):
            try:
                if poly.dict[exp] == 0.0:
                    del poly.dict[exp]
                else: poly.list_.append(Term(poly.dict[exp], exp))
            except KeyError:
#               print(traceback.format_exc())
                pass
        return poly

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        poly = Polynom()
        # if other is a number
        poly.dict = {(coef_ * other):self.dict[coef_]\
            for coef_ in self.dict.keys()}

        # Convert dict of numbers to list of Terms
        poly.list_ = []
        for exp in range(int(max(poly.dict.keys())), -1, -1):
            try:
                if poly.dict[exp] == 0.0:
                    del poly.dict[exp]
                else: poly.list_.append(Term(poly.dict[exp], exp))
            except KeyError:
                Terminal.output(traceback.format_exc())
        return poly

    def __iter__(self):
        """
        Returns a listiterator object of Terms contained.
        """
        return iter(self.list_)

    def __len__(self):
        #perhaps length of f(x) = 0 should be 0
        list_ = [term for term in self.list_ if term.coef != 0.0]
        return len(list_)

    def __getitem__(self, power):
        """
        The index is the exponent.  Returns a zero if there is nothing
        in that "slot".
        """
        try:
            value = float(self.dict[power])
        except KeyError:
            value = 0.0
        return value


    def wizard(self, page_txt_obj=None, sh_class=Terminal):
        """
        Interactively populates the Polynomial.
        """
        self.list_ = []
        menu2 = PlainList(['add monomial term', 'DONE', 'Quit'])
        menu2.label = 'Polynomial Wizard'
        while True:
            sel2 = Terminal().make_page(
                'Polynomial', page_txt_obj, lambda: sh_class.list_menu(menu2))
            if sel2 == 1:

                # Add monomial term
                Terminal.output('')
                coef_str = ''
                while len(coef_str) == 0:
                    try:
                        coef_str = sh_class.input('coefficient?')
                        coef = float(coef_str)
                    except ValueError:
                        coef_str = ''
                        continue

                pow_str = ''
                while len(pow_str) == 0:
                    pow_str = sh_class.input('power?')
                pow_ = float(pow_str)
                self.list_.append(Term(coef, pow_))
                menu2.label = str(self)
                self.dict.clear()
                for index in range(len(self)):
                    exponent = self.list_[index].exp
                    if exponent in self.dict.keys():
                        self.dict[exponent] += self.list_[index].coef
                    else: self.dict[exponent] = self.list_[index].coef
            elif sel2 == 2:
                break
            elif sel2 == 3:
                sys.exit()

    def eval(self, x_val):
        """
        Evaluate the Polynom for a particular value.
        """
        sum1 = decimal.Decimal(0.0)
        for index in range(len(self)):
            sum1 += self.list_[index].eval(x_val)
        return sum1

    def dx(self, *args):
        """
        derivative
        """
        new_pnom = Polynom([])
        for term in self.list_:
            new_pnom += term.dx()
        if len(args) > 0:
            args = list(args)
            value = float(args[0])
            return new_pnom(value)
        return new_pnom

    def S_dx(self, *args):
        """
        integral
        """
        new_pnom = Polynom([])
        for term in self.list_:
            new_pnom += term.S_dx()
        if len(args) > 0:
            args = list(args)
            value = float(args[0])
            return new_pnom(value)
        return new_pnom

    def __call__(self, x_val):
        """
        Rounded version of self.eval()
        """
        return round(self.eval(x_val), 4)
