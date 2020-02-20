
from odoo import models, fields, api



class HRExitReentry(models.Model):
    _name = 'hr.exit.reentry'

    name = fields.Many2one(comodel_name='hr.employee',string= "Employee Name", required=True)
    nationality = fields.Many2one(comodel_name='res.country', string="Nationality", required=True)
    department = fields.Many2one(comodel_name='hr.department', string="Department", required=True)
    rejoin_date = fields.Date("Rejoin Date", required=True)
    leave_date = fields.Date("Leave Date", required=True)
    leave_from = fields.Char("Leave From", required=True)
    leave_to = fields.Char("Leave To", required=True)
    govt_fee = fields.Float("Govt. Fee", required=True)
    leave_type = fields.Selection(selection=[(
        'contract', 'Contractual Leave'),
        ('emergency', 'Emergency Leave'),
        ('medical', 'Medical Leave'),
        ('others', 'Others'), ], string="Leave Type", required=True)
    months = fields.Selection(selection=[(
        '1', '1 Months'),
        ('2', '2 Months'),
        ('3', '3 Months'),
        ('4', '4 Months'),
        ('5', '5 Months'),
        ('6', '6 Months')], required=True, string='Months')
    paid_by = fields.Selection(selection=[(
        'personnel', 'personnel'),
        ('office', 'Office'), ], string="Paid By", required=True)

    stage = fields.Selection(selection=[(
        'new', 'Issue New'),
        ('wait', 'Waiting For Payment'),
        ('done', 'Done'), ], default='new')

    @api.multi
    def in_wait(self):
        self.stage = "wait"

    @api.multi
    def in_done(self):
        self.stage = "done"

    @api.multi
    def cancel(self):
        self.stage = "new"

    @api.onchange('name')
    def _onchange_employee(self):
        self.nationality = self.name.country_id
        self.department = self.name.department_id
