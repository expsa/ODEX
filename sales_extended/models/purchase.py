# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    order_dated = fields.Date(string='Order Dated')
    ref_no = fields.Char(string='Ref No.')
    shipping_to = fields.Char(string='Shipping to')
    legalization = fields.Char(string='Legalization')



PurchaseOrder()


class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    line_no = fields.Char(string='No.')
    name = fields.Html(string='Description', required=True)


PurchaseLine()
