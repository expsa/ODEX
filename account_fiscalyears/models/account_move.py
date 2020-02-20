# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import Warning, ValidationError


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    period_id = fields.Many2one('fiscalyears.periods',
                                string='Period', required=True, readonly=True,
                                states={'draft': [('readonly', False)]},
                                help='''The fiscalyear period
                                used for this receipt.''')

    @api.onchange('date')
    def _onchange_date_period(self):
        for inv in self:
            if inv.date:
                periods = self.env['fiscalyears.periods'].search(
                    [('state', '=', 'open'),
                     ('start_date', '<=', inv.date),
                     ('end_date', '>=', inv.date)])
                if periods:
                    inv.period_id = periods[0].id
                else:
                    raise Warning(
                        _('No fiscal year periods in this move date.'))

    @api.multi
    @api.constrains('date', 'period_id')
    def _check_date_period(self):
        ''' check date and period_id
            are in the same date range
        '''
        for move in self:
            if move.date and move.period_id:
                date = fields.Date.from_string(move.date)
                period_start_date = fields.Date.from_string(
                    move.period_id.start_date)
                period_end_date = fields.Date.from_string(
                    move.period_id.end_date)
                if not (date >= period_start_date and
                        date >= period_start_date):
                    raise ValidationError(
                        _('''move date and period must be in the same
                         date range'''))
            else:
                raise ValidationError(
                    _('''you must enter move date and period for
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

        return super(AccountMove, self).create(vals)


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"
    period_id = fields.Many2one('fiscalyears.periods',
                                related='move_id.period_id', store=True,
                                string='Period', related_sudo=False,
                                help='''The fiscalyear period
                                used for this move line.''')
