# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    res_model = fields.Char(
        'Related Document Model Name')

    res_id = fields.Integer('Related Document ID')

    restricted = fields.Boolean(string='Restricted', help='True if the order is restricted')

    @api.multi
    @api.depends('name', 'number')
    def name_get(self):
        return [(r.id,
                 (
                     (r.number and (r.number + ' ') or '') + (r.name or '') or _('Voucher'))
                 ) for r in self]

    @api.multi
    def voucher_move_line_create(self, line_total, move_id, company_currency, current_currency):
        '''
        Create one account move line, on the given account move, per voucher line where amount is not 0.0.
        It returns Tuple with tot_line what is total of difference between debit and credit and
        a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

        :param voucher_id: Voucher id what we are working with
        :param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
        :param move_id: Account move wher those lines will be joined.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
        :rtype: tuple(float, list of int)
        '''
        tax_calculation_rounding_method = self.env.user.company_id.tax_calculation_rounding_method
        tax_lines_vals = []
        for line in self.line_ids:
            # create one move line per voucher line where amount is not 0.0
            if not line.price_subtotal:
                continue
            line_subtotal = line.price_subtotal
            if self.voucher_type == 'sale':
                line_subtotal = -1 * line.price_subtotal
            # convert the amount set on the voucher line into the currency of the voucher's company
            # this calls res_curreny.compute() with the right context,
            # so that it will take either the rate on the voucher if it is relevant or will use the default behaviour
            amount = self._convert_amount(line.price_unit*line.quantity)
            move_line = {
                'journal_id': self.journal_id.id,
                'name': line.name or '/',
                'account_id': line.account_id.id,
                'service_id': line.service_id and line.service_id.id or False,
                'move_id': move_id,
                'partner_id': self.partner_id.commercial_partner_id.id,
                'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                'quantity': 1,
                'credit': abs(amount) if self.voucher_type == 'sale' else 0.0,
                'debit': abs(amount) if self.voucher_type == 'purchase' else 0.0,
                'date': self.account_date,
                'tax_ids': [(4, t.id) for t in line.tax_ids],
                'amount_currency': line_subtotal if current_currency != company_currency else 0.0,
                'currency_id': company_currency != current_currency and current_currency or False,
                'payment_id': self._context.get('payment_id'),
                'restricted': self.restricted,
            }
            # When global rounding is activated, we must wait until all tax lines are computed to
            # merge them.
            if tax_calculation_rounding_method == 'round_globally':
                self.env['account.move.line'].create(move_line)
                tax_lines_vals += self.env['account.move.line'].with_context(round=False)._apply_taxes(
                    move_line, move_line.get('debit', 0.0) - move_line.get('credit', 0.0))
            else:
                self.env['account.move.line'].with_context(apply_taxes=True).create(move_line)

        # When round globally is set, we merge the tax lines
        if tax_calculation_rounding_method == 'round_globally':
            tax_lines_vals_merged = {}
            for tax_line_vals in tax_lines_vals:
                key = (
                    tax_line_vals['tax_line_id'],
                    tax_line_vals['account_id'],
                    tax_line_vals['analytic_account_id'],
                )
                if key not in tax_lines_vals_merged:
                    tax_lines_vals_merged[key] = tax_line_vals
                else:
                    tax_lines_vals_merged[key]['debit'] += tax_line_vals['debit']
                    tax_lines_vals_merged[key]['credit'] += tax_line_vals['credit']
            currency = self.env['res.currency'].browse(company_currency)
            for vals in tax_lines_vals_merged.values():
                vals['debit'] = currency.round(vals['debit'])
                vals['credit'] = currency.round(vals['credit'])
                self.env['account.move.line'].create(vals)
        return line_total


class AccountVoucherLine(models.Model):
    _inherit = 'account.voucher.line'

    service_id = fields.Many2one('product.product', string='Service',
                                 ondelete='restrict', index=True)

    initiative_id = fields.Many2one(related='service_id.initiative_id',
                                    comodel_name='initiative',
                                    string='Initiative',
                                    ondelete='restrict',
                                    store=True)
