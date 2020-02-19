# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    expire_calibration = fields.Integer(string='Days Between Calibrations')
    notify_expire = fields.Integer(string='Notify Expire After')

    @api.multi
    def set_values(self):
        super(StockConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('expire_calibration', (self.expire_calibration or 0))
        set_param('notify_expire', (self.notify_expire or False))

    @api.model
    def get_values(self):
        res = super(StockConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        expire_calibration =int(get_param('expire_calibration', default=0))
        notify_expire = int(get_param('notify_expire', default=0))
        res.update(
            expire_calibration=expire_calibration,
            notify_expire=notify_expire,
        )
        return res


StockConfigSettings()
