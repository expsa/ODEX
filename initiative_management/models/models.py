# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class initiative(models.Model):
    _name = 'initiative'

    name = fields.Char('Name', required=True)

    department_id = fields.Many2one('hr.department', 'Department',
                                    required=True)

    start_date = fields.Date(string='Start Date', required=True, help='''the start of the
     initiative''')
    end_date = fields.Date(string='End Date', required=True,
                           help='the end of the initiative')

    duration = fields.Char(string='Duration')

    initiative_owner = fields.Many2one(
        'res.users', 'Initiative Owner', required=True)

    initiative_manager = fields.Many2one(
        'res.users', 'Initiative Manager', required=True)

    strategic_goal_id = fields.Many2one(comodel_name='initiative.goal',
                                        string='Strategic Goal', required=True)

    goals_ids = fields.Many2many(comodel_name='initiative.goal',
                                 relation='initiative_goals_rel',
                                 column1='initiative_id',
                                 column2='goal_id',
                                 string='Goals', required=True)

    expense_service_ids = fields.One2many(
        comodel_name='product.product', inverse_name='initiative_id', string='Expense Services',
        domain=[('type', '=', 'service'),
                ('nature', '=', 'expense')])

    income_service_ids = fields.One2many(
        comodel_name='product.product', inverse_name='initiative_id', string='Income Services',
        domain=[('type', '=', 'service'),
                ('nature', '=', 'income')])

    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('open', 'Open'),
                                        ('closed', 'Closed'),
                                        ('cancel', 'Cancel')],
                             string='State', default='draft')

    type = fields.Selection(selection=[('income', 'Income'),
                                       ('expense', 'Expense'),
                                       ('both', 'Both')],
                            string='Type', default='both')

    @api.multi
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        ''' check start date and end date to see if :
            start date come after end date
        '''
        for obj in self:
            if fields.Date.from_string(obj.start_date) > \
                    fields.Date.from_string(self.end_date):
                raise ValidationError(
                    _('start date must be before end date'))
    
    @api.multi
    def copy(self):
        ''' prevent copy of initiative .
        '''
        raise ValidationError(
            _('You cannot copy a initiative .'))

    @api.multi
    def open(self):
        ''' make sure services have been selected for each
            initiative and change state to open .
        '''
        for rec in self:
            if not rec.expense_service_ids and not rec.income_service_ids:
                raise ValidationError(
                    _('you must select services for this initiative'))
            rec.state = 'open'

    @api.multi
    def close(self):
        ''' change state of the initiative
            to close .
        '''
        for rec in self:
            rec.state = 'closed'

    @api.multi
    def cancel(self):
        ''' change state to cancel .
        '''
        for rec in self:
            rec.state = 'cancel'

    @api.multi
    def draft(self):
        ''' change state to draft .
        '''
        for rec in self:
            rec.state = 'draft'

    @api.multi
    def unlink(self):
        ''' delete initiatives but they must be in draft state .
        '''
        for rec in self:
            if rec.state not in ['draft', 'cancel']:
                raise UserError(
                    _('You cannot delete an initiative not in cancel or draft state.'))

        return super(initiative, self).unlink()


class initiativeGoals(models.Model):
    _name = 'initiative.goal'

    name = fields.Char('Name', required=True)

    initiative_ids = fields.One2many(comodel_name='initiative',
                                     string='Initiatives',
                                     inverse_name='strategic_goal_id')

    parent_id = fields.Many2one(comodel_name='initiative.goal',
                                string='Strategic Goal')

    sub_goals = fields.One2many(comodel_name='initiative.goal',
                                string='Sub Goals',
                                inverse_name='parent_id')

    @api.multi
    def unlink(self):
        for goal in self:
            if goal.initiative_ids:
                raise UserError(
                    _('''you can not delete this Strategic Goal because it is related to Initiatives'''))

            goal.sub_goals.unlink()
        return super(initiativeGoals, self).unlink()
