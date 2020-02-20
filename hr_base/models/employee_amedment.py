
from odoo import models, fields, api

# Employee Amedment
class Employee_Amedment(models.Model):
    _name = 'contract.amedment'
    _rec_name = 'employee'

    employee = fields.Many2one(comodel_name='hr.employee', required=True)
    employee_code = fields.Char("Employee Code", required=True)
    contract = fields.Many2one(comodel_name='hr.contract', required=True)
    effective_date = fields.Date()
    office = fields.Many2one(comodel_name='office.office', required=True)
    department = fields.Many2one(comodel_name='hr.department', required=True)
    grade = fields.Char()
    job = fields.Many2one(comodel_name='designation.info', string="Designation", required=True)
    to_office = fields.Many2one(comodel_name='office.office', string="To Office", required=True)
    to_department = fields.Many2one(comodel_name='hr.department', string="To Department", required=True)
    to_grade = fields.Char("To Grade")
    to_job = fields.Many2one(comodel_name='designation.info', string="To Designation", required=True)

    c_location = fields.Many2one(comodel_name='res.partner', string="Current Location", required=True)
    mol_location = fields.Char("MOL Location", required=True)
    r_manager = fields.Many2one(comodel_name='hr.employee', string="Reporting Manager", required=True)

    n_location = fields.Many2one(comodel_name='res.partner', string="New Location", required=True)
    nmol_location = fields.Char("MOL Location", required=True)
    nr_manager = fields.Many2one(comodel_name='hr.employee', string="Reporting Manager", required=True)
    remark = fields.Char("Remarks")

    @api.onchange('employee')
    def onchange_employee(self):
        if self.employee:
            self.office = self.env['office.office'].search([('name', '=', self.employee.office.name)])
            self.grade = self.employee.grade
            self.employee_code = self.employee.employee_code
            self.contract = self.env['hr.contract'].search([('name', '=', self.employee.name)])
            self.department = self.env['hr.department'].search([('name', '=', self.employee.department_id.name)])
            self.grade = self.employee.grade
            self.mol_location = self.employee.mol_location
            self.c_location = self.employee.address_id
            self.r_manager = self.employee.performence_manager.id

            self.to_department = self.to_office = self.to_grade = self.to_job = self.c_location = self.mol_location = ''

    @api.multi
    def validate_changes(self):
        self.employee.department_id = self.to_department.id
        self.employee.office = self.to_office.id
        self.employee.grade = self.to_grade
        self.nmol_location = self.mol_location
        self.n_location = self.c_location
        self.nr_manager = self.r_manager