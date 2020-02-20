
from odoo import models, fields, api
# Employee Clearance
class EmployeeClearance(models.Model):
    _name = 'employee.clearance'
    _rec_name = 'employee'

    employee = fields.Many2one(comodel_name='hr.employee', required=True)
    employee_code = fields.Char()
    department = fields.Many2one(comodel_name='hr.department')
    office = fields.Char()
    email = fields.Char()
    contact_phone = fields.Char()
    seniority_date = fields.Date()
    res_date = fields.Date(string='Resignation/Term Date')
    last_country_day = fields.Date()
    last_day_work = fields.Date(string='Last Day of Work')
    letter_to_client = fields.Char()

    it_department = fields.One2many(comodel_name='it.department', inverse_name='department_relation')

    @api.onchange('employee')
    def onchange_employee(self):
        if self.employee:
            self.employee_code = self.employee.employee_code
            self.department = self.employee.department_id.id
            self.office = self.employee.office.name
            self.email = self.employee.work_email
            self.contact_phone = self.employee.work_phone

class ItDepartment(models.Model):
    _name = 'it.department'
    _rec_name = 'item'

    item = fields.Char()
    status = fields.Char()
    handled_by = fields.Char()
    remarks = fields.Char()

    department_relation = fields.Many2one(comodel_name='employee.clearance')