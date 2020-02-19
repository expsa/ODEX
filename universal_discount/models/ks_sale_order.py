# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class KsGlobalDiscountSales(models.Model):
    _inherit = "sale.order"

    ks_global_discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                                               string='Universal Discount type', readonly=True,
                                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                               default='percent')
    ks_global_discount_rate = fields.Float('Universal Discount Rate', readonly=True, states={'draft': [('readonly', False)],
                                                                                   'sent': [('readonly', False)]})
    ks_amount_discount = fields.Monetary(string='Universal Discount', readonly=True, compute='_amount_all',
                                         track_visibility='always', store=True)
    ks_enable_discount = fields.Boolean(compute='ks_verify_discount')

    @api.depends('name')
    def ks_verify_discount(self):
        for item in self:
            item.ks_enable_discount = self.env['ir.config_parameter'].sudo().get_param('ks_enable_discount')

    @api.depends('order_line.price_total', 'ks_global_discount_rate', 'ks_global_discount_type')
    def _amount_all(self):
        for rec in self:
            res = super(KsGlobalDiscountSales, rec)._amount_all()
            if not ('ks_global_tax_rate' in rec):
                rec.ks_calculate_discount()
        return res

    @api.multi
    def _prepare_invoice(self):
        for rec in self:
            res = super(KsGlobalDiscountSales, rec)._prepare_invoice()
            res['ks_global_discount_rate'] = rec.ks_global_discount_rate
            res['ks_global_discount_type'] = rec.ks_global_discount_type
        return res

    @api.multi
    def ks_calculate_discount(self):
        for rec in self:
            if rec.ks_global_discount_type == "amount":
                rec.ks_amount_discount = rec.ks_global_discount_rate if rec.amount_untaxed > 0 else 0

            elif rec.ks_global_discount_type == "percent":
                if rec.ks_global_discount_rate != 0.0:
                    rec.ks_amount_discount = (rec.amount_untaxed + rec.amount_tax) * rec.ks_global_discount_rate / 100
                else:
                    rec.ks_amount_discount = 0
            rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.ks_amount_discount

    @api.constrains('ks_global_discount_rate')
    def ks_check_discount_value(self):
        if self.ks_global_discount_type == "percent":
            if self.ks_global_discount_rate > 100 or self.ks_global_discount_rate < 0:
                raise ValidationError('You cannot enter percentage value greater than 100.')
        else:
            if self.ks_global_discount_rate < 0 or self.ks_global_discount_rate > self.amount_untaxed:
                raise ValidationError('You cannot enter discount amount greater than actual cost or lower than 0.')
