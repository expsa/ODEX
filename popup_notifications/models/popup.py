# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PopupNotification(models.Model):
    _name = "popup.notification"

    title = fields.Char()
    message = fields.Text()
    status = fields.Selection(selection=[('shown', 'shown'), ('draft', 'draft')], default='draft')
    partner_ids = fields.Many2many(comodel_name='res.users', relation='popup_res_user_rel', column1='pop_id',
                                   column2='user_id')

    @api.multi
    def get_notifications(self):
        result = []
        for obj in self:
            result.append({
                'title': obj.title,
                'message': obj.message,
                'status': obj.status,
                'id': obj.id,
            })
        return result


PopupNotification()
