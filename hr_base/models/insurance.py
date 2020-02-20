
from odoo import models, fields, api
# Insurance
class Insurance(models.Model):
    _name = 'hr.insurance'
    _rec_name = 'member_name'

    card_code = fields.Char(required=True)
    member_name = fields.Char(required=True)
    dob = fields.Date('Date of Birth', required=True)
    clas_n = fields.Char('Class')
    relation = fields.Many2one(comodel_name='hr.relation.relation')
    # sponsor_id = fields.Many2one()
    # job = fields.Char()
    premium = fields.Float()
    start_date = fields.Date()
    expiry_date = fields.Date("End Date")
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])

    insurance_relation = fields.Many2one(comodel_name='hr.employee')
