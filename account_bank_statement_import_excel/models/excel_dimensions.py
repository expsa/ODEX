# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExcelDimensions(models.Model):
    _name = 'excel.dimensions'
    _description = 'The Dimensions of the excel file used in bank statement import'

    name = fields.Char(string='Name')

    company_id = fields.Many2one(comodel_name='res.company', string='company')

    account_number_row = fields.Integer(string='account number row')
    account_number_col = fields.Integer(string='account number column')

    currency_row = fields.Integer(string='currency row')
    currency_col = fields.Integer(string='currency column')

    balance_start_row = fields.Integer(string='starting balance row')
    balance_start_col = fields.Integer(string='starting balance column')

    balance_end_row = fields.Integer(string='ending balance row')
    balance_end_col = fields.Integer(string='ending balance column')

    date_period_row = fields.Integer(string='date period row')
    date_period_col = fields.Integer(string='date period column')

    details_row = fields.Integer(string='details row')

    debit_col = fields.Integer(string='debit column')

    credit_col = fields.Integer(string='credit column')

    balance_col = fields.Integer(string='balance column')

    type_col = fields.Integer(string='type column')

    note_col = fields.Integer(string='note column')

    date_col = fields.Integer(string='date column')
