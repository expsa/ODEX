# -*- coding: utf-8 -*-
from .iclib.hijri import ummqura
import datetime

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

from odoo import _

import re

PHONE_FORMAT = re.compile(r'^(((00|\+{1})\d{3})|(0))(\s*\d{9})$')
EMAIL_FORMAT = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
ID_FORMAT = re.compile(r'^\d{10}$')


NOW = datetime.date.today()

NAMES = {
    1: ('Muharram'),
    2: ('Safar'),
    3: ('Rabe Al Awwal'),
    4: ('Rabe Al Thane'),
    5: ('Jumad Al Awwal'),
    6: ('Jumad Al Thane'),
    7: ('Rajab'),
    8: ('Shaaban'),
    9: ('Ramadan'),
    10: ('Shawwal'),
    11: ('Thul Qaeda'),
    12: ('Thul Hijja'),
}


class Hijri(object):
    def __init__(self, gdate=NOW):
        '''
            Accepts gregorian date and returns
            Hijri Date.
        '''

        self.gdate, self.is_datetime = self.check_gdate(gdate)

        self.convert()


    def check_gdate(self, gdate):
        result = False
        is_datetime = False
        if isinstance(gdate, str):
            ''' try to convert the date str provided to date object'''
            try:
                result = datetime.datetime.strptime(gdate, DATE_FORMAT)
                is_datetime = False
            except ValueError as e:
                try:
                    result = datetime.datetime.strptime(gdate, DATETIME_FORMAT)
                    is_datetime = True
                except ValueError as e:
                    raise ValueError(u'The Date provided cannot be converted to Hijri, check date format')
        elif isinstance(gdate, datetime.date):
            result = gdate
            is_datetime = isinstance(gdate, datetime.datetime)

        else:
            raise Warning(_('Cannot convert date to hijri!'))
        return result, is_datetime


    def convert(self):
        self._c = ummqura
        # self._jd = self._c.gregorian_to_jd(self.gdate.year, self.gdate.month, self.gdate.day)
        # self._hijri = self._c.jd_to_islamic(self._jd)
        kk = self._c.from_gregorian(self.gdate.year, self.gdate.month, self.gdate.day)
        self._hijri = kk[:-1]
        self._t = kk[-1]

    def revert(self, raw):
        # jd = self._c.islamic_to_jd(*raw)
        gregorian = self._c.to_gregorian(*raw)
        return datetime.date(*gregorian)




    @property
    def raw(self):
        return self._hijri
    @raw.setter
    def raw(self, value):
        raise ValueError('Readonly value!')
    

    def format(self):
        try:
            if not self.is_datetime:
                return u'{}-{:02d}-{:02d}'.format(self.raw[0], self.raw[1], self.raw[2])
            else:
                return u'{:02d}-{:02d}-{} {}'.format(self.raw[2], self.raw[1], self.raw[0], self.gdate.strftime('%H:%M:%S'))
        except Exception as e:
            raise ValueError(e.args)


from . import res_city
from . import hijri
