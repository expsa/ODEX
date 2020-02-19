# -*- coding: utf-8 -*-
import time
import datetime
import math
from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from datetime import datetime, timedelta, date

class PurchaseContract(models.Model):
    _name = 'purchase.contract'

    name = fields.Char(required=True)
    note = fields.Text()
    type = fields.Selection([
        ('supplier','Supplier'),
        ('customer','Customer')
    ])
    contract_type = fields.Selection([
        ('nda','NDA'),
        ('agreement','Agreement'),
        ('contract','Contract'),
        ('mou','MOU'),
        ('license','License')
    ])
    purchase_id = fields.Many2one('purchase.order')
    partner_id = fields.Many2one('res.partner')
    start_date = fields.Date(default=datetime.now())
    end_date = fields.Date()
    amount = fields.Float()
    remain = fields.Float(compute='ComputeRemain')
    paid = fields.Float()
    remaining_days = fields.Integer(compute="ComputeRemainingDays")
    line_ids = fields.One2many('purchase.contract.line','contract_id')
    first_company = fields.Many2one('res.company')
    second_company = fields.Many2one('res.partner',related="partner_id")
    first_terms = fields.Text()
    second_terms = fields.Text()
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirmed'),
        ('done','Done'),
        ('cancel','Cancel')
    ],default='draft')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id.id)
    # nda = fields.Boolean(default=False)
    attachment_id = fields.Binary()
    department_id = fields.Many2one('hr.department')

    @api.depends('start_date','end_date')
    def ComputeRemainingDays(self):
        """
            compute remaining days
        """
        fmt = '%Y-%m-%d'
        if self.start_date and self.end_date:
            d1 = datetime.strptime(self.start_date, fmt)
            d2 = datetime.strptime(self.end_date, fmt)
            daysDiff = str((d2-d1).days)
            self.remaining_days = daysDiff
            self.write({'remaining_days':daysDiff})

    @api.constrains('start_date','end_date')
    def ConstraintOnDate(self):
        """
            make sure start date before end date
        """
        if self.start_date > self.end_date:
            raise ValidationError(_("Start Date Can't be After End Date"))

    @api.multi
    def action_confirm(self):
        """
            move document to confirm state
        """
        self.write({'state':'confirm'})

    @api.multi
    def action_done(self):
        """
            move document to done state
        """
        if self.paid == self.amount and self.remain == 0 :
            self.write({'state':'done'})
        else:
            raise ValidationError(_("You can't change the state to done while there's remaining amount"))
    
    @api.multi
    def action_set_to_draft(self):
        """
            move document to draft state
        """
        self.write({'state':'draft'})

    @api.multi
    def action_cancel(self):
        """
            move document to cancel state
        """
        self.write({'state':'cancel'})
    

    @api.multi
    @api.depends('paid','amount')
    def ComputeRemain(self):
        """
            Compute the remain value
        """
        for rec in self:
            rec.remain = rec.amount - rec.paid

    @api.onchange('type')
    def PartnerDomain(self):
        """
            Domaining the Partner using the type
        """
        if self.type == 'supplier':
            return {'domain':{'partner_id':[('supplier','=',True)]}}
        if self.type == 'customer':
            return {'domain':{'partner_id':[('customer','=',True)]}}


class PurchaseContractLine(models.Model):
    _name = 'purchase.contract.line'

    date_of_pay = fields.Date(default=datetime.now())
    note = fields.Char()
    amount = fields.Float()
    contract_id = fields.Many2one('purchase.contract')
    state = fields.Selection([
        ('draft','Draft'),
        ('paid','paid')
    ],default='draft')

    @api.multi
    def unlink(self):
        """
            prevent deleting a paid line
        """
        for rec in self:
            if rec.state == 'paid':
                raise ValidationError(_("You can't Delete a paid line"))

    @api.multi
    def action_paid(self):
        """
            change document state to paid
        """
        for rec in self:
            result = rec.amount + rec.contract_id.paid
            if result > rec.contract_id.amount:
                raise ValidationError(_("Paid amount can't be more than the contract amount"))
            else:
                rec.contract_id.paid = rec.amount + rec.contract_id.paid
                rec.write({'state':'paid'})