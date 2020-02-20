
from odoo import models, fields, api


# office
class office(models.Model):
    _name = 'office.office'
    _rec_name = 'name'
    name = fields.Char()