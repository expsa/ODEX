# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_followup_type = fields.Selection(selection=[('budget', 'Budget'),
                                                     ('undirected_tender', 'Undirected Tender'),
                                                     ('directed_tender', 'Directed Tender'),
                                                     ('project', 'Project')], default='budget', string='Sale Followup',
                                          required=True)
    ending_date = fields.Date(string='Ending Date')
    mark_followed = fields.Boolean()

    @api.model
    def create_followup_activity(self):
        followup_id = self.env.ref('quotation_followup.demo_followup1')
        for item in followup_id.followup_line:
            activity_type = self.env.ref('quotation_followup.mail_activity_follow_quota')
            if item.sale_followup_type == 'undirected_tender':
                ending_date = str(datetime.now().date() + timedelta(days=item.delay))
                orders_match = self.search(
                    [('sale_followup_type', '=', item.sale_followup_type), ('state', '=', 'draft'),
                     ('ending_date', '=', ending_date), ('mark_followed', '=', False)])
            else:
                date_order = (datetime.now() - timedelta(days=item.delay)).strftime(DEFAULT_SERVER_DATE_FORMAT)
                date_from = date_order + ' 00:00:00'
                date_to = date_order + ' 23:59:59'
                orders_match = self.search(
                    [('sale_followup_type', '=', item.sale_followup_type), ('state', '=', 'draft'),
                     ('date_order', '>=', date_from),
                     ('date_order', '<=', date_to), ('mark_followed', '=', False)])
            for order in orders_match:
                if item.send_popup:
                    user_id = order.user_id.id or order.create_uid.id
                    values = {'status': 'draft', 'title': u'Be notified about',
                              'message': "Do not forget to follow up with quota %s " % (order.name),
                              'partner_ids': [(6, 0, [user_id])]}
                    self.env['popup.notification'].create(values)
                if item.send_activity:
                    self.env['mail.activity'].create({
                        'summary': 'Follow up the quota %s'%(order.name),
                        'date_deadline': str(datetime.now().date() + timedelta(days=2)),
                        'activity_type_id': activity_type.id,
                        'user_id': order.user_id.id or order.create_uid.id,
                        'note': 'Follow up with this quotation with number %s'%(order.name),
                        'res_model_id': self.env.ref('sale.model_sale_order').id,
                        'res_id': order.id,
                    })
                order.write({'mark_followed': True})


SaleOrder()
