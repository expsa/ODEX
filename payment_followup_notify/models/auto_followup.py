# -*- coding: utf-8 -*-
import time

from odoo import models, fields, api
from odoo.tools.translate import _


class FollowupLine(models.Model):
    _inherit = 'account_followup.followup.line'
    send_popup = fields.Boolean(
        string='Popup',
        help="When processing, it will raise popup",
        default=True,
    )

    @api.multi
    def get_users_from_group(self, group_id):
        users_ids = []
        sql_query = """select uid from res_groups_users_rel where gid = %s"""
        params = (group_id,)
        self.env.cr.execute(sql_query, params)
        results = self.env.cr.fetchall()
        for users_id in results:
            users_ids.append(users_id[0])
        return users_ids

    @api.model
    def create_popup(self):
        ResPartner = self.env['res.partner']
        result = self.env['res.partner'].with_context(
            date=time.strftime('%Y-%m-%d')).get_partners_in_need_of_action_and_update()
        for partner_id in result.keys():
            followup_level = self.browse(result[partner_id][0])
            partner = ResPartner.browse(partner_id)
            if followup_level.manual_action:
                partner.do_partner_manual_action()
            if followup_level.send_email:
                partner.do_partner_mail()
            if followup_level.send_letter:
                message = "%s<I> %s </I>%s" % (
                    _("Follow-up letter of "), followup_level.name,
                    _(" will be sent"))
                partner.message_post(body=message)
            if followup_level.send_popup:
                accountant_group = self.env['ir.model.data'].xmlid_to_res_id(
                    'account.group_account_invoice')
                account_users = self.get_users_from_group(accountant_group)
                already_has_popup= self.env['popup.notification'].sudo().search([('message','ilike',partner.name),('status','=','draft')]).ids
                if not already_has_popup:
                    values = {'status': 'draft', 'title': u'Be notified about',
                              'message': "Do not forget to follow up with %s regarding next payment" % (partner.name),
                              'partner_ids': [(6, 0, account_users)]}

                    self.env['popup.notification'].create(values)

        ResPartner.browse(result.keys()).update_next_action(batch=True)


FollowupLine()
