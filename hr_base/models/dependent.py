from odoo import models, fields, api

class Dependent(models.Model):
    _name = 'hr.dependent'
    _rec_name = 'name'
    d_gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", required=True)
    d_passport = fields.Many2one(comodel_name='hr.employee.document',string= "Passport No", required=True)
    name = fields.Char('Name(As in Passport)', required="True")
    employee = fields.Char()
    arabic_name = fields.Char()
    dob = fields.Date('Date of Birth', required=True)
    date_issue = fields.Date('Date of Issue')
    date_expiry = fields.Date('Date of Expiry')
    nationality = fields.Many2one(comodel_name='res.country',string= "Nationality")
    relation = fields.Many2one(comodel_name='hr.relation.relation')
    religion = fields.Many2one(comodel_name='hr.religion.religion')
    iqama_num = fields.Char('Iqama Number')
    issue_place = fields.Many2one(comodel_name='issued_place.issued_place')
    fn = fields.Char("First Name", )
    mn = fields.Char("Middle Name", )
    ln = fields.Char("Last Name", )
    dependent_relation = fields.Many2one(comodel_name='hr.employee')

    @api.onchange('name')
    def _onchange_name(self):
        self.employee = self.dependent_relation.name