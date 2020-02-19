# -*- coding: utf-8 -*-

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    revision_no = fields.Char(string='Revision Number', size=32, readonly=True,
                              states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    revision_count = fields.Integer(string='Revision Count')
    rev_line = fields.One2many('purchase.revision', 'order_id', string='Revisions')
    temp_name = fields.Char()
    _sql_constraints = [
        ('name_uniq', 'unique(revision_no, company_id)', 'Revision Number must be unique!'),
    ]

    @api.multi
    def action_confirm(self):
        res = super(PurchaseOrder, self).action_confirm()
        self.temp_name = self.name
        return res

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        res.temp_name = res.name
        return res

    @api.multi
    def create_revisions(self):
        rev_obj = self.env['purchase.revision']
        rev_line_obj = self.env['purchase.revision.line']
        purchase_id = self[0]
        if purchase_id.order_line:
            revision_count = purchase_id.revision_count + 1
            revision_no = str(purchase_id.temp_name) + '-' + str(revision_count)
            rev_id = rev_obj.create({
                'name': revision_no,
                'order_id': purchase_id.id
            })
        else:
            raise UserError(('There is no line item to revise.'))
        for line in purchase_id.order_line:
            vals = {
                'revision_id': rev_id.id,
                'name': line.name,
                'product_id': line.product_id.id,
                'price_unit': line.price_unit,
                'tax_id': [(6, 0, [x.id for x in line.taxes_id])],
                'product_uom_qty': line.product_qty,
                'date_planned': line.date_planned,
                'product_uom': line.product_uom.id
            }
            rev_line_obj.create(vals)
        self.write({'revision_no': revision_no, 'revision_count': revision_count,'name': revision_no})
        return True


PurchaseOrder()


class PurchaseRevision(models.Model):
    _name = 'purchase.revision'

    name = fields.Char('Revision No.', size=32, readonly=True)
    order_id = fields.Many2one('purchase.order', 'Order Reference')
    revision_line = fields.One2many('purchase.revision.line', 'revision_id', 'Revision Lines')
    state = fields.Selection('purchase.order', related='order_id.state', readonly=True)

    @api.multi
    def apply_revisions(self):
        ''' Create order lines against revision lines '''
        revision_id = self[0]
        purchase_line_obj = self.env['purchase.order.line']
        for l in revision_id.order_id.order_line:
            l.unlink()
        for x in revision_id.revision_line:
            vals = {
                'name': x.name,
                'product_id': x.product_id.id,
                'price_unit': x.price_unit,
                'tax_id': [(6, 0, [a.id for a in x.tax_id])],
                'product_qty': x.product_uom_qty,
                'state': 'draft',
                'date_planned': x.date_planned,
                'product_uom': x.product_uom.id,
                'order_id': x.revision_id.order_id.id,
            }
            purchase_line_obj.create(vals)
        self.env['purchase.order'].write({'revision_no': revision_id.name,'name': revision_id.name})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }


PurchaseRevision()


class PurchaseRevisionLine(models.Model):
    _name = 'purchase.revision.line'

    revision_id = fields.Many2one(comodel_name='purchase.revision', string='Revision Ref.', required=True,
                                  ondelete='cascade', readonly=True)
    name = fields.Text(string='Description', required=True, readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'),
                              readonly=True)
    date_planned = fields.Datetime(string='Date Planned', required=True, readonly=1)
    product_uom = fields.Many2one(comodel_name='product.uom', string='Unit of Measure', required=True, readonly=True)
    tax_id = fields.Many2many(comodel_name='account.tax', relation='purchase_revision_tax', column1='revision_line_id',
                              column2='tax_id', string='Taxes', readonly=True)

    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product UoS'), required=True,
                                   readonly=True)


PurchaseRevisionLine()
