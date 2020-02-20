# -*- coding: utf-8 -*-

from odoo import models, fields, _, exceptions, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class hr_extend(models.Model):
    _name = 'hr.re.contract'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread']

    state = fields.Selection(string='State', selection=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('direct_manager', 'Direct Manager'),
        ('hr_manager', 'HR Manager'),
        ('finance_manager', 'Finance Manager'),
        ('gm_manager', 'General Manager'),
        ('done', 'Re - Contract("Done")'),
        ('refuse', 'Refuse'),
    ], default='draft',track_visibility='always')
    next_state = fields.Selection(string='Next Required Approval', selection=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('direct_manager', 'Direct Manager'),
        ('hr_manager', 'HR Manager'),
        ('finance_manager', 'Finance Manager'),
        ('gm_manager', 'General Manager'),
        ('done', 'Re - Contract("Done")'),
        ('refuse', 'Refuse'),
    ], default='draft')

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    validators_user_ids = fields.Many2one('hr.employee')
    date = fields.Date(default=fields.Date.context_today)
    effective_date = fields.Date()
    job_id = fields.Many2one('hr.job', string='Job Position', compute='_get_employee_data', store=True)
    department_id = fields.Many2one('hr.department', string='Department', compute='_get_employee_data', store=True)

    hire_date = fields.Date(string='Hire Date', compute='_get_employee_data', store=True)
    contract_id = fields.Many2one('hr.contract', compute='_get_employee_data', store=True, string='Current Contract',
                                  help='Latest contract of the employee')
    direct_mg = fields.Selection([
        ('approve', 'Approve'),
        ('refuse', 'Refuse')],
        string='Direct Manager Approvals')
    direct_refuse_cause = fields.Char(string='Direct Manager Refusal Cause')

    hr_mg = fields.Selection([
        ('approve', 'Approve'),
        ('refuse', 'Refuse')],
        string='HR Manager Approvals')
    hr_refuse_cause = fields.Char(string='HR Manager Refusal Cause')

    finance_mg = fields.Selection([
        ('approve', 'Approve'),
        ('refuse', 'Refuse')],
        string='Financial Manager Approvals')
    finance_refuse_cause = fields.Char(string='Financial Manager Refusal Cause')

    gm_mg = fields.Selection([
        ('approve', 'Approve'),
        ('refuse', 'Refuse')],
        string='General Manager Approvals')
    gm_refuse_cause = fields.Char(string='General Manager Refusal Cause')
    new_salary = fields.Float()
    is_direct_manager = fields.Boolean(string='Is Direct Manager', compute='_compute_is_direct_manager')
    refused = fields.Boolean(string='refused', compute='_compute_refuse')
    start_date = fields.Date(string='Current Contract Start Date', compute='_get_employee_data', store=True)
    new_contract_start_date = fields.Date()
    new_contract_end_date = fields.Date()
    eoc_date = fields.Date(string='Current Contract End Date', compute='_get_employee_data', store=True)
    increase_salary = fields.Selection([('no', 'NO'), ('yes', 'YES')], string='Increase Salary?', default='no')
    attach_ids = fields.One2many('ir.attachment', compute='_compute_attachment_ids', string="Last Appraisal",
                                 help="Attachment that don't come from message.")

    def _compute_attachment_ids(self):
        for task in self:
            attachment_ids = self.env['ir.attachment'].search(
                [('res_id', '=', task.id), ('res_model', '=', 'project.task')]).ids
            message_attachment_ids = task.mapped('message_ids.attachment_ids').ids  # from mail_thread
            task.attachment_ids = list(set(attachment_ids) - set(message_attachment_ids))

    def _compute_refuse(self):
        if self.direct_mg == 'refuse' and self.state == 'gm_manager':
            self.refused = True
        if self.hr_mg == 'refuse' and self.state == 'gm_manager':
            self.refused = True
        if self.gm_mg == 'refuse' and self.state == 'gm_manager':
            self.refused = True
        if self.finance_mg == 'refuse' and self.state == 'gm_manager':
            self.refused = True

    def action_refuse(self):
        for item in self:
            if item.state == 'done':
               contracts = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)], order='id DESC')[:2]
               item.contract_id.write({
                         'salary': item.contract_id.salary_degree.base_salary,
                         'salary_scale': item.contract_id.salary_scale.id,
                         'salary_level': item.contract_id.salary_level.id,
                         'salary_group': item.contract_id.salary_group.id,
                         'salary_degree': item.contract_id.salary_degree.id,})
        self.state = "refuse"

    def _compute_is_direct_manager(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self._uid)], limit=1).id
        if employee_id:
            if self.employee_id and self.employee_id.parent_id.id == employee_id and self.state == 'submit':
                self.is_direct_manager = True
            else:
                self.is_direct_manager = False
        else:
            self.is_direct_manager = False

    def action_submit(self):
        self.state = 'submitted'

    def action_direct_manager(self):
        if self.employee_id.parent_id and self._uid != self.employee_id.parent_id.user_id.id:
            raise exceptions.Warning(_('This is Not Your Role'))
        self.state = "direct_manager"

    def action_hr_manager(self):
        self.state = "hr_manager"

    def action_finance_manager(self):
        self.state = "finance_manager"

    def action_gm_manager(self):
        self.state = "gm_manager"

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(hr_extend, self).unlink()

    @api.onchange('new_contract_start_date')
    def onchange_new_contract_start_date(self):
        if self.new_contract_start_date:
            start_date = datetime.strptime(self.new_contract_start_date, DEFAULT_SERVER_DATE_FORMAT).date()
            end_date = start_date + relativedelta(years=1)
            end_date -= relativedelta(days=1)
            self.new_contract_end_date = end_date

    def _check_contract(self):

        old_start_date = datetime.strptime(self.contract_id.date_start, DEFAULT_SERVER_DATE_FORMAT).date()
        old_end_date = datetime.strptime(self.contract_id.date_end, DEFAULT_SERVER_DATE_FORMAT).date()
        new_start_date = datetime.strptime(self.new_contract_start_date, DEFAULT_SERVER_DATE_FORMAT).date()
        new_end_date = datetime.strptime(self.new_contract_end_date, DEFAULT_SERVER_DATE_FORMAT).date()
        if new_start_date <= old_end_date:
            raise exceptions.Warning(_('New Contract must have start date after the end date of old contract'))
        elif old_start_date <= new_start_date <= old_end_date:
            raise exceptions.Warning(_('New Contract must have start date after the end date of old contract'))
        elif new_start_date >= new_end_date:
            raise exceptions.Warning(_('New Contract start date must be before the end date'))

        return True

    def _check_refuse(self):
        if self.direct_mg == 'refuse':
            raise exceptions.Warning(_('Please Before Confirming, Direct Manager Refuses Request'))
        if self.hr_mg == 'refuse':
            raise exceptions.Warning(_('Please Before Confirming, HR Manager Refuses Request'))
        if self.gm_mg == 'refuse':
            raise exceptions.Warning(_('Please Before Confirming, General Manager Refuses Request'))
        if self.finance_mg == 'refuse':
            raise exceptions.Warning(_('Please Before Confirming, Financial Manager Refuses Request'))

    @api.multi
    def action_done(self):
        self._check_contract()
        self._check_refuse()
        today = datetime.now().date()
        str_today = today.strftime('%Y-%m-%d')
        if str_today != self.effective_date:
            raise exceptions.Warning(_('You can not re-contract employee because effective date is not today'))

        default = {
            'job_id': self.job_id.id,
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'date_start': self.new_contract_start_date,
            'date_end': self.new_contract_end_date,
            'name': 'Re-Contract' + self.employee_id.name,
        }
        if self.increase_salary == 'yes':

            default.update({'wage': self.new_salary_degree.base_salary,
                            'salary_scale': self.new_salary_scale.id,
                            'salary_level': self.new_salary_level.id,
                            # 'experience_year': self.experience_year,
                            'salary_group': self.new_salary_group.id,
                            'salary_degree': self.new_salary_degree.id,
                            })

        else:
            default.update({'wage': self.contract_id.salary_degree.base_salary,
                            'salary_scale': self.contract_id.salary_scale.id,
                            'salary_level': self.contract_id.salary_level.id,
                            'experience_year': self.contract_id.experience_year,
                            'salary_group': self.contract_id.salary_group.id,
                            'salary_degree': self.contract_id.salary_degree.id,
                            })

        c_id = self.contract_id.copy(default=default)

        for line in self.contract_id.employee_dependant:
            line.contract_id = c_id.id
        self.contract_id.write({'active': False})

        # Employee back to service
        self.employee_id.state = 'open'
        self.contract_id.state = 'program_directory'

        self.state = "done"

    def action_set_to_draft(self):
        if self.state == 'done':
            contracts = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)], order='id DESC')[:2]
            if contracts[0].active:
                contracts[0].write({'active': False})
                contracts[1].write({'active': True})
            elif contracts[1].active:
                contracts[1].write({'active': False})
                contracts[0].write({'active': True})
        self.state = "draft"
