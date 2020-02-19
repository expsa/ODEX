# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError 

class ContractCustom(models.Model):
    _inherit = 'contract.contract'

    type_of_contraction = fields.Selection([('subs' , 'Subscription') , ('contract' , 'Contract')])
    installment_ids = fields.One2many('line.contract.installment' , 'contract_id' , 'Installments')


class ContractInstallmentLine(models.Model):
    _name = 'line.contract.installment'

    contract_id = fields.Many2one('contract.contract')
    amount = fields.Float('Amount')
    name = fields.Char('Name' , required=True)
    due_date = fields.Date('Due Date')
    paid_amount = fields.Float('Paied Amount')
    paied_date = fields.Date('Paied Date')
    state = fields.Selection([('draft' , 'Draft') , ('paied' , 'Paied')],string="Status")

    @api.constrains('amount','paid_amount')
    def amount_validation(self):
        if self.amount <= 0:
            raise ValidationError(_('Sorry amount Must be greater than Zero'))
        if self.paid_amount < 0:
            raise ValidationError(_('Sorry amount must not be negative value'))