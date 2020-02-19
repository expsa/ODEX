from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class KsGlobalDiscountInvoice(models.Model):
    _inherit = "account.invoice"

    ks_global_discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                                               string='Universal Discount type', readonly=True,
                                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                               default='percent')
    ks_global_discount_rate = fields.Float('Universal Discount Rate', readonly=True, states={'draft': [('readonly', False)],
                                                                                   'sent': [('readonly', False)]})
    ks_amount_discount = fields.Monetary(string='Universal Discount', readonly=True, compute='_compute_amount',
                                         store=True, track_visibility='always')
    ks_enable_discount = fields.Boolean(compute='ks_verify_discount')
    ks_sales_discount_account = fields.Text(compute='ks_verify_discount')
    ks_purchase_discount_account = fields.Text(compute='ks_verify_discount')

    @api.multi
    @api.depends('name')
    def ks_verify_discount(self):
        for rec in self:
            rec.ks_enable_discount = rec.env['ir.config_parameter'].sudo().get_param('ks_enable_discount')
            rec.ks_sales_discount_account = rec.env['ir.config_parameter'].sudo().get_param('ks_sales_discount_account')
            rec.ks_purchase_discount_account = rec.env['ir.config_parameter'].sudo().get_param('ks_purchase_discount_account')

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'ks_global_discount_type',
                 'ks_global_discount_rate')
    def _compute_amount(self):
        for rec in self:
            res = super(KsGlobalDiscountInvoice, rec)._compute_amount()
            if not ('ks_global_tax_rate' in rec):
                rec.ks_calculate_discount()
            sign = rec.type in ['in_refund', 'out_refund'] and -1 or 1
            rec.amount_total_company_signed = rec.amount_total * sign
            rec.amount_total_signed = rec.amount_total * sign
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
            rec.amount_total = rec.amount_tax + rec.amount_untaxed - rec.ks_amount_discount

    @api.constrains('ks_global_discount_rate')
    def ks_check_discount_value(self):
        if self.ks_global_discount_type == "percent":
            if self.ks_global_discount_rate > 100 or self.ks_global_discount_rate < 0:
                raise ValidationError('You cannot enter percentage value greater than 100.')
        else:
            if self.ks_global_discount_rate < 0 or self.amount_untaxed < 0:
                raise ValidationError('You cannot enter discount amount greater than actual cost or lower than 0.')

    # @api.onchange('purchase_id')
    # def ks_get_purchase_order_discount(self):
    #     self.ks_global_discount_rate = self.purchase_id.ks_global_discount_rate
    #     self.ks_global_discount_type = self.purchase_id.ks_global_discount_type

    @api.model
    def invoice_line_move_line_get(self):
        ks_res = super(KsGlobalDiscountInvoice, self).invoice_line_move_line_get()
        if self.ks_amount_discount > 0:
            ks_name = "Universal Discount"
            if self.ks_global_discount_type == "percent":
                ks_name = ks_name + " (" + str(self.ks_global_discount_rate) + "%)"
            ks_name = ks_name + " for " + (self.origin if self.origin else ("Invoice No " + str(self.id)))

            if self.ks_sales_discount_account and (self.type == "out_invoice" or self.type == "out_refund"):
                dict = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': ks_name,
                    'price_unit': self.ks_amount_discount,
                    'quantity': 1,
                    'price': -self.ks_amount_discount,
                    'account_id': int(self.ks_sales_discount_account),
                    'invoice_id': self.id,
                }
                ks_res.append(dict)

            elif self.ks_purchase_discount_account and (self.type == "in_invoice" or self.type == "in_refund"):
                dict = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': ks_name,
                    'price_unit': self.ks_amount_discount,
                    'quantity': 1,
                    'price': -self.ks_amount_discount,
                    'account_id': int(self.ks_purchase_discount_account),

                    'invoice_id': self.id,
                }
                ks_res.append(dict)

        return ks_res

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        ks_res = super(KsGlobalDiscountInvoice, self)._prepare_refund(invoice, date_invoice=None, date=None,
                                                                      description=None, journal_id=None)
        ks_res['ks_global_discount_rate'] = self.ks_global_discount_rate
        ks_res['ks_global_discount_type'] = self.ks_global_discount_type
        return ks_res
