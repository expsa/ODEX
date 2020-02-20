# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import copysign


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    service_id = fields.Many2one('product.product', string='Service')
    restricted = fields.Boolean(string='Restricted', help='True if the order is restricted')
