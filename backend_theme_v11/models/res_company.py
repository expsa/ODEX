# -*- coding: utf-8 -*-

from odoo import models, fields

class ResCompany(models.Model):

    _inherit = 'res.company'

    dashboard_background = fields.Binary(attachment=True)