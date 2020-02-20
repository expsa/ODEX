# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import models, fields, api
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        inherit the name search to make only select normal analytic account
        in any view that don't use search for parent in the context
        """
        context = dict(self.env.context)
        siblings = context.get('siblings', False)
        if siblings:
            service_ids = self.env['requisition.request'].resolve_2many_commands(
                'lines_ids', siblings, ['service_id'])

            if service_ids:
                exist_service_ids = []
                for service_line in service_ids:
                    if service_line['service_id']:
                        if type(service_line['service_id']) == int:
                            exist_service_ids.append(
                                service_line['service_id'])
                        else:
                            exist_service_ids.append(
                                service_line['service_id'][0])

                if not args:
                    args = []

                domain = [('id', 'not in', exist_service_ids)]

                args = expression.AND([args, domain])

        return super(ProductProduct, self).name_search(name, args,
                                                       operator, limit)

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        return {
            'date_maturity': line.get('date_maturity', False),
            'partner_id': partner,
            'name': line['name'],
            'debit': line['price'] > 0 and line['price'],
            'credit': line['price'] < 0 and -line['price'],
            'account_id': line['account_id'],
            'analytic_line_ids': line.get('analytic_line_ids', []),
            'amount_currency': line['price'] > 0 and abs(line.get('amount_currency', False)) or -abs(line.get('amount_currency', False)),
            'currency_id': line.get('currency_id', False),
            'quantity': line.get('quantity', 1.00),
            'product_id': line.get('product_id', False),
            'service_id': line.get('service_id', False),
            'product_uom_id': line.get('uom_id', False),
            'analytic_account_id': line.get('account_analytic_id', False),
            'invoice_id': line.get('invoice_id', False),
            'tax_ids': line.get('tax_ids', False),
            'tax_line_id': line.get('tax_line_id', False),
            'analytic_tag_ids': line.get('analytic_tag_ids', False),
        }
