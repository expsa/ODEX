# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class City(models.Model):
    _name = 'res.country.city'


    @api.depends('code', 'name')
    def _load_country_id(self):
        for r in self:
            r.country_id = self.env.ref('base.sa')

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')

    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country', compute='_load_country_id', store=True)

