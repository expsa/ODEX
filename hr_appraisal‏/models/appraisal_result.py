from odoo import api, fields, models, _, exceptions


class AppraisalResult(models.Model):
    _name = 'appraisal.result'
    _rec_name = 'name'
    _description = 'Appraisal Result'

    name = fields.Char()
    result_from = fields.Float()
    result_to = fields.Float()

    # Constrains for result_from and result_to if it's value is less than zero or greater than 100
    @api.multi
    @api.constrains('result_from', 'result_to')
    def result_greed_constrains(self):
        for item in self:
            if item.result_from < 0.0 or item.result_to < 0.0:
                raise exceptions.Warning(_('Result values must be greater than zero.'))
            elif item.result_from > 100 or item.result_to > 100:
                raise exceptions.Warning(_('Result values must be less than 100.'))


class ContractAppraisal(models.Model):
    _inherit = 'hr.contract'

    # Relational fields
    appraisal_result_id = fields.Many2one('appraisal.result')


class ReContractAppraisal(models.Model):
    _inherit = 'hr.re.contract'

    # Relational fields
    evaluation_grade_id = fields.Many2one(related='employee_id.contract_id.appraisal_result_id', readonly=True)
