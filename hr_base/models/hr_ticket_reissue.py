

from odoo import models, fields, api

class HRTicketReissue(models.Model):
    _name = 'hr.ticket.reissue'

    departure = fields.Char("Departure Air Port", required=True)
    destination = fields.Char("Destination Air Port", required=True)
    departure_date = fields.Date("Departure Date", required=True)
    return_date = fields.Date("Return Date", required=True)
    change_sec = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No'), ], default='yes', string="Change Sector", required=True)
    reasons = fields.Char("Reasons")

    reissue_ticket = fields.Many2one(comodel_name='hr.ticket')