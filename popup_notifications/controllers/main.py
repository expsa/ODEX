# -*- coding: utf-8 -*-

import logging

import odoo.http as http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PopupController(http.Controller):

    @http.route('/popup_notifications/notify', type='json', auth="none")
    def notify(self):
        user_id = request.session.get('uid')
        return request.env['popup.notification'].sudo().search(
            [('partner_ids', '=', user_id), ('status', '!=', 'shown')]
        ).get_notifications()

    @http.route('/popup_notifications/notify_ack', type='json', auth="none")
    def notify_ack(self, notif_id):
        notif_obj = request.env['popup.notification'].sudo().browse([notif_id])
        if notif_obj:
            notif_obj.status = 'shown'


PopupController()
