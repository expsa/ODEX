# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import models, fields, api
from odoo.osv import expression


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_debit_credit_balance(self):
        analytic_line_obj = self.env['account.analytic.line']
        domain = ['|', ('account_id', 'child_of', self.ids),
                  ('account_id', '=', self.ids)]
        if self._context.get('from_date', False):
            domain.append(('date', '>=', self._context['from_date']))
        if self._context.get('to_date', False):
            domain.append(('date', '<=', self._context['to_date']))

        credit_groups = analytic_line_obj.read_group(
            domain=domain + [('amount', '>=', 0.0)],
            fields=['account_id', 'amount'],
            groupby=['account_id']
        )
        data_credit = {l['account_id'][0]: l['amount'] for l in credit_groups}
        debit_groups = analytic_line_obj.read_group(
            domain=domain + [('amount', '<', 0.0)],
            fields=['account_id', 'amount'],
            groupby=['account_id']
        )
        data_debit = {l['account_id'][0]: l['amount'] for l in debit_groups}

        for account in self:
            childs = self.search(['|', ('id', 'child_of', [account.id]),
                                  ('id', '=', [account.id])])

            account.debit = sum([abs(data_debit.get(x.id, 0.0))
                                 for x in childs])
            account.credit = sum([data_credit.get(x.id, 0.0) for x in childs])
            account.balance = account.credit - account.debit

    type = fields.Selection(selection=[
        ('general', 'General'),
        ('detailed', 'Detailed')], default='general', string='Type',
        help='''the type of analytic account general for parents and Detailed
        for account we can use in other operations''')

    parent_id = fields.Many2one('account.analytic.account', string='Parent')

    @api.onchange('type')
    def _onchange_type(self):
        """
        reset the parent when the type is changed
        """
        for acc in self:
            acc.parent_id = False

    @api.model
    def hierarchical_chart_details(self):
        """
        get the information of chart of analytic accounts
        reutrn : a list of dictionaries that contains orgnized accounts
        and accounts
        """
        accounts = self.sudo().search([])
        accounts = accounts.read([])

        return ['code', 'name', 'partner_id', 'debit',
                'credit', 'balance'], accounts
