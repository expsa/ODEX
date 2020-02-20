from calendar import monthrange
import time
from datetime import datetime
from odoo import SUPERUSER_ID
from odoo import models, fields, api, _, exceptions
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta


class HrPersonalPermission(models.Model):
    _name = 'hr.personal.permission'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    from_hr_department = fields.Boolean()
    date = fields.Date()
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    duration = fields.Float(compute='get_duration_no')
    employee_contract_id = fields.Many2one(comodel_name='hr.contract.type')
    balance = fields.Integer(related='employee_id.contract_id.working_hours.permission_hours')

    permission_number = fields.Integer(force_save=True, readonly=True, store=True)
    early_exit = fields.Boolean()
    mission_purpose = fields.Text()

    employee_no = fields.Char(related='employee_id.emp_no', readonly=True)
    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    refuse_cause = fields.Text()
    attach_ids = fields.One2many('ir.attachment', 'personal_permission_id')
    approved_by = fields.Many2one(comodel_name='res.users')
    refused_by = fields.Many2one(comodel_name='res.users')
    employee_id = fields.Many2one('hr.employee', 'Employee Id', default=lambda item: item.get_user_id())



    state = fields.Selection(
        [('draft', _('Draft')), ('send', _('Send')), ('direct_manager', _('Direct Manager')),
         ('approve', _('approve'))
            , ('refused', _('Refused'))], default="draft",track_visibility='always')

    @api.one
    @api.depends('date_from', 'date_to')
    def get_duration_no(self):
        for item in self:
            if item.date_from and item.date_to:
                start_date_value = datetime.strptime(item.date_from, "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(item.date_to, "%Y-%m-%d %H:%M:%S")
                if start_date_value <= end_date:
                    days = (end_date - start_date_value).days
                    seconds_diff = (end_date - start_date_value).seconds
                    item.duration = (days * 24) + seconds_diff / 3600
                else:
                    raise exceptions.Warning(_('End Date must be greater than Start Date'))

    @api.multi
    @api.onchange('date_to', 'date_from', 'employee_id')
    def permission_number_decrement(self):
        for item in self:
            if item.date_to:
                current_date = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT)
                current_month = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT).month
                date_from = current_date.strftime('%Y-{0}-01'.format(current_month))
                date_to = current_date.strftime('%Y-{0}-01'.format(current_month + 1))
                if current_month==12:
                   date_to = current_date.strftime('%Y-{0}-31'.format(current_month))
                number_of_per = item.employee_id.contract_id.working_hours.permission_number
                employee_permissions = self.search([
                    ('employee_id', '=', item.employee_id.id),
                    ('state', '=', 'approve'),
                    ('date_from', '>=', date_from),
                    ('date_to', '<=', date_to)])
                if number_of_per - len(employee_permissions) > 0:
                    item.permission_number = number_of_per - len(employee_permissions)
                else:
                    raise exceptions.Warning(_('Sorry You Have Used All Your Permission In This Month'))
                if employee_permissions.date_to and item.date_to:
                    permission_date1 = datetime.strptime(employee_permissions.date_to,
                                                         DEFAULT_SERVER_DATETIME_FORMAT).date()
                    date_to_value1 = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT).date()

                    if permission_date1 == date_to_value1:
                        raise exceptions.Warning(
                            _('Sorry You Have Used All Your Permission In This Day you have one permission per a Day'))

    @api.multi
    @api.constrains('date_from', 'date_to')
    def _get_date_constrains(self):
        for item in self:
            current_month = (datetime.utcnow() + timedelta(hours=3)).date().month
            current_year = (datetime.utcnow() + timedelta(hours=3)).date().year
            month_len = monthrange(current_year, current_month)[1]
            number_of_per = item.employee_id.contract_id.working_hours.permission_number
            number_of_durations = item.employee_id.contract_id.working_hours.permission_hours
            this_month_permission = self.search([('employee_id', '=', item.employee_id.id), ('state', '=', 'approve'),
                                                 ('date_from', '>=', time.strftime('%Y-{0}-1'.format(current_month))),
                                                 ('date_to', '<=',
                                                  time.strftime('%Y-{0}-{1}'.format(current_month, month_len)))])
            if item.date_to:
                current_date = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT)
                current_month = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT).month
                date_from = current_date.strftime('%Y-{0}-01'.format(current_month))
                date_to = current_date.strftime('%Y-{0}-01'.format(current_month + 1))
                if current_month==12:
                   date_to = current_date.strftime('%Y-{0}-31'.format(current_month))
                employee_permissions = self.search([
                    ('employee_id', '=', item.employee_id.id),
                    ('state', '=', 'approve'),
                    ('date_from', '>=', date_from),
                    ('date_to', '<=', date_to)])

            if number_of_per - len(employee_permissions) <= 0:
                raise exceptions.Warning(_('Sorry You Have Used All Your Permission In This Month'))
            start_date_value = datetime.strptime(item.date_from, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(item.date_to, "%Y-%m-%d %H:%M:%S")
            if start_date_value <= end_date:
                days = (end_date - start_date_value).days
                seconds_diff = (end_date - start_date_value).seconds
                item.duration = (days * 24) + seconds_diff / 3600
                if item.duration > item.balance or item.duration <= 0.0:
                    raise exceptions.Warning(
                        _('This Duration not Allowed it must be Less Than or  equal to Balance And Not Equal Zero'))
                if employee_permissions.date_to and item.date_to:
                    permission_date = datetime.strptime(employee_permissions.date_to,
                                                        DEFAULT_SERVER_DATETIME_FORMAT).date()
                    date_to_value = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT).date()

                    if permission_date == date_to_value:
                        raise exceptions.Warning(
                            _('Sorry You Have Used All Your Permission In This Day you have one permission per a Day'))

    @api.multi
    def draft_state(self):
        self.state = "draft"

    @api.multi
    def send(self):
        for item in self:
            mail_content = "Hello I'm", item.employee_id.name, " request to Permission Hours= ", item.duration,"Please approved thanks."
            main_content = {
                   'subject': _('Request Permission Hours %s Employee %s') % (item.duration, item.employee_id.name),
                   'author_id': self.env.user.partner_id.id,
                   'body_html': mail_content,
                   'email_to': item.department_id.email_manager,
                }
            self.env['mail.mail'].create(main_content).send()
        self.state = "send"

    @api.multi
    def direct_manager(self):
        self.state = "direct_manager"

    @api.multi
    def approve(self):
        self.state = "approve"

    @api.multi
    def refused(self):
        self.state = "refused"

    @api.multi
    def get_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False

   
    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(HrPersonalPermission, self).unlink()

    # @api.model
    # def create(self,vals):
    #     new_record = super(HrPersonalPermission, self).create(vals)
    #     for item in new_record:
    #         last_permission=self.search([('employee_id', '=', item.employee_id.id), ('state', '=', 'approve')],order='date_to desc',limit=1)
    #         if last_permission:
    #             this_month_permissions=self.search([('employee_id', '=', item.employee_id.id), ('state', '=', 'approve')])
    #             last_month=datetime.strptime(last_permission.date_to,DEFAULT_SERVER_DATETIME_FORMAT).month
    #             current_month=datetime.now().month
    #             current_month_permission=self.search([('employee_id', '=', item.employee_id.id), ('state', '=', 'approve'),
    #                                                   ('date_from','>=',datetime.strftime('%Y-{0}-1'.format(current_month))),
    #                                                   ('date_to', '>=',
    #                                                    datetime.strftime('%Y-{0}-30'.format(current_month)))])
    #             if current_month> last_month:
    #
    #         employee_permissions = self.search([('employee_id', '=', item.employee_id.id), ('state', '=', 'approve')])
    #         if item.employee_id.contract_id.type_id.permission_number - len(employee_permissions) > 0:
    #             item.permission_number = item.employee_id.contract_id.type_id.permission_number - len(employee_permissions)
    #             start_date_value = datetime.strptime(item.date_from, "%Y-%m-%d %H:%M:%S")
    #             end_date = datetime.strptime(item.date_to, "%Y-%m-%d %H:%M:%S")
    #             if start_date_value <= end_date:
    #                 days = (end_date - start_date_value).days
    #                 seconds_diff = (end_date - start_date_value).seconds
    #                 item.duration = (days * 24) + seconds_diff / 3600
    #                 if item.duration > item.balance or item.duration <= 0.0:
    #                     raise exceptions.Warning(_('This Duration not Allowed it must be Less Than or  equal to Balance And Not Equal Zero'))
    #         else:
    #             raise exceptions.Warning(_('Sorry You Have Used All Your Permission In This Month'))
    #
    #
    #
    #     return new_record


HrPersonalPermission()


class HrPersonalPermissionAttach(models.Model):
    _inherit = 'ir.attachment'

    personal_permission_id = fields.Many2one(comodel_name='hr.personal.permission')
