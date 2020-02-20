
from odoo import models, fields, api
# EmployeeCard
class EmployeeCard(models.Model):
    _name = 'employee.card'
    _rec_name = 'employee'

    employee = fields.Many2one(comodel_name='hr.employee', required=True)
    employee_code = fields.Char(string='Employee Code')
    department = fields.Many2one(comodel_name='hr.department')
    job_title = fields.Many2one(comodel_name='designation.info', string='Job Title')
    office = fields.Char()
    card_type = fields.Selection(selection=[(
        'Acces Card', 'Access Card'),
        ('Business Card', 'Business Card'),
        ('Id Card', 'Id Card')], required=True, string='Card Type')
    card_no = fields.Char(string='Card No.')
    requested_date = fields.Char(string='Requesed Date')
    reason = fields.Char()
    status = fields.Char()
    access_type = fields.Char(string='Access Type')
    period_stay = fields.Date(string='Period of Stay')
    issue_date = fields.Date(string='Issue Date')
    expiry_date = fields.Date(string='Expiry Date')

    @api.onchange('employee')
    def onchange_date_id(self):
        if self.employee:
            self.employee_code = self.employee.employee_code
            self.job_title = self.employee.job_id.name
            self.department = self.employee.department_id
            self.office = self.employee.office.name
