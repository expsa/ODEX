
from odoo import models, fields, api

class FamilyIqama(models.Model):
    _name = 'employee.family.iqama'
    _rec_name = 'iqama_no'

    iqama_no = fields.Char("Iqama/ID No", required=True)
    serial_no = fields.Char()
    iqama_position = fields.Char()
    place_issue = fields.Char('Place of Issue')
    issue_date = fields.Date()
    expiry_date = fields.Date(required=True)
    # date_hijri = fields.Char('Date of Expiry(Hijri)')
    arrival_date = fields.Date('Arrival Date in Suadi')
    in_saudi = fields.Boolean('Is Saudi?')
    link = fields.Many2one(comodel_name='employee.iqama')