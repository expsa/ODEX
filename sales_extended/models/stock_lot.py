# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _


class ProductLot(models.Model):
    _inherit = 'stock.production.lot'

    lot_calibration_ids = fields.One2many(comodel_name='stock.lot.calibration', inverse_name='lot_id',
                                          string='Calibration Lines')
    end_user_id = fields.Many2one(comodel_name='res.partner', string='End User')
    warranty_months = fields.Integer(string='Warranty Months', related='product_id.product_tmpl_id.warranty_months')
    warranty_partner_id = fields.Many2one(comodel_name='res.partner', domain=[('supplier', '=', True)],
                                          string='Warranty Provider',
                                          related='product_id.product_tmpl_id.warranty_partner_id')

    @api.multi
    def update_stock_lot_calibrations(self):
        dummy, view_id = self.env['ir.model.data'].get_object_reference('sales_extended',
                                                                        'update_lot_calibration_form')
        return {
            'name': _("Update calibration for lot %s ") % (self.name),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'update.lot.calibration',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_lot_id': self.id,
            }
        }


ProductLot()



