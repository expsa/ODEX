# -*- coding: utf-8 -*-
from odoo import models, fields,api
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_terms_id = fields.Many2one(comodel_name='sale.terms.conditions', string='Default Term')

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('default_terms_id', (self.default_terms_id.id or False))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        default_term_id = literal_eval(get_param('default_terms_id', default='False'))
        res.update(
            default_terms_id=default_term_id,
        )
        return res


ResConfigSettings()
