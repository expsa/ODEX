# -*- coding: utf-8 -*-
from odoo import api, models, fields, _, exceptions
from . import Hijri


class Ummalqura(models.TransientModel):
    _name = 'odex.hijri'

    def _calculate_hijri(self, date):
        h = Hijri(date)
        return h.format()

    def convert(self, date):
        return self._calculate_hijri(date)