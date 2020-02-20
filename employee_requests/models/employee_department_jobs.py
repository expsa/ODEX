from odoo import api, fields, models, _


class EmployeeDepartmentJobs(models.Model):
    _name = 'employee.department.jobs'
    _rec_name = 'employee_id'
    _description = 'Employee Department and Jobs'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date()
    comment = fields.Text()
    state = fields.Selection(selection=[('draft', _('Draft')), ('confirm', _('Confirm')), ('approved', _('Approved'))],
                             default='draft',track_visibility='always')
    promotion_type = fields.Selection(
        selection=[('department', _('Department')), ('job', _('Job')), ('both', _('Both'))],track_visibility='always')

    # relational fields
    employee_id = fields.Many2one(comodel_name="hr.employee",track_visibility='always')
    old_department_id = fields.Many2one(comodel_name='hr.department', related='employee_id.department_id')
    old_department_2_id = fields.Many2one(comodel_name='hr.department')
    old_job_id = fields.Many2one(comodel_name='hr.job', related='employee_id.job_id')
    old_job_2_id = fields.Many2one(comodel_name='hr.job')
    new_department_id = fields.Many2one(comodel_name='hr.department')
    new_job_id = fields.Many2one(comodel_name='hr.job')

    # store department and job
    @api.onchange('employee_id')
    def store_level_group_and_degree_values(self):
        self.old_department_2_id = self.old_department_id
        self.old_job_2_id = self.old_job_id

    def confirm(self):
        self.state = 'confirm'

    def approved(self):
        for item in self:
            if item.promotion_type == 'department':
                if item.new_department_id:
                    item.employee_id.write({
                        'department_id': item.new_department_id.id
                    })
            elif item.promotion_type == 'job':
                if item.new_job_id:
                    item.employee_id.write({
                        'job_id': item.new_job_id.id
                    })
            elif item.promotion_type == 'both':
                if item.new_job_id and item.new_department_id:
                    item.employee_id.write({
                        'department_id': item.new_department_id.id,
                        'job_id': item.new_job_id.id
                    })

        self.state = 'approved'

    def draft(self):
        for item in self:
            if item.promotion_type == 'department':
                if item.new_department_id:
                    item.employee_id.write({
                        'department_id': item.old_department_2_id.id
                    })
            elif item.promotion_type == 'job':
                if item.new_job_id:
                    item.employee_id.write({
                        'job_id': item.old_job_2_id.id
                    })
            elif item.promotion_type == 'both':
                if item.new_job_id and item.new_department_id:
                    item.employee_id.write({
                        'department_id': item.old_department_2_id.id,
                        'job_id': item.old_job_2_id.id
                    })

        self.state = 'draft'
