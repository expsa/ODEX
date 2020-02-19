# -*- coding: utf-8 -*-
import time
import datetime
import math
from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from datetime import datetime, timedelta, date

class StockPickingCustom(models.Model):
    _inherit = 'stock.picking'

    department_id = fields.Many2one('hr.department')
    category_id = fields.Many2one('product.category')

# class StockJournal(models.Model):
#     _name = 'stock.journal'
#
#     name = fields.Char(required=True)
#     location_id = fields.Many2one('stock.location')
#     exchange = fields.Boolean()


class StockInventoryCustomLine(models.Model):
    _inherit = 'stock.inventory.line'

    remain = fields.Float(compute="ComputeRemain")
    reason = fields.Char()
    
    @api.multi
    @api.depends('theoretical_qty','product_qty')
    def ComputeRemain(self):
        """
            compute the remain by subtracting the theo from the real
        """
        for rec in self:
            rec.remain = rec.theoretical_qty - rec.product_qty


class StockInventoryCustom(models.Model):
    _inherit = 'stock.inventory'

    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirmed'),
        ('inprogress','In Progress'),
        ('done','Validated'),
        ('cancel','Cancelled'),
    ],default='draft')

    @api.multi
    def action_confirm_custom(self):
        """
            Change document state form Draft to Confrimed
        """
        if len(self.line_ids)!=0:        
            self.write({
                'state':'inprogress',
            })
        else:
            raise ValidationError(_("You can't Confirm without adding products"))