# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class fiscalyears_periods(models.Model):
    _inherit = 'fiscalyears.periods'

    moves_ids = fields.One2many(comodel_name='account.move',
                                inverse_name='period_id',
                                string='Moves', help='''the moves
                                    linked with the period''')

    invoices_ids = fields.One2many(comodel_name='account.invoice',
                                   inverse_name='period_id',
                                   string='Invoices', help='''the invoices
                                    linked with the period''')

    payments_ids = fields.One2many(comodel_name='account.payment',
                                   inverse_name='period_id',
                                   string='Payments', help='''the payments
                                    linked with the period''')

    vouchers_ids = fields.One2many(comodel_name='account.voucher',
                                   inverse_name='period_id',
                                   string='Vouchers', help='''the vouchers
                                    linked with the period''')

    @api.multi
    def cancel(self):
        ''' change state to cancel .
        '''
        for rec in self:
            if rec.moves_ids:
                raise ValidationError(
                    _('you can not cancel a period linked with moves'))

            # if rec.budgets_ids:
            #     raise ValidationError(
            #         _('you can not cancel a period linked with budgets'))

            if rec.invoices_ids:
                raise ValidationError(
                    _('you can not cancel a period linked with invoices'))

            if rec.payments_ids:
                raise ValidationError(
                    _('you can not cancel a period linked with payments'))

            if rec.vouchers_ids:
                raise ValidationError(
                    _('you can not cancel a period linked with vouchers'))

            rec.state = 'cancel'

    @api.multi
    def close(self):
        ''' change state of the  period
            to close after make sure every linked operation is reached
            last state.
        '''
        for rec in self:
            if not all(x == 'posted' for x in
                       rec.mapped('moves_ids.state')):
                raise ValidationError(
                    _('make sure all linked moves have been posted'))

            # if not all(x == 'confirm' for x in
            #            rec.mapped('budgets_ids.state')):
            #     raise ValidationError(
            #         _('make sure all linked budgets have been confirmed'))

            # close this condition as requested by PAs
            # if not all(x == 'paid' for x in
            #            rec.mapped('invoices_ids.state')):
            #     raise ValidationError(
            #         _('make sure all linked invoices have been paid'))

            # if not all(x == 'posted' for x in
            #            rec.mapped('payments_ids.state')):
            #     raise ValidationError(
            #         _('make sure all linked payments have been posted'))

            # if not all(x == 'posted' for x in
            #            rec.mapped('vouchers_ids.state')):
            #     raise ValidationError(
            #         _('make sure all linked vouchers have been posted'))

            rec.state = 'closed'
