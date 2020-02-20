# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


class CrossoveredBudget(models.Model):
    _name = "crossovered.budget"
    _inherit = "crossovered.budget"

    fiscalyear_id = fields.Many2one('fiscalyears',
                                    string='Fiscal Year', required=True, readonly=True,
                                    states={'draft': [('readonly', False)]},
                                    help='''The fiscalyear
                                used for this budget.''')

    @api.onchange('date_from', 'date_to')
    def _onchange_dates(self):
        for budget in self:
            if budget.date_from and budget.date_to:
                fiscalyears = self.env['fiscalyears'].search(
                    [('state', '=', 'open'),
                     ('start_date', '<=', budget.date_from),
                     ('end_date', '>=', budget.date_to)])
                if fiscalyears:
                    budget.fiscalyear_id = fiscalyears[0].id
                else:
                    raise Warning(
                        _('''No fiscal year for
                         this budget date range.'''))

    @api.multi
    @api.constrains('date_from', 'date_to', 'fiscalyear_id')
    def _check_dates_fiscalyear(self):
        ''' check date and fiscalyear_id
            are in the same date range
        '''
        for budget in self:
            if budget.date_from and budget.date_to and budget.fiscalyear_id:
                date_from = fields.Date.from_string(budget.date_from)
                date_to = fields.Date.from_string(budget.date_to)
                fiscalyear_start_date = fields.Date.from_string(
                    budget.fiscalyear_id.start_date)
                fiscalyear_end_date = fields.Date.from_string(
                    budget.fiscalyear_id.end_date)
                if not (date_from >= fiscalyear_start_date and
                        date_to <= fiscalyear_end_date):
                    raise ValidationError(
                        _('''budget date range and fiscalyear must be in
                         the same'''))
            else:
                raise ValidationError(
                    _('''you must enter budget date range and fiscalyear for
                    this receipt'''))


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    fiscalyear_id = fields.Many2one('fiscalyears',
                                    related='crossovered_budget_id.fiscalyear_id',
                                    store=True, string='Period',
                                    related_sudo=False,
                                    help='''The fiscalyear
                                used for this budget line.''')
