#!/usr/bin/env python
#coding=utf8
"""
Classes for calculating pay checks, and other budget-related matters
"""
import array
import decimal
import locale
from datetime import timedelta, datetime, date

from versatiledialogs import terminal
from things import Thing
from cjh.money import Money
__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'

class PayPeriod(Thing):
    """
    A two-week pay period
    """

    def __init__(self, start_date=date.today(), wage=7.25, percent=33.3333, sh_obj=terminal.Terminal()):
        """
        set start_date, wage, and percent for withholding
        """
        super(PayPeriod, self).__init__()
        self.start_date = start_date
        self.wage = wage
        self.percent = percent
        self.shift_dict = {}
        self.shell = sh_obj
        
    @property
    def hoursf(self):
        """
        Returns the length of the PayPeriod in hrs as a float.
        """
        return self.hours_worked.seconds / 3600.0 + self.hours_worked.days * 24

    @property
    def hours_worked(self):
        """
        Total hours for the PayPeriod
        """
        hrs_worked = timedelta()
        for i in self.shift_dict.items():
            hrs_worked += i[1].duration
        return hrs_worked

    @staticmethod
    def withholding_wizard():
        """
        Figures out a reasonable estimate percent withheld base on
        past pay stubs.
        """
        terminal.Terminal.print_header()
        terminal.Terminal.output('Withholdings Wizard')
        terminal.Terminal.output('-' * 30)
        terminal.Terminal.output(
            'Please enter the following fields from a recent pay stub.')
        gross = decimal.Decimal(terminal.Terminal.input('Gross pay: $'))
        net = decimal.Decimal(terminal.Terminal.input('  Net pay: $'))
        percent = 100.0 * (1.00 - net / gross)
        #print('Percent withheld: %.3g%%' % (percent))
        terminal.Terminal.output('Percent withheld: {:.3g}%'.format(percent))
        terminal.Terminal.wait()
        return percent

    def add_shift(self, m_m, d_d):
        """
        m_m=numerical month, d_d=day of the month
        """
        self.shift_dict.update(
            {date(date.today().year, m_m, d_d): Shift(m_m, d_d, sh_obj=self.shell)})

    def __str__(self):
        width = terminal.Terminal.width()
        table = ''
        sorted_keys = sorted(self.shift_dict.keys())
        #for i in self.shift_dict.items():
        for i in sorted_keys:
            table += str(self.shift_dict[i])#.rstrip('\n').rstrip(' ')
        #table = table.replace('\n', '')
        locale.setlocale(locale.LC_ALL, '')
        rstr = ('  start date: {}'.format(self.start_date) +\
            '\n    end date: {}'.format(self.start_date + timedelta(14))  +\
            '\ncheck issued: {}'.format(self.start_date + timedelta(21)) +\
            '\n        wage: {}'.format(locale.currency(self.wage)) +\
            '\n  %% withheld: %.3g%%' % self.percent +\
            '\n\nHRS WORKED\tEST NET PAY\n' +\
            '%10.3g\t%11s' %
                (self.hoursf, locale.currency(self.est_net_pay().amount)) + '\n' +
                '-' * 29 + '\n\n' + table)
        if len(self.shift_dict) > 0:
            rstr += ('-' * 52)# + ' ')#.center(width)
        return rstr

    def gross_pay(self):
        """
        Before taxes, etc.
        """
        return Money(self.hoursf * self.wage)

    def est_net_pay(self):
        """
        Estimate Net Pay based on estimated percentage withheld.
        """
        return self.gross_pay() - Money(self.gross_pay().amount * self.percent / 100.0)


class WorkWeek(Thing):
    """
    Seven days of work.  Half of a PayPeriod
    """

    @staticmethod
    def weekday_name(day_number):
        """
        Turns an integer 0-6 into a dayname abbreviation.
        """
        day_num_dic = {0:'M', 1:'T', 2:'W', 3:'R', 4:'F', 5:'Sat.', 6:'Sun.'}
        try:
            day_str = day_num_dic[day_number]
        except KeyError:
            day_str = day_number
        return day_str


class Shift(Thing):
    """
    It would be possible to implement this as a child of cjh.scalars.Scalar
    """

    def __init__(self, *args, **kwargs):
        """
        form 1: Shift(month, day, hour_in, min_in, hour_out, min_out)
        form 2: Shift(month, day), with other values gathered interactively
        """
        if 'sh_obj' in kwargs.keys():
            sh_obj = kwargs['sh_obj']
        else: sh_obj = terminal.Terminal()
        super(Shift, self).__init__()
        month = args[0]
        day = args[1]
        self.date = date(date.today().year, month, day)
        try:
            time_in_array = array.array('i', [int(args[2]), int(args[3])])
            time_out_array = array.array('i', [int(args[4]), int(args[5])])
        except IndexError:
            time_in_array = array.array(\
                'i', [int(n) for n in sh_obj.input('time in: ').split(':')])
            if len(time_in_array) >= 2:
                time_out_array = array.array(\
                    'i', [int(n) for n in sh_obj.input('time out: ').split(
                        ':')])

        self.time_in = datetime(\
            self.date.year, self.date.month, self.date.day, time_in_array[0],\
            time_in_array[1])
        self.time_out = datetime(\
            self.date.year, self.date.month, self.date.day, time_out_array[0],\
            time_out_array[1])

    @property
    def duration(self):
        """
        Returns the length of the Shift.
        """
        return self.time_out - self.time_in

    @property
    def hoursf(self):
        """
        Length of Shift in hrs as a Decimal
        """
        return decimal.Decimal(float(self))

    def __str__(self):
        main_str = '|{:>5}) {}   |   {}   |   {}   |'.format(
            WorkWeek.weekday_name(
                self.date.weekday()
                ),#.center(5),
            self.date,
            '{} — {}'.format(
                self.time_in.strftime('%H:%M'), self.time_out.strftime('%H:%M')
                ),
            '%3.2g' % self.hoursf)#.center(cli.Cli.width())
      #  return ('-' * (len(main_str.strip()) - 2) + ' ').center(
      #      cli.Cli.width()) + '\n' + main_str + '\n'
        return ('-' * (len(main_str.strip()) - 2) + ' ')+ '\n' + main_str + '\n'
    #.center(
    #        cli.Cli.width()) 

    def __repr__(self):
        return "{}){{'in': '{}', 'out': '{}', 'delta': '{} hrs.'}}".format(\
            WorkWeek.weekday_name(\
            self.date.weekday()), self.time_in, self.time_out, self.hoursf)

    def __gt__(self, other):
        return self.duration > other.duration

    def __lt__(self, other):
        return self.duration < other.duration

    def __eq__(self, other):
        return self.duration == other.duration

    def __add__(self, other):
        return self.duration + other.duration

    def __radd__(self, other):
        try:
            return self.duration + other.duration
        except AttributeError:
            return self.duration + other

    def __float__(self):
        return self.duration.seconds / 3600.0 + self.duration.days * 24

    def __rshift__(self, other):
        """
        in this case, should be read "...is earlier than..."
        """
        if self.time_in < other.time_in:
            return True
        else: return False

    def __lshift__(self, other):
        """
        "...is later than...", "...happened after..."
        """
        if self.time_in > other.time_in:
            return True
        else: return False
