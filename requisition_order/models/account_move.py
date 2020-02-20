# -*- coding: utf-8 -*-

import time
from collections import OrderedDict
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools.misc import formatLang, format_date
from odoo.tools import float_is_zero, float_compare
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp
from lxml import etree


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    service_id = fields.Many2one('product.product', string='Service')
    initiative_id = fields.Many2one(related='service_id.initiative_id',
                                    comodel_name='initiative',
                                    string='Initiative',
                                    store=True)

    restricted = fields.Boolean(string='Restricted', help='True if the order is restricted')

    @api.one
    def _prepare_analytic_line(self):
        """ Prepare the values used to create() an account.analytic.line upon validation of an account.move.line having
            an analytic account. This method is intended to be extended in other modules.
            #cusomtization :
            add service_id to the created move line
        """
        amount = (self.credit or 0.0) - (self.debit or 0.0)
        default_name = self.name or(self.ref or '/' + ' -- ' +
                                    (self.partner_id and self.partner_id.name or '/'))
        return {
            'name': default_name,
            'date': self.date,
            'account_id': self.analytic_account_id.id,
            'tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'unit_amount': self.quantity,
            'product_id': self.product_id and self.product_id.id or False,
            'service_id': self.service_id and self.service_id.id or False,
            'product_uom_id': self.product_uom_id and self.product_uom_id.id or False,
            'amount': self.company_currency_id.with_context(date=self.date or fields.Date.context_today(self)).compute(amount, self.analytic_account_id.currency_id) if self.analytic_account_id.currency_id else amount,
            'general_account_id': self.account_id.id,
            'ref': self.ref,
            'move_id': self.id,
            'user_id': self.invoice_id.user_id.id or self._uid,
            'restricted': self.restricted,
        }
