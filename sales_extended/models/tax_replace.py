# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    amount_tax = fields.Monetary(string='VAT', store=True, readonly=True, compute='_amount_all')


SaleOrder()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    tax_id = fields.Many2many(comodel_name='account.tax', string='VAT',
                              domain=['|', ('active', '=', False), ('active', '=', True)])


SaleOrderLine()


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    amount_tax = fields.Monetary(string='VAT', store=True, readonly=True, compute='_amount_all')


PurchaseOrder()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    taxes_id = fields.Many2many(comodel_name='account.tax', string='VAT',
                                domain=['|', ('active', '=', False), ('active', '=', True)])


PurchaseOrderLine()


class Invoice(models.Model):
    _inherit = 'account.invoice'
    amount_tax = fields.Monetary(string='VAT', store=True, readonly=True, compute='_amount_all')


Invoice()


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    invoice_line_tax_ids = fields.Many2many(comodel_name='account.tax',
                                            relation='account_invoice_line_tax', column1='invoice_line_id',
                                            column2='tax_id',
                                            string='VAT',
                                            domain=[('type_tax_use', '!=', 'none'), '|', ('active', '=', False),
                                                    ('active', '=', True)], oldname='invoice_line_tax_id')


InvoiceLine()
