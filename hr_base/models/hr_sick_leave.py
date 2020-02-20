from odoo import models, fields, api


class hr_sick_leave(models.Model):
    _name = 'hr.sick.leave'


    date_from = fields.Date()
    date_to = fields.Date()
    duration = fields.Integer()
    status = fields.Char()
    allocation_start_date = fields.Date()
    allocation_end_date = fields.Date()
    leave_request = fields.Char()
    sick_relation = fields.Many2one(comodel_name='hr.employee', string='sick relation')