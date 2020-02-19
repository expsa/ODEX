# -*- coding: utf-8 -*-
from odoo import models, fields


class TermsConditions(models.Model):
    _name = 'sale.terms.conditions'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    default_term = fields.Boolean(string='Default Term')
    include_bank_details=fields.Boolean()
    bank_id=fields.Many2one(comodel_name='res.bank',string='Bank')
    desc = fields.Html(string='Description',translate=True)
    arabic_desc = fields.Html(string="Arabic Terms")


TermsConditions()
