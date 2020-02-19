# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _


class LotCalibration(models.Model):
    _name = 'stock.lot.calibration'

    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot', required=True)
    date = fields.Date(string='Date', required=True)
    location_id = fields.Many2one(comodel_name='stock.location', required=True, string='Location')
    technician_id = fields.Many2one(comodel_name='res.users', string='Technician', required=True)

    feedback = fields.Text(string='Feedback')

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
    def notify_expire_activity(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        notify_expire = int(get_param('notify_expire', default=0))
        expire_calibration = int(get_param('expire_calibration', default=0))
        got_data = False
        followup_table = '''
                <table border="2" width=100%%>
                <tr>
                    <td>''' + _("Product") + '''</td>
                    <td>''' + _("Lot") + '''</td>
                    <td>''' + _("Last Calibration Date") + '''</td>
                    <td>''' + _("Feedback") + '''</td>
                </tr>
                <tr>
                '''
        if notify_expire:
            for lot in self.env['stock.production.lot'].sudo().search([]):
                last_calibration = lot.lot_calibration_ids.sorted(lambda x: x.date, reverse=True)
                if last_calibration:
                    last_calibration_date = last_calibration[0].date
                    if last_calibration_date:
                        last_calibration_date = datetime.strptime(last_calibration_date, DEFAULT_SERVER_DATE_FORMAT)
                        total_days = notify_expire + expire_calibration
                        final_date = last_calibration_date + timedelta(days=total_days)
                        if final_date.date() == datetime.now().date():
                            got_data = True

                            calibration = "<td>" + str(last_calibration_date) + "</td>" if last_calibration_date else ''
                            feedback = "<td>" + str(last_calibration[0].feedback) + "</td>" if last_calibration[
                                0].feedback else ''
                            followup_table += "<td>" + str(lot.product_id.display_name) + "</td>" + "<td>" + str(
                                lot.name) + "</td>" + calibration + feedback
        followup_table += '''</tr>
                                        </table>
                                        <center>'''
        if got_data:
            stock_group = self.env['ir.model.data'].xmlid_to_res_id(
                'stock.group_stock_manager')
            stock_users = self.get_users_from_group(stock_group)
            sale_group = self.env['ir.model.data'].xmlid_to_res_id(
                'sales_team.group_sale_manager')
            sale_users = self.get_users_from_group(sale_group)
            all_users = self.env['res.users'].sudo().browse(list(set(stock_users + sale_users)))
            for user in all_users:
                mail = self.env['mail.mail'].create({
                    'body_html': followup_table,
                    'subject': 'Devices Need Calibration',
                    'email_to': user.partner_id.email,
                    'partner_ids': [(4, user.partner_id.id)]
                })
                mail.send()
        return True


LotCalibration()
