# -*- coding: utf-8 -*-
from odoo import models, fields


class ScrapOrder(models.Model):
    _inherit = 'stock.scrap'

    scrap_notes = fields.Text(string='Scrap Notes')


ScrapOrder()
