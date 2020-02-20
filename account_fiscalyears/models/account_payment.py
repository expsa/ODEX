# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from odoo.addons.account.models.account_payment import \
    MAP_INVOICE_TYPE_PARTNER_TYPE


class account_payment(models.Model):
    _name = 'account.payment'
    _inherit = 'account.payment'

    period_id = fields.Many2one('fiscalyears.periods',
                                string='Period', required=True, readonly=True,
                                states={'draft': [('readonly', False)]},
                                help='''The fiscalyear period
                                used for this payment.''')

    @api.onchange('payment_date')
    def _onchange_payment_date(self):
        for payment in self:
            if payment.payment_date:
                periods = self.env['fiscalyears.periods'].search(
                    [('state', '=', 'open'),
                     ('start_date', '<=', payment.payment_date),
                     ('end_date', '>=', payment.payment_date)])
                if periods:
                    payment.period_id = periods[0].id
                else:
                    raise Warning(
                        _('No fiscal year periods in this payment date.'))

    @api.multi
    @api.constrains('payment_date', 'period_id')
    def _check_date_period(self):
        ''' check payment_date and period_id
            are in the same date range
        '''
        for payment in self:
            if payment.payment_date and payment.period_id:
                payment_date = fields.Date.from_string(payment.payment_date)
                period_start_date = fields.Date.from_string(
                    payment.period_id.start_date)
                period_end_date = fields.Date.from_string(
                    payment.period_id.end_date)
                if not (payment_date >= period_start_date and
                        payment_date >= period_start_date):
                    raise ValidationError(
                        _('''payment date and period must be in the same
                         date range'''))
            else:
                raise ValidationError(
                    _('''you must enter payment date and period for
                    this payment and there are must be in the same
                         date range'''))

    @api.model
    def create(self, vals):
        payment_date = vals.get('payment_date', False)
        period_id = vals.get('period_id', False)
        if payment_date and not period_id:
            periods = self.env['fiscalyears.periods'].search(
                [('state', '=', 'open'),
                 ('start_date', '<=', payment_date),
                 ('end_date', '>=', payment_date)])
            if periods:
                vals.update({'period_id': periods[0].id})

        return super(account_payment, self).create(vals)


class account_register_payments(models.TransientModel):
    _name = "account.register.payments"
    _inherit = 'account.register.payments'

    period_id = fields.Many2one('fiscalyears.periods',
                                string='Period', required=True,
                                help='''The fiscalyear period
                                used for this invoice.''')

    @api.onchange('payment_date')
    def _onchange_payment_date(self):
        for inv in self:
            if inv.payment_date:
                periods = self.env['fiscalyears.periods'].search(
                    [('state', '=', 'open'),
                     ('start_date', '<=', inv.payment_date),
                     ('end_date', '>=', inv.payment_date)])
                if periods:
                    inv.period_id = periods[0].id
                else:
                    raise Warning(
                        _('No fiscal year periods in this payment date.'))

    @api.multi
    @api.constrains('payment_date', 'period_id')
    def _check_date_period(self):
        ''' check payment_date and period_id
            are in the same date range
        '''
        for inv in self:
            if inv.payment_date and inv.period_id:
                payment_date = fields.Date.from_string(inv.payment_date)
                period_start_date = fields.Date.from_string(
                    inv.period_id.start_date)
                period_end_date = fields.Date.from_string(
                    inv.period_id.end_date)
                if not (payment_date >= period_start_date and
                        payment_date >= period_start_date):
                    raise ValidationError(
                        _('''payment date and period must be in the same
                         date range'''))
            else:
                raise ValidationError(
                    _('''you must enter payment date and period for
                    this invoice and there are must be in the same
                         date range'''))

    @api.multi
    def _prepare_payment_vals2(self, invoices):
        '''Create the payment values.

        :param invoices: The invoices that should have the same commercial
         partner and the same type.
        :return: The payment values as a dictionary.
        '''
        amount = self._compute_payment_amount(
            invoices) if self.multi else self.amount
        payment_type = ('inbound' if amount >
                        0 else 'outbound') if self.multi else self.payment_type
        return {
            'journal_id': self.journal_id.id,
            'payment_method_id': self.payment_method_id.id,
            'payment_date': self.payment_date,
            'communication': self.communication,
            'invoice_ids': [(6, 0, invoices.ids)],
            'payment_type': payment_type,
            'amount': abs(amount),
            'currency_id': self.currency_id.id,
            'partner_id': invoices[0].commercial_partner_id.id,
            'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type],
            'period_id': self.period_id.id
        }
