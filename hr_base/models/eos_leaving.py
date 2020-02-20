from odoo import models, fields, api
# Employee Leaving
class EOSLeaving(models.Model):
    _name = 'eos.leaving'
    _rec_name = 'employee'

    employee = fields.Many2one(comodel_name='hr.employee', required=True)
    employee_code = fields.Char()
    department = fields.Char()
    office = fields.Char()
    reason = fields.Char(required=True)
    requested_date = fields.Date()
    notice_date = fields.Date('Notice Start Date')
    end_date = fields.Date('Notice End Date')
    interview_date = fields.Date('Exit Interview Date')
    contact_person = fields.Char('GOSI No')
    description = fields.Char()
    employee_clearence_ref = fields.Many2one(comodel_name='employee.clearance', string="Employee Clearence Ref", readonly=True)

    @api.onchange('employee')
    def onchange_employee(self):
        if self.employee:
            self.employee_code = self.employee.employee_code
            self.department = self.employee.department_id.name
            self.office = self.employee.office.name
            # self.contact_person = self.employee.gosi_no.gosi_no

    @api.multi
    def create_emp_clearence(self):
        clearence_recs = self.env['employee.clearance'].search([])
        if self.employee_clearence_ref.id == 0:
            new = clearence_recs.create({'employee': self.employee.id})
            self.employee_clearence_ref = new
            self.employee_clearence_ref.employee_code = self.employee_code
            self.employee_clearence_ref.department = self.department
            self.employee_clearence_ref.office = self.office
            self.employee_clearence_ref.email = self.employee.work_email
            self.employee_clearence_ref.contact_phone = self.employee.work_phone

        else:
            self.employee_clearence_ref.employee = self.employee.id
            self.employee_clearence_ref.employee_code = self.employee_code
            self.employee_clearence_ref.department = self.department
            self.employee_clearence_ref.office = self.office
            self.employee_clearence_ref.email = self.employee.work_email
            self.employee_clearence_ref.contact_phone = self.employee.work_phone

