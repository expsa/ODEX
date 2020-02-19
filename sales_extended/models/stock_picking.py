# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    delivery_dated = fields.Date(string='Dated')
    po_no = fields.Char(string='P.O No.')

    @api.multi
    def button_validate(self):
        self.ensure_one()
        lines_to_check = self.move_line_ids
        if self.picking_type_id.code == 'outgoing':
            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(_('You need to supply a lot/serial number for %s.') % product.display_name)
                    else:
                            get_param = self.env['ir.config_parameter'].sudo().get_param
                            expire_calibration = int(get_param('expire_calibration', default=0))
                            if expire_calibration:
                                month_ago_date = (datetime.now().date() - timedelta(days=expire_calibration)).strftime(
                                    '%Y-%m-%d')
                                last_calibration = line.lot_id.lot_calibration_ids.sorted(lambda x: x.date, reverse=True)
                                if last_calibration:
                                    last_calibration_date = last_calibration[0].date
                                    if datetime.strptime(last_calibration_date,
                                                         DEFAULT_SERVER_DATE_FORMAT).date() < datetime.strptime(
                                        month_ago_date, DEFAULT_SERVER_DATE_FORMAT).date():
                                        raise UserError(_('You need to calibrate product %s with lot %s.') % (
                                            product.display_name, line.lot_id.name))
                                if not last_calibration:
                                    raise UserError(_('You need to add calibration to product %s with lot %s.') % (
                                        product.display_name, line.lot_id.name))
        return super(StockPicking, self).button_validate()


StockPicking()
