# -*- coding: utf-8 -*-
##############################################################################
#
#    LCT, Life Connection Technology
#    Copyright (C) 2011-2012 LCT
#
##############################################################################

from odoo import api, fields, models, _

class ResourceResource(models.Model):
    _inherit = 'resource.resource'

    name = fields.Char(required=True, translate=True)
