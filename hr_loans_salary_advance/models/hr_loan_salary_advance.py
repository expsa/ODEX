# -*- coding: utf-8 -*-
from __future__ import division
from odoo import models, fields, api, _, exceptions
from dateutil import relativedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.safe_eval import safe_eval
# from pprint import pprint
from odoo import SUPERUSER_ID
from datetime import datetime, timedelta, date



class HrSalaryAdvance(models.Model):
    _name = 'hr.loan.salary.advance'
    _rec_name = 'employee_id'
    _description = 'Employee Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char()
    state = fields.Selection(
        [('draft', _('Draft')), ('submit', _('Submit')), ('dirct_manager', _('Direct Manager')),
         ('hr_manager', _('HR Manager')), ('executive_manager', _('Executive Manager')),
         ('pay', _('Pay')), ('refused', _('Refused')), ('closed', _('Closed')), ('cancel', _('Cancel'))],
        default="draft",track_visibility='always')
    date = fields.Date()
    from_hr_depart = fields.Boolean()
    is_old = fields.Boolean()
    months_employeed = fields.Float(compute='_get_month_no')
    evaluation_grade = fields.Many2one(related='employee_id.contract_id.appraisal_result_id', readonly=True)
    contract_duration_date = fields.Date(related='employee_id.contract_id.date_start')
    payment_ref = fields.Char()
    emp_expect_amount = fields.Float()
    finance_propos_amount = fields.Float(compute='_get_finance_gm_propos_amount', store=True)
    gm_propos_amount = fields.Float(compute='_get_finance_gm_propos_amount', store=True)
    months = fields.Integer(default=1)
    monthly_salary = fields.Float()
    total_paid_inst = fields.Float(compute='get_total_paid_installment')
    remaining_loan_amount = fields.Float(compute='get_remaining_loan_amount')
    installment_amount = fields.Float(compute='get_installment_amount')
    # previous_loan = fields.Boolean()
    end_date = fields.Date(related='employee_id.contract_id.date_end')

    # Relational fields
    company_id = fields.Many2one(comodel_name='res.company', related='employee_id.company_id')
    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    deduction_lines = fields.One2many('loan.installment.line', 'deduction_line')
    moves_ids = fields.One2many('hr.account.moves', 'moves_id')
    employee_id = fields.Many2one('hr.employee', 'Employee Id', default=lambda item: item.get_user_id(),index=True)
    request_type = fields.Many2one('loan.request.type')

    # change state to draft
    @api.multi
    def draft_state(self):
        for item in self:
            if item.moves_ids:
                for line in item.moves_ids:
                    if line.journal_move_id:
                        if line.journal_move_id.state == 'draft':
                            #line.journal_move_id.state = 'canceled'
                            line.journal_move_id.unlink()
                            line.unlink()
                            item.state = 'draft'
                        else:
                            raise exceptions.Warning(_(
                                'You can not re-draft Loan because account move with ID "%s" in state Posted') % line.journal_move_id.name)
                    else:
                       self.state = 'draft'
            else:
                self.state = 'draft'

    # change state to submit
    @api.multi
    def submit(self):
        for item in self:
            if item.request_type.year > (item.months_employeed / 12):
                raise exceptions.Warning(_
                                         ('You can not submit loan when your total service is less than number of years'))
            deductions = item.deduction_lines
            if len(deductions) == 0:
                raise exceptions.Warning(_('You must create al least one installment'))
            else:

                mail_content = "Hello I'm", item.employee_id.name, " request Need to ", item.request_type.name,"Amount",item.emp_expect_amount,"Please approved thanks :)."
                main_content = {
                        'subject': _('Request Loan-%s Employee %s') % (item.request_type.name, item.employee_id.name),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': item.department_id.email_manager,
                    }
                self.env['mail.mail'].create(main_content).send()
        self.percentage_constrain()
        self.state = "submit"


    @api.multi
    def dirct_manager(self):
        self.state = "dirct_manager"

    @api.multi
    def hr_manager(self):
        self.state = "hr_manager"

    @api.multi
    def executive_manager(self):
        self.state = "executive_manager"

    # change state to pay
    @api.multi
    def pay(self):
        for item in self:
            if item.is_old is False:
                debit_line_vals = {
                    'name': 'debit',
                    'debit': item.gm_propos_amount,
                    'account_id': item.request_type.account_id.id,
                    'partner_id': item.employee_id.user_id.partner_id.id
                }
                credit_line_vals = {
                    'name': 'credit',
                    'credit': item.gm_propos_amount,
                    'account_id': item.request_type.journal_id.default_credit_account_id.id,
                    'partner_id': item.employee_id.user_id.partner_id.id
                }
                move = self.env['account.move'].create({
                    'state': 'draft',
                    'journal_id': item.request_type.journal_id.id,
                    'date': item.date,
                    'ref': 'Loan',
                    'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                })

                self.env['hr.account.moves'].create({
                    'number': item.code,
                    'amount': item.gm_propos_amount,
                    'journal': item.request_type.journal_id.id,
                    'partner_id': item.employee_id.user_id.partner_id.id,
                    'date': item.date,
                    'journal_move_id': move.id,
                    'moves_id': item.id
                })

        self.state = "pay"

    @api.multi
    def refused(self):
        self.state = "refused"

    @api.multi
    def closed(self):
        self.state = "closed"

    @api.multi
    def cancel(self):
        self.state = "cancel"

    @api.multi
    def get_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False

 

    @api.multi
    def create_loan(self):
        for item in self:
            if item.contract_duration_date:
                if item.end_date:
                    if item.months <= item.months_employeed:
                        date_start = fields.Datetime.from_string(item.date)

                        items = []
                        for number in range(item.months):
                            dt = date_start + relativedelta.relativedelta(months=number)
                            date_end = fields.Datetime.to_string(dt)

                            record_id = self.env['loan.installment.line'].create({
                                'installment_date': date_end,
                                'installment_amount': item.installment_amount,
                                'paid': False
                            })

                            print(record_id)
                            items.append(record_id.id)
                        item.deduction_lines = self.env['loan.installment.line'].browse(items)
                    else:
                        raise exceptions.Warning(
                            _('The number of installments does not exceed the employee contract period.'))

                else:
                    date_start = fields.Datetime.from_string(item.date)

                    items = []
                    for number in range(item.months):
                        dt = date_start + relativedelta.relativedelta(months=number)
                        date_end = fields.Datetime.to_string(dt)

                        record_id = self.env['loan.installment.line'].create({
                            'installment_date': date_end,
                            'installment_amount': item.installment_amount,
                            'paid': False
                        })
                        items.append(record_id.id)
                    item.deduction_lines = self.env['loan.installment.line'].browse(items)
            else:
                raise exceptions.Warning(_('The employee does not have contract Start Date .'))

    @api.multi
    @api.depends('gm_propos_amount', 'months')
    def get_installment_amount(self):
        for item in self:
            if item.gm_propos_amount > 0.0 and item.months > 0:
                item.installment_amount = item.gm_propos_amount / float(item.months)

    @api.multi
    @api.depends('contract_duration_date', 'end_date')
    def _get_month_no(self):
        for item in self:
            if item.contract_duration_date and item.end_date:

                start_contract_date = datetime.strptime(item.contract_duration_date, "%Y-%m-%d")
                end_contract_date = datetime.strptime(item.end_date, "%Y-%m-%d")

                relative_months = relativedelta.relativedelta(end_contract_date, start_contract_date).months
                relative_years = relativedelta.relativedelta(end_contract_date, start_contract_date).years
                item.months_employeed = relative_months + (relative_years * 12)

            else:

                current_date = date.today()
                start_contract_date = datetime.strptime(item.contract_duration_date, "%Y-%m-%d")
                relative_months = relativedelta.relativedelta(current_date, start_contract_date).months
                relative_years = relativedelta.relativedelta(current_date, start_contract_date).years
                item.months_employeed = relative_months + (relative_years * 12)

    @api.depends('deduction_lines')
    def get_total_paid_installment(self):
        for item in self:
            tota_number = 0.0
            if item.employee_id.id:
                for line in item.deduction_lines:
                    if line.paid is True:
                        tota_number += line.installment_amount
                item.total_paid_inst = tota_number

    @api.depends('deduction_lines')
    def get_remaining_loan_amount(self):
        for item in self:
            item.remaining_loan_amount = item.gm_propos_amount - item.total_paid_inst

    @api.constrains('deduction_lines')
    def deduction_lines_constraine(self):
        for item in self:
            deductions = item.deduction_lines
            if len(deductions) == 0:
                raise exceptions.Warning(_('You must create al least one installment'))

    @api.depends('emp_expect_amount')
    def _get_finance_gm_propos_amount(self):
        for item in self:
            if item.emp_expect_amount:
                item.finance_propos_amount = item.emp_expect_amount
                item.gm_propos_amount = item.emp_expect_amount

    # percentage constrain depending on the sart date
    @api.constrains('date')
    def percentage_constrain(self):
        records = self.env['hr.loan.salary.advance'].search(
            [('employee_id', '=', self.employee_id.id), ('date', '=', self.date), ('state', '=', 'pay')])
        total_number = 0.0

        # Get all un paid installments from all loans that it's state is pay and it's date is this loan date in "total_number"
        for item in records:
            for line in item.deduction_lines:

                if line.paid is False and line.installment_date == item.date:
                    total_number += line.installment_amount

        # Adding to total_number all intallments that not paid in current loan
        for item in self:
            for line in item.deduction_lines:
                if line.paid is False and line.installment_date == item.date:
                    total_number += line.installment_amount


        # Check if [exp_payroll_custom] module is installed
        Module = self.env['ir.module.module'].sudo()
        modules = Module.search([('state', '=', 'installed'), ('name', '=', 'exp_payroll_custom')])

        if modules :
            # get payslip by check if the loan date is in "Date from - Date to" in payslip
            '''records = self.env['hr.payslip'].search([('employee_id','=', self.employee_id.id),
                                                     ('date_from','<=',self.date),
                                                     ('date_to','>=',self.date)])'''
            emp_deduction = item.employee_id.contract_id.total_deduction
            # adding total deductions to total_number
            #for record in records:
            #   total_number += record.total_deductions - recordss

            total_number = total_number - emp_deduction

        percentage = self.request_type.percentage / 100
        percentage_salary = self.monthly_salary * percentage

        if percentage_salary < total_number:
            raise exceptions.Warning(
                _('The total number of installment of all months in start date is greater than the salary percentage'))

    @api.onchange('request_type')
    def _get_employee_expect_amount(self):

        # Initialize component
        self.emp_expect_amount = 0.0

        if self.request_type.loan_type == 'percentage':
            total = 0.0

            for rule in self.request_type.allowance_id:
                if self.employee_id:
                    if self.employee_id.contract_id:
                        total += self._compute_rule(rule, self.employee_id.contract_id)
                    else:
                        raise exceptions.Warning(_("Employee '%s' has no contract") % self.employee_id.name)

            if self.request_type.factor > 0:
                self.emp_expect_amount = total * self.request_type.factor
            else:
                self.emp_expect_amount = total

        else:
            self.emp_expect_amount = self.request_type.amount

    # Compute salary rules
    @api.multi
    def _compute_rule(self, rule, contract):

        baselocaldict = {'categories': {}, 'rules': {}, 'payslip': {}, 'worked_days': {},
                         'inputs': {}}
        localdict = dict(baselocaldict, employee=contract.employee_id, contract=contract)

        if rule.amount_select == 'percentage':
            total_percent = 0
            if rule.related_benefits_discounts:
                for line in rule.related_benefits_discounts:
                    if line.amount_select == 'fix':
                        total_percent += self._compute_rule(line, contract)
                    elif line.amount_select == 'percentage':
                        total_percent += self._compute_rule(line, contract)
                    else:
                        total_percent += self._compute_rule(line, contract)
            if total_percent:
                if rule.salary_type == 'fixed':
                    try:
                        return float(total_percent * rule.amount_percentage / 100)
                    except:
                        raise UserError(
                            _('Wrong percentage base or quantity defined for salary rule %s (%s).') % (
                                rule.name, rule.code))
                elif rule.salary_type == 'related_levels':
                    levels_ids = rule.salary_amount_ids.filtered(
                        lambda item: item.salary_scale_level.id == contract.salary_level.id)
                    if levels_ids:
                        for l in levels_ids:
                            try:
                                return float(l.salary * total_percent / 100)
                            except:
                                raise UserError(
                                    _('Wrong quantity defined for salary rule %s (%s).') % (
                                        rule.name, rule.code))
                    else:
                        return 0
                elif rule.salary_type == 'related_groups':
                    groups_ids = rule.salary_amount_ids.filtered(
                        lambda item: item.salary_scale_group.id == contract.salary_group.id)
                    if groups_ids:
                        for g in groups_ids:
                            try:
                                return float(g.salary * total_percent / 100)
                            except:
                                raise UserError(
                                    _('Wrong quantity defined for salary rule %s (%s).') % (
                                        rule.name, rule.code))
                    else:
                        return 0
                elif rule.salary_type == 'related_degrees':
                    degrees_ids = rule.salary_amount_ids.filtered(
                        lambda item: item.salary_scale_degree.id == contract.salary_degree.id)
                    if degrees_ids:
                        for d in degrees_ids:
                            try:
                                return float(d.salary * total_percent / 100)
                            except:
                                raise UserError(
                                    _('Wrong quantity defined for salary rule %s (%s).') % (
                                        rule.name, rule.code))
                    else:
                        return 0
            else:
                try:
                    return 0
                except:
                    raise Warning(_('There is no total for rule : %s') % (rule.name))

        elif rule.amount_select == 'fix':
            if rule.salary_type == 'fixed':
                try:
                    return rule.fixed_amount
                except:
                    raise UserError(_('Wrong quantity defined for salary rule %s (%s).') % (rule.name, rule.code))
            elif rule.salary_type == 'related_levels':
                levels_ids = rule.salary_amount_ids.filtered(
                    lambda item: item.salary_scale_level.id == contract.salary_level.id)
                if levels_ids:
                    for l in levels_ids:
                        try:
                            return l.salary
                        except:
                            raise UserError(
                                _('Wrong quantity defined for salary rule %s (%s).') % (rule.name, rule.code))
                else:
                    return 0
            elif rule.salary_type == 'related_groups':
                groups_ids = rule.salary_amount_ids.filtered(
                    lambda item: item.salary_scale_group.id == contract.salary_group.id)
                if groups_ids:
                    for g in groups_ids:
                        try:
                            return g.salary
                        except:
                            raise UserError(
                                _('Wrong quantity defined for salary rule %s (%s).') % (rule.name, rule.code))
                else:
                    return 0
            elif rule.salary_type == 'related_degrees':
                degrees_ids = rule.salary_amount_ids.filtered(
                    lambda item: item.salary_scale_degree.id == contract.salary_degree.id)
                if degrees_ids:
                    for d in degrees_ids:
                        try:
                            return d.salary
                        except:
                            raise UserError(
                                _('Wrong quantity defined for salary rule %s (%s).') % (rule.name, rule.code))
                else:
                    return 0
            else:
                raise UserError(_('Error'))

        else:
            try:
                safe_eval(rule.amount_python_compute, localdict, mode='exec', nocopy=True)
                paython_code = float(localdict['result']), 'result_qty' in localdict and localdict[
                    'result_qty'] or 1.0, 'result_rate' in localdict and localdict['result_rate'] or 100.0
                return float(localdict['result'])
            except:
                raise UserError(_('Wrong python code defined for salary rule %s (%s).') % (rule.name, rule.code))

    # Override write function
    def write(self, value):
        result = super(HrSalaryAdvance, self).write(value)
        return result

    # override unlink function
    def unlink(self):
        for item in self:
            if item.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))

            if item.total_paid_inst > 0.0:
                raise exceptions.Warning(_('You can not delete record when total paid installment greater than zero'))

        return super(HrSalaryAdvance, self).unlink()

    # override create function
    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('hr.loan.salary.advance') or '/'
        values['code'] = seq

        res = super(HrSalaryAdvance, self).create(values)

        res.finance_propos_amount = values['finance_propos_amount']
        res.gm_propos_amount = values['gm_propos_amount']

        get_loans = self.env['hr.loan.salary.advance'].search([])

        total_installment = 0.0

        for item in get_loans:
            if item.request_type.number_of_request == 'once' and res.request_type.number_of_request == 'once' and item.id != res.id:
                raise exceptions.Warning(
                    _('You can not create loan that have request type with number of request is once.'))

            if item.request_type.name == res.request_type.name:
                if res.request_type.allow_overlapping is False:
                    for line in item.deduction_lines:
                        if line.paid is False:
                            raise exceptions.Warning(
                                _('You can not create loan when there is un paid loan with the same type.'))

                        total_installment += line.installment_amount
        return res


HrSalaryAdvance()


class LoanInstallmentLine(models.Model):
    _name = 'loan.installment.line'
    installment_date = fields.Date()
    installment_amount = fields.Float()
    paid = fields.Boolean()
    payment_date = fields.Date()

    # Relational fields
    deduction_line = fields.Many2one(comodel_name='hr.loan.salary.advance')

    @api.multi
    def postpone_of_installment(self):
        action = self.env.ref('hr_loans_salary_advance.loan_installment_line_action').read()[0]
        action['views'] = [(self.env.ref('hr_loans_salary_advance.loan_installment_line_form_view').id, 'form')]
        action['res_id'] = self.id

        action['target'] = 'new'

        return action

    # Override create function
    def refresh_page(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    # Override write function
    def write(self, value):
        result = super(LoanInstallmentLine, self).write(value)
        # self.refresh_page()
        return result


LoanInstallmentLine()


class LoanRequestType(models.Model):
    _name = 'loan.request.type'
    _rec_name = 'name'

    name = fields.Char(translate=True)
    loan_type = fields.Selection(selection=[('fixed_amount', _('Fixed Amount')),
                                            ('percentage', _('Percentage of salary'))], default='fixed_amount')
    number_of_request = fields.Selection(selection=[('unlimited', _('unlimited')), ('once', _('Once'))],
                                         default='unlimited')
    allow_overlapping = fields.Boolean()
    factor = fields.Integer()
    percentage = fields.Float()
    amount = fields.Float()
    year = fields.Integer()

    # Relational fields
    allowance_id = fields.Many2many('hr.salary.rule')
    journal_id = fields.Many2one('account.journal')
    account_id = fields.Many2one('account.account')

    def unlink(self):
        for item in self:
            i = self.env['hr.loan.salary.advance'].search([('request_type', '=', item.id)])
            if i:
                raise exceptions.Warning(_('You can not delete record There is a related other record code %s Request Loan')% i.code)
        return super(LoanRequestType, self).unlink()





class AccountMoves(models.Model):
    _name = 'hr.account.moves'

    number = fields.Char()
    reference = fields.Char()
    date = fields.Date()
    period = fields.Char()
    amount = fields.Float()
    status = fields.Boolean()

    # relational fields
    journal = fields.Many2one(comodel_name='account.journal')
    moves_id = fields.Many2one(comodel_name='hr.loan.salary.advance')
    partner_id = fields.Many2one(comodel_name='res.partner')
    journal_move_id = fields.Many2one(comodel_name='account.move')
