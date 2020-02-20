from odoo import api, fields, models, _


class ManagerAppraisalLine(models.Model):
    _name = 'manager.appraisal.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Standard Appraisal'

    name = fields.Char()
    great_level = fields.Float()

    # Relational fields
    customize_appraisal_id = fields.One2many('customize.appraisal', 'customize_appraisal_line_id')

    # Compute total degree from
    @api.onchange('customize_appraisal_id')
    def calculate_total_degrees(self):
        for item in self:
            item.great_level = 0.0
            if item.customize_appraisal_id:
                for line in item.customize_appraisal_id:
                    item.great_level += line.great_degree_level


class CustomizeAppraisal(models.Model):
    _name = 'customize.appraisal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'question'
    _description = 'Customize Appraisal'

    question = fields.Char()
    great_degree_level = fields.Float(related='degree_id.great_degree_level')

    # Relational fields
    customize_appraisal_line_id = fields.Many2one('manager.appraisal.line')  # Inverse Field
    degree_id = fields.Many2one('appraisal.degree')


class AppraisalDegree(models.Model):
    _name = 'appraisal.degree'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Appraisal Degree'

    name = fields.Char()
    great_degree_level = fields.Float()
    greed = fields.Float()
