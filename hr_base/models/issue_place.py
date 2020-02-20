
from odoo import models, fields, api
# issue_place
class issue_place(models.Model):
    _name = 'issued_place.issued_place'
    _rec_name = 'name'
    name = fields.Char()