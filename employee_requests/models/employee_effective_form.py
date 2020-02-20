from odoo import models, fields, api, _, exceptions
from odoo import SUPERUSER_ID


class EmployeeEffectiveForm(models.Model):
    _name = 'employee.effective.form'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    from_hr = fields.Boolean()
    contract_id = fields.Many2one('hr.contract')

    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    employee_salary = fields.Float(related='employee_id.contract_id.salary', readonly=True)
    employee_house_all = fields.Float(related='employee_id.contract_id.house_allowance_temp', readonly=True)
    total_salary = fields.Float(related='employee_id.contract_id.total_allowance', readonly=True)
    remarks = fields.Text()
    employee_id = fields.Many2one('hr.employee', 'Employee Id', default=lambda item: item.get_user_id())

    effective_form_type = fields.Selection(
        [('first_tim_job', _('First Time Job')), ('return_from_leave', _('Return From Leave'))])
    effective_form_date = fields.Date(track_visibility='always')

    state = fields.Selection(
        [('draft', _('Draft')), ('submit', _('Submit')), ('direct_manager', _('Direct Manager')),
         ('hr_manager', _('Hr_manager')), ('done', _('Done')),
         ('refused', _('Refused'))],
        default="draft",track_visibility='always')

    @api.depends('employee_salary', 'employee_house_all', 'employee_transport_all', 'employee_communication_all')
    def _calculate_toal_salary(self):
        for item in self:
            item.total_salary = item.employee_salary + item.employee_communication_all + item.employee_house_all + item.employee_transport_all

    @api.multi
    def draft_state(self):
        self.state = "draft"

    @api.multi
    def submit(self):
        for item in self:
            mail_content = "Hello I'm", item.employee_id.name, " request Need to ", item.effective_form_type,"Please approved thanks."
            main_content = {
                   'subject': _('Request Effective-%s Employee %s') % (item.effective_form_type, item.employee_id.name),
                   'author_id': self.env.user.partner_id.id,
                   'body_html': mail_content,
                   'email_to': item.department_id.email_manager,
                }
            self.env['mail.mail'].create(main_content).send()

        self.state = "submit"

    @api.multi
    def direct_manager(self):
        self.state = "direct_manager"

    @api.multi
    def hr_manager(self):
        self.state = "hr_manager"

    @api.multi
    def done(self):
        self.state = "done"

        for item in self:
            if item.effective_form_type == 'first_tim_job':
                item.employee_id.sudo().write({'first_hiring_date': item.effective_form_date})
            else:
                return False

    @api.multi
    def refused(self):
        self.state = "refused"

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(EmployeeEffectiveForm, self).unlink()

    @api.multi
    def get_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False


    # #onchange effective date 16/1/2019
    #
    # @api.onchange('effective_form_date')
    # def first_hiring_dat_chang(self):
    #     if self.state == 'done':
    #         self.employee_id.first_hiring_date = self.effective_form_date
