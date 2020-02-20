from __future__ import division
from odoo import models, fields, api, _, exceptions
# from datetime import datetime
# import logging


class employee_overtime_request(models.Model):
    _name = 'employee.overtime.request'
    _rec_name = 'request_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    request_date = fields.Date()
    reason = fields.Text()
    date_to = fields.Date()
    date_from = fields.Date()
    transfer_type = fields.Selection(
        [('accounting', 'Accounting'), ('payroll', 'Payroll')], default='accounting')

    overtime_plase = fields.Selection(
        [('inside', 'Inside'), ('outside', 'Outside')], default='inside')


    state = fields.Selection(
        [('draft', _('Draft')),
         ('submit', _('Submit')),
         ('direct_manager', _('Direct Manager')),
         ('financial_manager', _('Financial Manager')),
         ('hr_aaproval', _('HR Approval')),
         ('validated', _('Validated')),
         ('refused', _('Refused'))], default="draft",track_visibility='always')

    # Relation fields
    account_id = fields.Many2one(comodel_name='account.account', string='Account')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Payment Method',
                                 domain=[('type', 'in', ('bank', 'cash'))])
    benefits_discounts = fields.Many2one(comodel_name='hr.salary.rule', string='Benefits/Discounts', domain=[('rules_type', '=', 'overtime')])
    line_ids_over_time = fields.One2many(comodel_name='line.ids.over.time', inverse_name='employee_over_time_id')

    @api.onchange('transfer_type', 'account_id', 'journal_id', 'line_ids_over_time')
    def onchange_transfer_type(self):
        if self.transfer_type == 'payroll':
            self.account_id = False
            self.journal_id = False
            for line in self.line_ids_over_time:
                line.account_id = False
                line.journal_id = False
        if self.transfer_type == 'accounting':
            for line in self.line_ids_over_time:
                if self.state == 'hr_aaproval':

                    if not line.account_id:
                        line.account_id = self.account_id
                    if not line.journal_id:
                        line.journal_id = self.journal_id
                else:
                    line.account_id = False
                    line.journal_id = False

    @api.onchange('account_id')
    def onchange_account_id(self):
        for line in self.line_ids_over_time:
            line.account_id = self.account_id

    @api.onchange('journal_id')
    def onchange_journal_id(self):
        for line in self.line_ids_over_time:
            line.journal_id = self.journal_id

    @api.one
    def re_draft(self):
        # when redraft cancel the created account move
        if self.transfer_type == 'payroll':
            advantages = self.env['contract.advantage']
            contract_advantage = advantages.search([('over_time_id', '=', self.id)])
            if contract_advantage:
                contract_advantage.unlink()
            self.state = 'draft'
        if self.transfer_type == 'accounting':
            if self.line_ids_over_time[0].move_id:
                move_id_not_draft = False
                for line in self.line_ids_over_time:
                    if line.move_id.state == 'posted':
                        move_id_not_draft_name = line.move_id.name
                        move_id_not_draft = True
                if move_id_not_draft:
                    raise exceptions.Warning(_(
                        'You can not cancel account move "%s" in state not draft') % move_id_not_draft_name)
                else:
                    for record in self.line_ids_over_time:
                        #record.move_id.write({'state': 'canceled'})
                        record.move_id.unlink()
                        record.write({
                            'move_id': False
                        })
                        record.account_id = False
                        record.journal_id = False
                    self.write({'state': 'draft'})
                    self.account_id = False
                    self.journal_id = False
            else:
                self.write({
                    'state': 'draft',
                    'account_id': False,
                    'journal_id': False
                })
                for record in self.line_ids_over_time:
                    record.write({
                        'move_id': False,
                        'account_id': False,
                        'journal_id': False
                    })

    @api.multi
    def submit(self):
        for item in self:
            for line in item.line_ids_over_time:
                mail_content = "Hello I'm", line.employee_id.name, " request Need to overtime amount =",line.price_hour,"Please approved thanks."
                main_content = {
                     'subject': _('Request Overtime Employee %s') % (line.employee_id.name),
                     'author_id': self.env.user.partner_id.id,
                     'body_html': mail_content,
                     'email_to': line.employee_id.department_id.email_manager,
                  }
                self.env['mail.mail'].create(main_content).send()
        self.state = "submit"

    @api.multi
    def direct_manager(self):
        self.state = "direct_manager"

    @api.multi
    def financial_manager(self):
        self.state = "financial_manager"

    @api.multi
    def hr_aaproval(self):
        self.state = "hr_aaproval"

    @api.multi
    def validated(self):
        if self.transfer_type == 'accounting':
            for item in self:
                for record in item.line_ids_over_time:
                    debit_line_vals = {
                        'name': record.employee_id.name,
                        'debit': record.price_hour,
                        'account_id': record.account_id.id,
                        'partner_id': record.employee_id.user_id.partner_id.id
                    }
                    credit_line_vals = {
                        'name': record.employee_id.name,
                        'credit': record.price_hour,
                        'account_id': record.journal_id.default_credit_account_id.id,
                        'partner_id': record.employee_id.user_id.partner_id.id
                    }
                    move = record.env['account.move'].create({
                        'state': 'draft',
                        'journal_id': record.journal_id.id,
                        'date': item.request_date,
                        'ref': record.employee_id.name,
                        'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                    })

                    record.move_id = move.id
            self.state = "validated"
        if self.transfer_type == 'payroll':
            # last_day_of_current_month = date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1])
            # first_day_of_current_month = date.today().replace(day=1)
            for item in self:
                for record in item.line_ids_over_time:
                    if record.employee_id.contract_id:
                        record.employee_id.contract_id.write({
                            'advantages': [(0, 0, {
                                'benefits_discounts': item.benefits_discounts.id,
                                'type': 'customize',
                                'date_from': item.date_from,
                                'date_to': item.date_to,
                                'amount': record.price_hour,
                                'over_time_id': self.id
                            })]
                        })
                    else:
                        raise exceptions.Warning(_(
                            'Employee "%s" has no contract Please create contract to add line to advantages') % record.employee_id.name)

            self.state = "validated"

    @api.multi
    def refused(self):
        self.state = "refused"

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(employee_overtime_request, self).unlink()


class HrEmployeeOverTime(models.Model):
    _name = 'line.ids.over.time'

    over_time_workdays_hours = fields.Float(string="workdays hours")
    over_time_vacation_hours = fields.Float(string="Vacation days hours")
    regular_hourly_rate = fields.Float(string='Regular Hourly Rate', compute='get_hour_price')
    price_hour = fields.Float(string='Overtime Amount', compute='get_over_time_amount', store=True)

    # Relational fields
    account_id = fields.Many2one('account.account')
    journal_id = fields.Many2one('account.journal', string='Payment Method', domain=[('type', 'in', ('bank', 'cash'))])
    move_id = fields.Many2one('account.move')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_over_time_id = fields.Many2one('employee.overtime.request', string='Employee')

    # Select employee once in Over Time Line
    @api.onchange('employee_id')
    def select_employee_once(self):
        employee_ids = self.env['hr.employee'].search([]).ids

        for line in self.employee_over_time_id.line_ids_over_time:
            if line.employee_id:
                if line.employee_id.id in employee_ids:
                    employee_ids.remove(line.employee_id.id)

        return {'domain': {'employee_id': [('id', 'in', employee_ids)]}}

    @api.model
    def default_get(self, fields):
        res = super(HrEmployeeOverTime, self).default_get(fields)
        if self._context.get('account_id') and self._context.get('journal_id'):
            res['account_id'] = self._context.get('account_id')
            res['journal_id'] = self._context.get('journal_id')
        return res

    @api.multi
    @api.depends('employee_id.contract_id', 'over_time_workdays_hours', 'over_time_vacation_hours', 'employee_id')
    def get_over_time_amount(self):
        for line in self:
            contract_id = line.employee_id.contract_id
            wage = contract_id.total_allowance if contract_id and contract_id.total_allowance else 0
            if contract_id.working_hours:
                total_hours = contract_id.working_hours.work_days * contract_id.working_hours.work_hour
                if total_hours != 0:
                    price_hour = wage / total_hours
                else:
                    price_hour = 0
                o_t_a_d = price_hour * contract_id.working_hours.overtime_factor_daily * line.over_time_workdays_hours
                o_t_a_v = price_hour * contract_id.working_hours.overtime_factor_holiday * line.over_time_vacation_hours
            else:
                o_t_a_d = o_t_a_v = 0
            line.price_hour = o_t_a_d + o_t_a_v
            emp_total_hours= line.over_time_workdays_hours + line.over_time_vacation_hours

            if emp_total_hours > contract_id.working_hours.max_overtime_hour:
                raise exceptions.Warning(_('The Number Of Overtime Hours For The Employee %s Is Greater Max Hours')% line.employee_id.name)

    @api.multi
    @api.onchange('employee_id')
    def get_hour_price(self):
        for line in self:
            line.regular_hourly_rate = 0
            if line.employee_id:
                contract_id = line.employee_id.contract_id
                wage = contract_id.total_allowance if contract_id and contract_id.total_allowance else 0
                if contract_id.working_hours:
                    total_hours = contract_id.working_hours.work_days * contract_id.working_hours.work_hour
                    if total_hours != 0:
                        price_hour_regular = wage / total_hours
                    else:
                        price_hour_regular = 0
                    line.regular_hourly_rate = price_hour_regular
