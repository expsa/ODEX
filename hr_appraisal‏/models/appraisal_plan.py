from odoo import api, fields, models, _, exceptions


class AppraisalPlan(models.Model):
    _name = 'appraisal.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Appraisal plan'

    name = fields.Char()
    is_manager = fields.Boolean()
    great_level = fields.Float(compute='compute_total')

    # Relational fields
    department_id = fields.Many2one('hr.department')
    standard_appraisal_id = fields.One2many('standard.appraisal', 'standard_appraisal_line')
    manager_appraisal_id = fields.One2many('manager.appraisal', 'manager_appraisal_line')

    # Compute total field
    @api.multi
    @api.depends('is_manager', 'standard_appraisal_id', 'manager_appraisal_id')
    def compute_total(self):
        for item in self:
            item.great_level = 0.0
            if not item.is_manager:
                if item.standard_appraisal_id:
                    for line in item.standard_appraisal_id:
                        item.great_level += line.great_level
            else:
                if item.manager_appraisal_id:
                    for line in item.manager_appraisal_id:
                        item.great_level += line.great_level

    # Refresh the page
    @api.multi
    def re_compute_total(self):
        return True


# class AppraisalPlanComplete(models.Model):
#     _name = 'appraisal.plan.complete'
#     _rec_name = 'name'
#     _description = 'Appraisal plan complete'
#
#     name = fields.Char()
#
#     name = fields.Char()
#     is_manager = fields.Boolean()
#     great_level = fields.Float()
#
#     # Relational fields
#     department_id = fields.Many2one('hr.department')
#     standard_appraisal_id = fields.One2many('standard.appraisal.line', 'standard_appraisal_line')
#     manager_appraisal_id = fields.One2many('manager.appraisal.complete', 'manager_appraisal_line')
#


class StandardAppraisal(models.Model):
    _name = 'standard.appraisal'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'question'
    _description = 'Standard Appraisal'

    question = fields.Char()
    great_level = fields.Float()

    # Relational fields
    standard_appraisal_line = fields.Many2one('appraisal.plan')  # inverse field


class ManagerAppraisal(models.Model):
    _name = 'manager.appraisal'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'appraisal_name'
    _description = 'Standard Appraisal'

    appraisal_name = fields.Char()
    great_level = fields.Float(related='question_id.great_level')

    # Relational fields
    manager_appraisal_line = fields.Many2one('appraisal.plan')  # inverse field
    question_id = fields.Many2one('manager.appraisal.line')

    # Open manager appraisal
    @api.multi
    def open_manager_appraisal(self):
        for item in self:
            if item.question_id:
                action = self.env.ref('hr_appraisal‏.appraisal_action_view').read()[0]
                action['views'] = [(self.env.ref('hr_appraisal‏.appraisal_form_view').id, 'form')]
                action['res_id'] = item.question_id.id
                action['target'] = 'new'
                return action
