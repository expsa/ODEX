# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

class TransportMethodWizard(models.TransientModel):
    _name = 'exchange.wizard'
    
    exchange_id = fields.Many2one('exchange.request')
    name = fields.Char(related="exchange_id.name")
    line_ids = fields.Many2many('exchange.wizard.line','wizard_id')

    @api.multi
    def print_report(self):
        """
            create pickgin 
        """
        source = False
        dest = False
        move_lines = []
        if self.exchange_id.stock_journal_id.location_id.id == False:
            raise ValidationError(_("Please Select a location in your stock journal first"))
        if self.exchange_id.requisition_type == 'exchange':
            source = self.exchange_id.location_id.id
            dest = self.exchange_id.stock_journal_id.location_id.id
        else:
            source = self.exchange_id.stock_journal_id.location_id.id
            dest = self.exchange_id.location_id.id
        for rec in self.line_ids:
            result = rec.picking_done + rec.picking_quantity
            quant = rec.product_qty
            if result > quant:
                raise ValidationError(_("Pickgin Quantity Can't be more than Asked Quantity"))
            if rec.product_id.type != 'service':
                move_lines.append((0,0,{
                    'name':rec.product_id.name,
                    'product_id':rec.product_id.id,
                    'product_uom_qty':rec.picking_quantity,
                    'product_uom':rec.Uom_id.id,
                    'location_dest_id':dest,
                }))
        if len(move_lines)!=0:
            stock_picking = self.env['stock.picking'].create({
                'name':'mosabtest',
                'date':self.exchange_id.request_date,
                'partner_id':self.exchange_id.user_id.partner_id.id,
                'origin':self.exchange_id.name,
                'department_id':self.exchange_id.department_id.id,
                'category_id':self.exchange_id.category_id.id,
                'picking_type_id':self.exchange_id.picking_type_id.id,
                'location_dest_id':dest,
                'location_id':source,
                'state':'assigned',
                'move_lines':move_lines,
            })
            for rec in stock_picking.move_lines:
                rec._set_quantity_done(rec.product_qty)
            self.exchange_id.write({'stock_picking':[(4,stock_picking.id)]})
            state = True
            for rec in self.line_ids:
                result = rec.picking_done + rec.picking_quantity
                quant = rec.product_qty
                if result != quant:
                    state = False
            if state == True:
                self.exchange_id.write({'state':'done'})
        return True


class TransportMethodWizard(models.TransientModel):
    _name = 'purchase.wizard'
    
    exchange_id = fields.Many2one('exchange.request')
    name = fields.Char(related="exchange_id.name")
    line_ids = fields.Many2many('exchange.wizard.line','purchase_wizard_id')

    @api.multi
    def print_report(self):
        """
            create pickgin 
        """
        picktype = False
        if self.exchange_id.type != 'service':
            if self.exchange_id.requisition_type == 'exchange':
                picktype = self.env['stock.picking.type'].search([('warehouse_id','=',self.exchange_id.warehouse_id.id),('code','=','incoming')])[0].id
            if self.exchange_id.requisition_type == 'return':
                picktype = self.env['stock.picking.type'].search([('warehouse_id','=',self.warehouse_id.exchange_id.id),('code','=','outgoing')])[0].id
        if len(self.exchange_id.requisition_id) !=0:
            if self.exchange_id.requisition_id.state != 'cancel':
                raise ValidationError(_("This Request already have Purchase Reuisition"))
        else:
            move_lines = []
            for rec in self.line_ids:
                move_lines.append((0,0,{
                    'product_id':rec.product_id.id,
                    'product_qty':rec.product_qty,
                    'name':rec.note,
                }))
            if self.exchange_id.type == 'service':
                picktype = 1
            purchase_requisition = self.env['purchase.requisition'].create({
                # 'name':self.name,
                # 'exchange_date':self.exchange_id.request_date,
                'priority':self.exchange_id.priority,
                'category_id':self.exchange_id.category_id.id,
                'department_id':self.exchange_id.department_id.id,
                'purpose':self.exchange_id.purpose,
                'origin':self.exchange_id.name,
                'stock_journal_id':self.exchange_id.stock_journal_id.id,
                'picking_type_id':picktype,
                'state':'draft',
                'exchange_request':self.exchange_id.id,
                'line_ids':move_lines,
                'vendor_ids': [(4, vendor.id, None) for vendor in self.exchange_id.vendor_ids],
                'justification':self.exchange_id.justification,
            })
            self.exchange_id.requisition_id = purchase_requisition
            self.exchange_id.write({'state':'waiting'})


class Exchangelines(models.TransientModel):
    _name = 'exchange.wizard.line'

    wizard_id = fields.Many2one('exchange.wizard' )
    purchase_wizard_id = fields.Many2one('purchase.wizard' )
    requ_name = fields.Char(related="wizard_id.name", store=True)
    purchase_requ_name = fields.Char(related="purchase_wizard_id.name", store=True)
    product_id = fields.Many2one('product.product')
    name = fields.Char(related='product_id.name')
    product_qty = fields.Integer()
    Uom_id = fields.Many2one(related='product_id.uom_id')
    note = fields.Char()
    qty_available = fields.Float()
    picking_quantity = fields.Integer()
    picking_done = fields.Integer()