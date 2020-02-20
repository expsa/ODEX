# -*- coding: utf-8 -*-

from odoo import models, fields


class ResLang(models.Model):
    _name = "res.lang"
    _inherit = "res.lang"
    _description = "Language Flag"

    flag_image = fields.Binary('Flag Image')
