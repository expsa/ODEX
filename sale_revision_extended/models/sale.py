# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    revision_no = fields.Char(string='Revision Number', size=32, readonly=True,
                              states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    revision_count = fields.Integer(string='Revision Count')
    rev_line = fields.One2many(comodel_name='sale.revision', inverse_name='order_id', string='Revisions')
    temp_name = fields.Char()

    # _sql_constraints = [
    #     ('name_uniq', 'unique(revision_no, company_id)', 'Revision Number must be unique!'),
    # ]

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.temp_name = self.name
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.temp_name = res.name
        return res

    @api.multi
    def create_revisions(self):
        rev_obj = self.env['sale.revision']
        rev_line_obj = self.env['sale.revision.line']
        sale_id = self[0]
        if sale_id.order_line:
            revision_count = sale_id.revision_count + 1
            revision_no = str(sale_id.temp_name) + '-' + str(revision_count)
            # revision_no = revision_count
            rev_id = rev_obj.create({
                'name': revision_no,
                'order_id': sale_id.id
            })
        else:
            raise UserError(('There is no line item to revise.'))
        for line in sale_id.order_line:
            vals = {
                'revision_id': rev_id.id,
                'name': line.name,
                'product_id': line.product_id.id,
                'price_unit': line.price_unit,
                'tax_id': [(6, 0, [x.id for x in line.tax_id])],
                'product_uom_qty': line.product_uom_qty,
            }
            rev_line_obj.create(vals)
        self.write({'revision_no': revision_count, 'revision_count': revision_count, 'name': revision_no})
        for item in self.picking_ids:
            item.origin = revision_no
        return True


class SaleRevision(models.Model):
    _name = 'sale.revision'

    name = fields.Char('Revision No.', size=32, readonly=True)
    order_id = fields.Many2one('sale.order', 'Order Reference')
    revision_line = fields.One2many('sale.revision.line', 'revision_id', 'Revision Lines')
    state = fields.Selection('sale.order', related='order_id.state', readonly=True)

    @api.multi
    def apply_revisions(self):
        ''' Create order lines against revision lines '''
        revision_id = self[0]
        sale_line_obj = self.env['sale.order.line']
        for l in revision_id.order_id.order_line:
            l.unlink()
        for x in revision_id.revision_line:
            vals = {
                'name': x.name,
                'product_id': x.product_id.id,
                'price_unit': x.price_unit,
                'tax_id': [(6, 0, [a.id for a in x.tax_id])],
                'product_uom_qty': x.product_uom_qty,
                'state': 'draft',
                'order_id': x.revision_id.order_id.id,
            }
            sale_line_obj.create(vals)
        self.env['sale.order'].write({'revision_no': revision_id.name, 'name': revision_id.name})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }


class SaleRevisionLine(models.Model):
    _name = 'sale.revision.line'

    revision_id = fields.Many2one('sale.revision', string='Revision Ref.', required=True, ondelete='cascade',
                                  readonly=True)
    name = fields.Text(string='Description', required=True, readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'),
                              readonly=True)
    tax_id = fields.Many2many('account.tax', 'sale_revision_tax', 'revision_line_id', 'tax_id', string='Taxes',
                              readonly=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product UoS'), required=True,
                                   readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
