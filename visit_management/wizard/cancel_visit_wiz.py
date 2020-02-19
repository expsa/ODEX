# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class CancelVisit(models.Model):
    _name = 'cancel.visit.reason'

    cancel_reason = fields.Html(string='Cancel Reason', required=True)

    @api.multi
    def approve_cancel(self):
        current_event_id = self.env['calendar.event'].sudo().browse(self._context.get('active_id'))

        if current_event_id.user_id:

            manager = self.env['crm.team'].sudo().search([('member_ids', 'in', [current_event_id.user_id.id])])
            message = "The visit  '%s' has been canceled by '%s' ,due to %s" % (
            current_event_id.name, manager.user_id.name, self.cancel_reason)
            followers=list(set([manager.user_id.partner_id.id,self.env.user.partner_id.id,current_event_id.user_id.partner_id.id]))
            values = {
                'body': message,
                'model': 'calendar.event',
                'message_type': 'notification',
                'no_auto_thread': True,
                'res_id': current_event_id.id,
                'partner_ids': [(6, 0, followers)]
            }
            if False in followers:
                followers.remove(False)
            current_event_id.message_post(body=message, subtype="mail.mt_comment",partner_ids=followers)
        current_event_id.write({'state': 'progress', 'cancel_reason': self.cancel_reason})
        return True


CancelVisit()
