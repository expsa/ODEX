# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import Warning, ValidationError


class AccountVoucher(models.Model):
    _name = 'account.voucher'
    _inherit = "account.voucher"

    period_id = fields.Many2one('fiscalyears.periods',
                                string='Period', required=True, readonly=True,
                                states={'draft': [('readonly', False)]},
                                help='''The fiscalyear period
                                used for this receipt.''')

    @api.onchange('date')
    def _onchange_date(self):
        for voucher in self:
            if voucher.date:
                periods = self.env['fiscalyears.periods'].search(
                    [('state', '=', 'open'),
                     ('start_date', '<=', voucher.date),
                     ('end_date', '>=', voucher.date)])
                if periods:
                    voucher.period_id = periods[0].id
                else:
                    raise Warning(
                        _('No fiscal year periods in this bill date.'))

    @api.multi
    @api.constrains('date', 'period_id')
    def _check_date_period(self):
        ''' check date and period_id
            are in the same date range
        '''
        for voucher in self:
            if voucher.date and voucher.period_id:
                date = fields.Date.from_string(voucher.date)
                period_start_date = fields.Date.from_string(
                    voucher.period_id.start_date)
                period_end_date = fields.Date.from_string(
                    voucher.period_id.end_date)
                if not (date >= period_start_date and
                        date >= period_start_date):
                    raise ValidationError(
                        _('''bill date and period must be in the same
                         date range'''))
            else:
                raise ValidationError(
                    _('''you must enter bill date and period for
                    this receipt'''))

    @api.model
    def create(self, vals):
        date = vals.get('date', False)
        period_id = vals.get('period_id', False)
        if date and not period_id:
            periods = self.env['fiscalyears.periods'].search(
                [('state', '=', 'open'),
                 ('start_date', '<=', date),
                 ('end_date', '>=', date)])
            if periods:
                vals.update({'period_id': periods[0].id})

        return super(AccountVoucher, self).create(vals)


class AccountVoucherLine(models.Model):
    _name = 'account.voucher.line'
    _inherit = "account.voucher.line"
    period_id = fields.Many2one('fiscalyears.periods',
                                related='voucher_id.period_id', store=True,
                                string='Period', related_sudo=False,
                                help='''The fiscalyear period
                                used for this receipt line.''')
