# -*- coding: utf-8 -*-
from odoo import api, fields, models


class UpdateLotCalibration(models.TransientModel):
    _name = 'update.lot.calibration'
    _rec_name = 'lot_id'
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today, index=True)
    location_id = fields.Many2one(comodel_name='stock.location', required=True, string='Location')
    technician_id = fields.Many2one(comodel_name='res.users', string='Technician', required=True,
                                    default=lambda s: s.env.user.id)
    feedback = fields.Text(string='Feedback')

    @api.multi
    def confirm_calibration(self):
        self.env['stock.lot.calibration'].sudo().create({
            'lot_id': self.lot_id.id,
            'date': self.date,
            'location_id': self.location_id.id,
            'technician_id': self.technician_id.id,
            'feedback': self.feedback
        })
        return True


UpdateLotCalibration()
