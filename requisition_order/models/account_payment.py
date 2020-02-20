# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict
from odoo.addons.account.models import account_payment as payment_standard


class account_payment(models.Model):
    _inherit = "account.payment"

    custody_id = fields.Many2one(
        comodel_name='product.product', string='Custody',
        copy=False,
        domain=[('type', '=', 'service'),
                ('nature', '=', 'custody')],
        help='used for custody purpose')

    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id', 'custody_id')
    def _compute_destination_account_id(self):
        if self.invoice_ids:
            self.destination_account_id = self.invoice_ids[0].account_id.id
        elif self.custody_id:
            self.destination_account_id = self.custody_id.property_account_expense_id.id
        elif self.payment_type == 'transfer':
            if not self.company_id.transfer_account_id.id:
                raise UserError(_('Transfer account not defined on the company.'))
            self.destination_account_id = self.company_id.transfer_account_id.id
        elif self.partner_id:
            if self.partner_type == 'customer':
                self.destination_account_id = self.partner_id.property_account_receivable_id.id
            else:
                self.destination_account_id = self.partner_id.property_account_payable_id.id
        elif self.partner_type == 'customer':
            default_account = self.env['ir.property'].get(
                'property_account_receivable_id', 'res.partner')
            self.destination_account_id = default_account.id
        elif self.partner_type == 'supplier':
            default_account = self.env['ir.property'].get(
                'property_account_payable_id', 'res.partner')
            self.destination_account_id = default_account.id

    @api.model
    def resolve_2many_commands_on_model(self, comodel_name, commands, fields=None):
        """
            # need it here cause i don not want to create reference to requisition
        """
        result = []                     # result (list of dict)
        record_ids = []                 # ids of records to read
        updates = defaultdict(dict)     # {id: vals} of updates on records

        for command in commands or []:
            if not isinstance(command, (list, tuple)):
                record_ids.append(command)
            elif command[0] == 0:
                result.append(command[2])
            elif command[0] == 1:
                record_ids.append(command[1])
                updates[command[1]].update(command[2])
            elif command[0] in (2, 3):
                record_ids = [id for id in record_ids if id != command[1]]
            elif command[0] == 4:
                record_ids.append(command[1])
            elif command[0] == 5:
                result, record_ids = [], []
            elif command[0] == 6:
                result, record_ids = [], list(command[2])

        # read the records and apply the updates
        records = self.env[comodel_name].browse(record_ids)
        for data in records.read(fields):
            data.update(updates.get(data['id'], {}))
            result.append(data)

        return result

    @api.model
    def default_get(self, fields):
        rec = super(account_payment, self).default_get(fields)
        requisition_defaults = self.resolve_2many_commands_on_model(
            'requisition.request', self._context.get('requisition_request_ids'))
        if requisition_defaults and len(requisition_defaults) == 1:
            requisition = requisition_defaults[0]
            rec['communication'] = requisition['name']
            rec['name'] = requisition['name']
            rec['currency_id'] = requisition['currency_id'][0]
            rec['custody_id'] = requisition['custody_id'][0]
            rec['payment_type'] = 'outbound'
            # rec['partner_type'] = MAP_requisition_TYPE_PARTNER_TYPE[requisition['type']]
            rec['partner_id'] = requisition['beneficiary_id'][0]
            rec['amount'] = requisition['custody_amount']

        return rec

    @api.multi
    def action_custody_payment(self):
        requisition_defaults = self.resolve_2many_commands_on_model(
            'requisition.request', self._context.get('requisition_request_ids'))

        if requisition_defaults and len(requisition_defaults) == 1:
            self.env['requisition.request'].browse(
                [x['id'] for x in requisition_defaults]).write(
                {'payment_id': self.id, 'state': 'running'})
