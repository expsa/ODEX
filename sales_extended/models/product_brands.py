# -*- coding: utf-8 -*-
from odoo import fields,api,models
from odoo.exceptions import Warning
from odoo.tools.translate import _


class CostTypes(models.Model):
    _name = 'landed.cost.type'
    _rec_name = 'name'
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)


class Rates(models.Model):
    _name = 'res.rates'
    _rec_name = 'currency_id'
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To', required=True)
    rate = fields.Float(string='Rate', default=1.0)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True)

    @api.multi
    @api.constrains('rate')
    def rate_constraint(self):
        for item in self:
            if item.rate <= 0:
                raise Warning(_('Rate cannot be  0 or less.'))


class ProductBrands(models.Model):
    _name = 'product.brand'
    _rec_name = 'name'
    _description = 'Product Brands'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', domain=[('supplier', '=', True)],
                                 required=True)
    discount = fields.Float(string='Discount %')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True)
    name = fields.Char(string='Brand Name', required=True)
    line_ids = fields.One2many(comodel_name='product.brand.lines', inverse_name='brand_id', string='Categories')
    margin_ids = fields.One2many(comodel_name='product.brand.margin.lines', inverse_name='brand_id', string='Margins')


class ProductBrandLines(models.Model):
    _name = 'product.brand.lines'

    brand_id = fields.Many2one(comodel_name='product.brand', string='Brand')
    category_id = fields.Many2one(comodel_name='product.product', string='Cost Type', required=True,
                                  domain=[('landed_cost_ok', '=', True)])

    cost_type_id = fields.Many2one(comodel_name='landed.cost.type', string='Category', required=True)
    is_percent = fields.Boolean()
    value = fields.Float(string='Value', default=1.0, required=True)
    percent_value = fields.Char(compute='is_percent_value')

    @api.one
    @api.depends('is_percent')
    def is_percent_value(self):
        for item in self:
            if item.is_percent:
                item.percent_value = '%'
            else:
                item.percent_value = ''

    @api.multi
    @api.constrains('value')
    def brand_calc_value(self):
        for item in self:
            if item.value <= 0:
                raise Warning(_('Value cannot be 0 or less'))


ProductBrandLines()


class ProductBrandMargins(models.Model):
    _name = 'product.brand.margin.lines'
    brand_id = fields.Many2one(comodel_name='product.brand', string='Brand')
    category_id = fields.Many2one(comodel_name='landed.cost.type', string='Category', required=True)
    margin = fields.Float(string='Margin%', default=1.0, required=True)

    @api.multi
    @api.constrains('margin')
    def brand_calc_margin(self):
        for item in self:
            if item.margin <= 0:
                raise Warning(_('Margin cannot be 0 or less'))


ProductBrandMargins()
