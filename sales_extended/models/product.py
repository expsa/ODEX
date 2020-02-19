# -*- coding: utf-8 -*-
import odoo.addons.decimal_precision as dp
import time
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _


class ProductAccessories(models.Model):
    _name = 'product.accessory.line'
    _rec_name = 'product_tmpl_id'

    product_tmpl_id = fields.Many2one(comodel_name='product.template')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    qty = fields.Float(string='Qty', default=0.0)

    @api.multi
    @api.constrains('qty')
    def qty_constraint(self):
        for item in self:
            if item.qty <= 0:
                raise Warning(_('Qty cannot be 0 or less.'))


ProductAccessories()


class ProductCostLine(models.Model):
    _name = 'product.cost.lines'
    _rec_name = 'cost_id'
    product_id = fields.Many2one(comodel_name='product.template')
    cost_id = fields.Many2one(comodel_name='landed.cost.type', string='Category')
    category_id = fields.Many2one(comodel_name='product.product', string='Cost Type', required=True,
                                  domain=[('landed_cost_ok', '=', True)])
    item_type = fields.Selection([('percent', 'Percent'), ('value', 'Value')], string='Type')
    value = fields.Float(string='Value')
    total = fields.Float(string='Total Line')


ProductCostLine()


class ProductMarginLine(models.Model):
    _name = 'product.margin.lines'
    _rec_name = 'product_id'
    _order = 'category_id'
    product_id = fields.Many2one(comodel_name='product.template')
    category_id = fields.Many2one(comodel_name='landed.cost.type', string='Category', required=True)
    margin = fields.Float(string='Margin%', default=1.0, required=True)


ProductMarginLine()


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    type = fields.Selection(default='product')
    arabic_name = fields.Char('Arabic Name')
    arabic_desc = fields.Html()

    @api.one
    def _get_last_purchase(self):
        for item in self:
            current_date = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
            for price_list in item.seller_ids:
                if price_list.date_start and price_list.date_end:
                    if item.brand_id.partner_id.id == price_list.name.id and current_date >= price_list.date_start and current_date <= price_list.date_end:
                        item.last_purchase_price = price_list.price

    @api.one
    @api.depends('last_purchase_price', 'currency_id', 'brand_id')
    def _get_last_purchase_rate(self):
        for item in self:
            date = datetime.now().date()
            current_rate = self.env['res.rates'].sudo().search([('date_from', '<=', date),
                                                                ('date_to', '>=', date),
                                                                ('currency_id', '=', item.currency_id.id)], limit=1)
            if current_rate:
                item.purchase_price_rate = (item.last_purchase_price - (
                        (item.brand_id.discount * item.last_purchase_price) / 100)) * current_rate.rate
            else:
                item.purchase_price_rate = (
                        item.last_purchase_price - ((item.brand_id.discount * item.last_purchase_price) / 100))

    last_purchase_price = fields.Float(string='Purchase Price', compute='_get_last_purchase')
    purchase_price_rate = fields.Float(string='Purchase Price With Rate', compute='_get_last_purchase_rate')
    product_accessory_ids = fields.One2many(comodel_name='product.accessory.line', inverse_name='product_tmpl_id',
                                            string='Product Sale Accessories')
    default_code = fields.Char(
        'Article No.', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
    cost_line_ids = fields.One2many(comodel_name='product.cost.lines', inverse_name='product_id',
                                    compute='_get_cost_types')
    list_price = fields.Float(string='Sales Price', default=1.0,
                              digits=dp.get_precision('Product Price'), compute='_get_brand_sale_price',
                              help="Base price to compute the customer price. Sometimes called the catalog price.")
    is_use_store = fields.Boolean(compute='_get_user_store_price')
    list_price_store = fields.Float(string='Sales Price', default=1.0, digits=dp.get_precision('Product Price'),
                                    help="Base price to compute the customer price. Sometimes called the catalog price.")
    brand_id = fields.Many2one(comodel_name='product.brand', string='Brand')
    brand_categ_id = fields.Many2one(comodel_name='landed.cost.type', string='Category', domain=[('id', 'in', [])])
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', related='brand_id.currency_id')
    warranty_months = fields.Integer(string='Warranty Months')
    warranty_partner_id = fields.Many2one(comodel_name='res.partner', domain=[('supplier', '=', True)],
                                          string='Warranty Provider')
    margin_line_ids = fields.One2many(comodel_name='product.margin.lines', inverse_name='product_id',
                                      string='Margin Lines', compute='_get_cost_types')

    @api.one
    @api.depends('brand_id', 'brand_categ_id', 'last_purchase_price')
    def _get_cost_types(self):
        for item in self:
            if item.brand_categ_id and item.brand_id:
                lines = self.env['product.brand.lines'].search([('brand_id', '=', item.brand_id.id),
                                                                ('cost_type_id', '=', item.brand_categ_id.id)])
                margins = self.env['product.brand.margin.lines'].search([('brand_id', '=', item.brand_id.id),
                                                                         ('category_id', '=', item.brand_categ_id.id)])
                purchase_late_price = item.purchase_price_rate

                def get_total_cost(line, last_purchase_price):
                    if line.is_percent:
                        return last_purchase_price * (line.value / 100)
                    else:
                        return line.value

                for line in margins:
                    item.margin_line_ids |= self.env['product.margin.lines'].create({'product_id': item.id,
                                                                                     'margin': line.margin,
                                                                                     'category_id': line.category_id.id})
                for record in lines:
                    item.cost_line_ids |= self.env['product.cost.lines'].create({'product_id': item.id,
                                                                                 'cost_id': record.cost_type_id.id,
                                                                                 'category_id': record.category_id.id,
                                                                                 'item_type': 'percent' if record.is_percent else 'value',
                                                                                 'value': record.value,
                                                                                 'total': get_total_cost(record,
                                                                                                         purchase_late_price)})

    @api.one
    def _get_user_store_price(self):
        for item in self:
            if not item.brand_id or not item.brand_categ_id:
                item.is_use_store = True
            else:
                item.is_use_store = False

    @api.one
    @api.depends('brand_id', 'brand_categ_id', 'last_purchase_price', 'purchase_price_rate', 'list_price_store',
                 'is_use_store', 'currency_id')
    def _get_brand_sale_price(self):
        for item in self:
            if not item.is_use_store:
                def get_total_cost(line, last_purchase_price):
                    if line.is_percent:
                        return last_purchase_price * (line.value / 100)
                    else:
                        return line.value

                lines = self.env['product.brand.lines'].search([('brand_id', '=', item.brand_id.id),
                                                                ('cost_type_id', '=', item.brand_categ_id.id)])
                margins = self.env['product.brand.margin.lines'].search([('brand_id', '=', item.brand_id.id),
                                                                         ('category_id', '=', item.brand_categ_id.id)])
                purchase_late_price = item.purchase_price_rate
                total = sum(get_total_cost(line, purchase_late_price) for line in lines) + purchase_late_price
                gross = sum(record.margin / 100 * total for record in margins) + total
                item.list_price = gross
            else:
                item.list_price = item.list_price_store

    @api.multi
    @api.onchange('brand_id')
    def onchange_product_brand_id(self):
        for item in self:
            if item.brand_id:
                item.brand_categ_id = False
                categ_ids = [record.cost_type_id.id for record in item.brand_id.line_ids]
                return {'domain': {'brand_categ_id': [('id', 'in', categ_ids)]}}
            else:
                return {'domain': {'brand_categ_id': [('id', 'in', [])]}}


ProductTemplate()


class Product(models.Model):
    _inherit = 'product.product'
    default_code = fields.Char('Article No', index=True)
    # description_sale = fields.Html(string="Sale Description" , translate=True , related="product_tmpl_id.description_sale")


    @api.multi
    @api.constrains('default_code')
    def _check_default_code(self):
        for product in self:
            domain = [
                ('id', '!=', product.id),
                ('default_code', '=', product.default_code),
                ('default_code', '!=', False)]
            other_products = self.search(domain)
            if other_products:
                raise ValidationError(
                    _("This Article Number is already set to Product '%s'") % other_products[0].name)

    @api.one
    def _get_last_purchase(self):
        pricelist = self.env['product.pricelist.item'].search(
            [('date_start', '<=', time.strftime(DEFAULT_SERVER_DATE_FORMAT)),
             ('date_end', '>=', time.strftime(DEFAULT_SERVER_DATE_FORMAT)), ], limit=1)
        if self.product_variant_ids:
            product_id = self.product_variant_ids[0]
            if pricelist:
                self.last_purchase_price = pricelist.pricelist_id.price_get(product_id.id, 1).get(
                    pricelist.pricelist_id.id, 0.0)
            else:
                self.last_purchase_price = 0
        else:
            self.last_purchase_price = 0

    @api.one
    @api.depends('last_purchase_price', 'currency_id', 'brand_id')
    def _get_last_purchase_rate(self):
        for item in self:
            date = datetime.now().date()
            current_rate = self.env['res.rates'].sudo().search([('date_from', '<=', date),
                                                                ('date_to', '>=', date),
                                                                ('currency_id', '=', item.currency_id.id)], limit=1)
            if current_rate:
                item.purchase_price_rate = (item.last_purchase_price - (
                        (item.brand_id.discount * item.last_purchase_price) / 100)) * current_rate.rate
            else:
                item.purchase_price_rate = (
                        item.last_purchase_price - ((item.brand_id.discount * item.last_purchase_price) / 100))

    last_purchase_price = fields.Float(string='Purchase Price', compute='_get_last_purchase')
    purchase_price_rate = fields.Float(string='Purchase Price With Rate', compute='_get_last_purchase_rate')


Product()
