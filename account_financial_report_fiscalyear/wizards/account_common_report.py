# Copyright 2009-2017 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountCommonReport(models.TransientModel):
    _inherit = 'account.common.report'

    date_period_type = fields.Selection(
        string='Date Period Type',
        selection=[('fiscalyear', 'Fiscal Year'),
                   ('fiscalyear_period', 'Fiscal Year Period'), ])

    fiscalyear_id = fields.Many2one('fiscalyears',
                                    string='Fiscal Year',
                                    help='''The fiscalyear
                                used for this report.''')

    period_id = fields.Many2one('fiscalyears.periods',
                                string='Period',
                                help='''The fiscalyear period
                                used for this report.''')

    @api.onchange('fiscalyear_id')
    def _onchange_fiscalyear_id(self):
        if self.fiscalyear_id:
            if self.date_period_type == 'fiscalyear':
                self.date_from = self.fiscalyear_id.start_date
                self.date_to = self.fiscalyear_id.end_date

    @api.onchange('period_id')
    def _onchange_period_id(self):
        if self.period_id:
            if self.date_period_type == 'fiscalyear_period':
                self.date_from = self.period_id.start_date
                self.date_to = self.period_id.end_date
