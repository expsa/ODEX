from odoo import models, fields, api


# EOS
class EOS(models.Model):
    _name = 'employee.eos'
    _rec_name = 'employee'

    employee = fields.Many2one(comodel_name='hr.employee', required=True)
    department = fields.Char()
    job = fields.Char()
    contract = fields.Char()
    joining_date = fields.Date('Joining Date')
    leaving_date = fields.Date()
    employee_code = fields.Char()
    currency = fields.Char()
    year = fields.Char()
    date = fields.Date()
    type_d = fields.Char('Type')
    payslip = fields.Char()
    remaining_leave = fields.Float()
    no_year = fields.Char('No of Years')
    no_month = fields.Char('No of Months')
    no_days = fields.Char('No of Days')
    total_award = fields.Float()
    leave_balance = fields.Float()
    salary = fields.Float('Salary of Current Month')
    others = fields.Float()
    total_amount = fields.Float()

    @api.onchange('employee')
    def onchange_employee(self):
        if self.employee:
            self.department = self.employee.department_id.name
            self.contract = self.employee.work_phone
            self.joining_date = self.employee.joining_date
            self.leaving_date = self.employee.leaving_date
            self.employee_code = self.employee.employee_code

