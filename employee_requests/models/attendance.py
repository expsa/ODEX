from odoo import models, fields, api, _


class Transactions(models.Model):
    _inherit = 'hr.attendance.transaction'

    personal_permission_id = fields.Many2one('hr.personal.permission', string='Permission Request')
    approve_personal_permission = fields.Boolean(string='Permission')
    total_permission_hours = fields.Float()
