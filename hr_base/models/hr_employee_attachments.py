from odoo import models, fields


class HrEmployeeAttachment(models.Model):
    _name = 'hr.employee.attachments'
    _rec_name = 'name'
    name = fields.Char()
    file_name = fields.Binary()
    employee_id = fields.Many2one(comodel_name='hr.employee')


HrEmployeeAttachment()
