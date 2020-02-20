# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_account_fiscalyears = fields.Boolean(
        string='Fiscal Years Management')

    module_account_chart_of_accounts = fields.Boolean(
        string='Hierarchy Chart Of Accounts')

    anglo_saxon_accounting = fields.Boolean(
        related='company_id.anglo_saxon_accounting',
        string="Use anglo-saxon accounting")

    module_analytic_account = fields.Boolean(
        string='Extended Analytic Accounts')

    expense_journal_id = fields.Many2one(
        related='company_id.default_expense_journal_id',
        comodel_name='account.journal', string='Expense Journal')

    custody_journal_id = fields.Many2one(
        related='company_id.default_custody_journal_id',
        comodel_name='account.journal', string='Custody Journal')

    income_journal_id = fields.Many2one(
        related='company_id.default_income_journal_id',
        comodel_name='account.journal', string='Income Journal')


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_expense_journal_id = fields.Many2one(
        'account.journal', 'Expense Journal')

    default_custody_journal_id = fields.Many2one(
        'account.journal', 'Custody Journal')

    default_income_journal_id = fields.Many2one(
        'account.journal', 'Income Journal')
