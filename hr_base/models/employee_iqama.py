from odoo import models, fields, api

# Employee Iqama
class Iqama(models.Model):
    _name = 'employee.iqama'
    _rec_name = 'iqama_no'

    employee = fields.Many2one(comodel_name='hr.employee')
    employee_code = fields.Char()
    office = fields.Char()
    department = fields.Char()
    job = fields.Char('Job Position')
    name = fields.Char('Name(As in Passport)')
    arabic_name = fields.Char()
    nationality = fields.Char()
    relegion = fields.Char('Religion')
    dob = fields.Date('Date of Birth')

    serial_no = fields.Char()

    in_saudi = fields.Boolean('Is Saudi?')

    iqama_no = fields.Char("Iqama/ID No", required=True)
    iqama_position = fields.Char()
    place_issue = fields.Char('Place of Issue')
    issue_date = fields.Date(required=True)
    expiry_date = fields.Date(required=True)
    arrival_date = fields.Date('Arrival Date in Suadi')
    description = fields.Text()


    t_link = fields.One2many('employee.family.iqama', 'link', string="Family Iqama/ID Details")

    @api.onchange('employee')
    def onchange_employee(self):
        if self.employee:
            self.employee_code = self.employee.employee_code
            self.job = self.employee.job_id.name
            self.name = self.employee.name_as_pass
            self.arabic_name = self.employee.arabic_name
            self.department = self.employee.department_id.name
            self.office = self.employee.office.name
            self.dob = self.employee.birthday
            self.relegion = self.employee.religion
            self.serial_no = self.employee.serial_num
            self.name = self.employee.name_as_pass
            self.iqama_no = self.employee.iqama_num.id
            self.arabic_name = self.employee.arabic_name
            self.nationality = self.employee.country_id.name
            self.issue_date = self.employee.iqama_num.issue_date
            self.expiry_date = self.employee.iqama_num.expiry_date
