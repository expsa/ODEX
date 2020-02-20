# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import api, exceptions, fields, models, _
from odoo.exceptions import Warning, ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    res_model = fields.Char(
        'Related Document Model Name')
    res_id = fields.Integer('Related Document ID')

    restricted = fields.Boolean(string='Restricted', help='True if the order is restricted')

    @api.model
    def invoice_line_move_line_get(self):
        '''
        #cusomtization :
            add service_id to the created move line
        '''
        res = []
        for line in self.invoice_line_ids:
            if line.quantity == 0:
                continue
            tax_ids = []
            for tax in line.invoice_line_tax_ids:
                tax_ids.append((4, tax.id, None))
                for child in tax.children_tax_ids:
                    if child.type_tax_use != 'none':
                        tax_ids.append((4, child.id, None))
            analytic_tag_ids = [(4, analytic_tag.id, None)
                                for analytic_tag in line.analytic_tag_ids]

            move_line_dict = {
                'invl_id': line.id,
                'type': 'src',
                'name': line.name.split('\n')[0][:64],
                'price_unit': line.price_unit,
                'quantity': line.quantity,
                'price': line.price_subtotal,
                'account_id': line.account_id.id,
                'product_id': line.product_id.id,
                'service_id': line.service_id.id,
                'uom_id': line.uom_id.id,
                'account_analytic_id': line.account_analytic_id.id,
                'tax_ids': tax_ids,
                'invoice_id': self.id,
                'analytic_tag_ids': analytic_tag_ids,
                'restricted': self.restricted,
            }
            res.append(move_line_dict)
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    service_id = fields.Many2one('product.product', string='Service',
                                 ondelete='restrict', index=True)

    initiative_id = fields.Many2one(related='service_id.initiative_id',
                                    comodel_name='initiative',
                                    string='Initiative',
                                    store=True)


class AccountInvoiceTax(models.Model):
    _inherit = "account.invoice.tax"

    @api.onchange('tax_id')
    def _onchange_tax_id(self):
        if not self.tax_id:
            return
        if self.account_id:
            return
        taxes = self.tax_id.compute_all(
            self.invoice_id.amount_untaxed, self.invoice_id.currency_id,
            1, False, self.invoice_id.partner_id)['taxes']

        if not taxes:
            return
        tax = taxes[0]

        self.name = tax.get('name', False)
        self.amount = tax.get('amount', 0.0)
        self.base = tax.get('base', 0.0)

        self.account_id = tax.get('account_id', False)
