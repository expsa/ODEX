from odoo import models, fields


class HRTicketDependent(models.Model):
    _name = 'hr.ticket.dependent'

    name = fields.Char('Name(As in Passport)')
    dob = fields.Date('Date of Birth', required=True)
    date_issue = fields.Date('Date of Issue')
    date_expiry = fields.Date('Date of Expiry')
    fn = fields.Char("First Name", )
    mn = fields.Char("Middle Name", required=True)
    ln = fields.Char("Last Name", required=True)
    ticket_req = fields.Selection(selection=[(
        'yes', 'Yes'),
        ('no', 'No'), ], default='yes', string="Ticket Required", required=True)

    departure_date = fields.Date("Departure Date", required=True)
    return_date = fields.Date("Return Date", required=True)

    # Relational fields
    nationality = fields.Many2one(comodel_name='res.country', string="Nationality")
    passport = fields.Many2one(comodel_name='hr.employee.document', string="Passport No", required=True)
    dependent_ticket = fields.Many2one(comodel_name='hr.ticket')
