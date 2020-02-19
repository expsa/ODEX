from odoo import models, fields


class Bank(models.Model):
    _inherit = 'res.bank'

    iban = fields.Char(string='Iban')
    beneficiary = fields.Char(string='Beneficiary')
    warranty = fields.Char(string='Warranty')
    account_number = fields.Char(string='Account Number')


Bank()
