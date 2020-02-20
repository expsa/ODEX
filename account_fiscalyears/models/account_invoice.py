# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import Warning, ValidationError


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    period_id = fields.Many2one('fiscalyears.periods',
                                string='Period', required=True, readonly=True,
                                states={'draft': [('readonly', False)]},
                                help='''The fiscalyear period
                                used for this invoice.''')

    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        for inv in self:
            if inv.date_invoice:
                periods = self.env['fiscalyears.periods'].search(
                    [('state', '=', 'open'),
                     ('start_date', '<=', inv.date_invoice),
                     ('end_date', '>=', inv.date_invoice)])
                if periods:
                    inv.period_id = periods[0].id
                else:
                    raise Warning(
                        _('No fiscal year periods in this date.'))

    @api.multi
    @api.constrains('date_invoice', 'period_id')
    def _check_date_period(self):
        ''' check date_invoice and period_id
            are in the same date range
        '''
        for inv in self:
            if inv.date_invoice and inv.period_id:
                date_invoice = fields.Date.from_string(inv.date_invoice)
                period_start_date = fields.Date.from_string(
                    inv.period_id.start_date)
                period_end_date = fields.Date.from_string(
                    inv.period_id.end_date)
                if not (date_invoice >= period_start_date and
                        date_invoice >= period_start_date):
                    raise ValidationError(
                        _('''invoice date and period_id are in the same
                         date range'''))
            else:
                raise ValidationError(
                    _('''you must enter invoice date and period for
                    this invoice'''))

    @api.model
    def create(self, vals):
        date_invoice = vals.get('date_invoice', False)
        period_id = vals.get('period_id', False)
        if date_invoice and not period_id:
            periods = self.env['fiscalyears.periods'].search(
                [('state', '=', 'open'),
                 ('start_date', '<=', date_invoice),
                 ('end_date', '>=', date_invoice)])
            if periods:
                vals.update({'period_id': periods[0].id})

        return super(AccountInvoice, self).create(vals)


class AccountInvoiceLine(models.Model):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
    period_id = fields.Many2one('fiscalyears.periods',
                                related='invoice_id.period_id', store=True,
                                string='Period', related_sudo=False,
                                help='''The fiscalyear period
                                used for this invoice line.''')
