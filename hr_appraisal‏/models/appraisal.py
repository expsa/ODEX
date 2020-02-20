from odoo import api, fields, models, _, exceptions


class Appraisal(models.Model):
    _name = 'hr.employee.appraisal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'
    _description = 'Appraisal'

    date_from = fields.Date()
    date_to = fields.Date()
    great_level = fields.Float()
    level_achieved = fields.Float()
    level_achieved_percentage = fields.Float(track_visibility='always')
    appraisal_date = fields.Date()
    is_manager = fields.Boolean(related='appraisal_plan_id.is_manager')
    state = fields.Selection([
        ("draft", _("Draft")), ("state_done", _("Done")), ("closed", _("Closed"))
    ], default='draft',track_visibility='always')
    start_compute = fields.Char(
        compute='fill_employee_or_manager_appraisal')  # Invisible filed to call compute function

    # Relational fields
    employee_appraisal = fields.Many2one('hr.group.employee.appraisal')  # Inverse field
    employee_id = fields.Many2one('hr.employee')
    appraisal_plan_id = fields.Many2one('appraisal.plan')  # to store the main appraisal
    # appraisal_plan_complete_id = fields.Many2one('appraisal.plan.complete')
    standard_appraisal_employee_line_ids = fields.One2many('standard.appraisal.line',
                                                           'standard_appraisal_employee_line')
    manager_appraisal_line_id = fields.One2many('manager.appraisal.complete', 'manager_appraisal_line_for_employee')
    appraisal_result = fields.Many2one('appraisal.result',track_visibility='always')

    # Fill Employee appraisal or manager appraisal
    @api.multi
    @api.depends('appraisal_plan_id')
    def fill_employee_or_manager_appraisal(self):
        for item in self:

            # Initialize values
            standard_appraisal_list = []
            manager_appraisal_list = []

            if item.appraisal_plan_id:
                if not item.appraisal_plan_id.is_manager:

                    # Fill standard_appraisal_employee_line_ids to complete
                    for line in item.appraisal_plan_id.standard_appraisal_id:
                        standard_appraisal_list.append({
                            'great_level': line.great_level,
                            'question': line.question
                        })
                    item.standard_appraisal_employee_line_ids = [(0, 0, value) for value in standard_appraisal_list]

                else:
                    # Fill manager_appraisal_line_id to complete
                    for line in item.appraisal_plan_id.manager_appraisal_id:
                        complete_manager_appraisal_list = []

                        for record in line.question_id.customize_appraisal_id:
                            complete_manager_appraisal_list.append({
                                'question': record.question,
                                'great_degree_level': record.great_degree_level,
                                'degree_id': record.degree_id.id
                            })

                        manager_appraisal_list.append({
                            'appraisal_name': line.appraisal_name,
                            'question_id': line.question_id.id,
                            'question_complete_id': self.env['manager.appraisal.complete.line'].create({
                                'name': line.question_id.name,
                                'customize_appraisal_id': [(0, 0, value) for value in complete_manager_appraisal_list]

                            }).id
                        })
                    item.manager_appraisal_line_id = [(0, 0, value) for value in manager_appraisal_list]

                    # Compute total and great level for every line in manager appraisal
                    # compute great level from all lines
                    great_achieved = 0.0
                    for element in item.manager_appraisal_line_id:
                        great_level = 0.0
                        total = 0.0

                        for line in element.question_complete_id.customize_appraisal_id:
                            great_level += line.great_degree_level
                            total += line.greed

                        element.question_complete_id.great_level = great_level
                        element.question_complete_id.total = total

                        # compute great level from all line
                        great_achieved += element.great_level
                    item.great_level = great_achieved

    # Update level achieved values when changed in lines
    # Update level achieved percentage when changed in lines
    # Determine which appraisal result from appraisal percentage
    @api.onchange('standard_appraisal_employee_line_ids', 'appraisal_plan_id')
    def onchange_appraisal_lines(self):
        for item in self:
            # Initialize
            total_greed, total_great_level, item.level_achieved, item.great_level, item.level_achieved_percentage = 0.0, 0.0, 0.0, 0.0, 0.0
            appraisal_result_list = []

            if not item.is_manager:
                for line in item.standard_appraisal_employee_line_ids:
                    # Update level achieved values when changed in lines
                    total_greed += line.greed
                    total_great_level += line.great_level
                item.great_level = total_great_level
                item.level_achieved = total_greed

                # Update level achieved percentage when changed in lines
                if item.level_achieved > 0.0 and item.great_level > 0.0:
                    item.level_achieved_percentage = (item.level_achieved * 100) / item.great_level

                if item.level_achieved_percentage > 100:
                    raise exceptions.Warning(
                        _('There is No percentage result for employee appraisal Greater than 100%'))
                # Determine which appraisal result from appraisal percentage
                appraisal_result = self.env['appraisal.result'].search([
                    ('result_from', '<=', item.level_achieved_percentage),
                    ('result_to', '>', item.level_achieved_percentage)])
                if len(appraisal_result) > 1:
                    for line in appraisal_result:
                        appraisal_result_list.append(line.name)
                    raise exceptions.Warning(
                        _('Please check appraisal result configuration , there is more than result for percentage %s  are %s ') % (
                        round(item.level_achieved_percentage, 2), appraisal_result_list))
                else:
                    item.appraisal_result = appraisal_result.id

    @api.onchange('manager_appraisal_line_id', 'appraisal_plan_id')
    def onchange_manager_appraisal_line_id(self):
        for item in self:
            # Initialize
            total_greed, total_great_level, item.level_achieved, item.great_level, item.level_achieved_percentage = 0.0, 0.0, 0.0, 0.0, 0.0
            appraisal_result_list = []

            if item.is_manager:
                for line in item.manager_appraisal_line_id:
                    # Update level achieved values when changed in lines
                    total_greed += line.total
                    total_great_level += line.great_level
                item.great_level = total_great_level
                item.level_achieved = total_greed

                # Update level achieved percentage when changed in lines
                if item.level_achieved > 0.0 and item.great_level > 0.0:
                    item.level_achieved_percentage = (item.level_achieved * 100) / item.great_level

                if item.level_achieved_percentage > 100:
                    raise exceptions.Warning(
                        _('There is No percentage result for employee appraisal Greater than 100%'))
                # Determine which appraisal result from appraisal percentage
                appraisal_result = self.env['appraisal.result'].search([
                    ('result_from', '<=', item.level_achieved_percentage),
                    ('result_to', '>', item.level_achieved_percentage)])

                if len(appraisal_result) > 1:
                    for line in appraisal_result:
                        appraisal_result_list.append(line.name)
                    raise exceptions.Warning(
                        _('Please check appraisal result configuration , there is more than result for percentage %s  are %s ') % (
                        round(item.level_achieved_percentage, 2), appraisal_result_list))
                else:
                    item.appraisal_result = appraisal_result.id

    # Recompute function
    @api.multi
    def recompute_values_level_achieved(self):
        if not self.is_manager:
            self.onchange_appraisal_lines()
        else:
            self.onchange_manager_appraisal_line_id()

    @api.multi
    def draft(self): 
        for item in self:
            if item.employee_appraisal.state not in ('draft','gen_appraisal','start_appraisal'):
               raise exceptions.Warning(_('You can not Re-draft when there is appraisal not in state draft for employees.'))
    
            if item.employee_id.contract_id.appraisal_result_id:
                item.employee_id.contract_id.appraisal_result_id = False
        self.state = 'draft'

    @api.multi
    def set_state_done(self):
        for item in self:

            # Update appraisal result in contract
            if item.employee_id.contract_id:
                if item.appraisal_result:
                    item.employee_id.contract_id.appraisal_result_id = item.appraisal_result
            else:
                raise exceptions.Warning(
                    _('There is no contract for employee "%s" to update appraisal result ') % item.employee_id.name)
            item.state = 'state_done'

    @api.multi
    def closed(self):
        self.state = 'closed'

    # Override unlink function
    def unlink(self):
        for item in self:
            if item.state != 'draft':
                raise exceptions.Warning(
                    _('You can not delete record in state not in draft for employee "%s" ') % item.employee_id.name)
        return super(Appraisal, self).unlink()


class StandardAppraisalLines(models.Model):
    _name = 'standard.appraisal.line'
    _rec_name = 'greed'
    _description = 'Standard Appraisal line'

    greed = fields.Float()
    question = fields.Char()
    great_level = fields.Float()

    # Relational fields
    standard_appraisal_employee_line = fields.Many2one('hr.employee.appraisal')  # inverse field

    @api.constrains('greed', 'great_level')
    def greed_constrains(self):
        for item in self:
            if item.greed > item.great_level:
                raise exceptions.Warning(_('You Cannot The Greed Greater Than Great Level'))


class ManagerAppraisalLines(models.Model):
    _name = 'manager.appraisal.complete'

    appraisal_name = fields.Char()
    great_level = fields.Float(related='question_complete_id.great_level')
    total = fields.Float(related='question_complete_id.total')

    # Relational fields
    question_id = fields.Many2one('manager.appraisal.line')
    question_complete_id = fields.Many2one('manager.appraisal.complete.line', domain="[('id','in',[])]")
    manager_appraisal_line_for_employee = fields.Many2one('hr.employee.appraisal')  # inverse field

    # Open manager appraisal
    @api.multi
    def open_manager_appraisal(self):
        for item in self:
            if item.question_complete_id:
                action = self.env.ref('hr_appraisal‏.manager_appraisal_complete_line_action').read()[0]
                action['views'] = [(self.env.ref('hr_appraisal‏.manager_appraisal_complete_line_form_view').id, 'form')]
                action['res_id'] = item.question_complete_id.id
                action['target'] = 'new'
                return action


class ManagerAppraisalCompleteLines(models.Model):
    _name = 'manager.appraisal.complete.line'

    name = fields.Char()
    total = fields.Float()
    great_level = fields.Float()

    # Relational fields
    customize_appraisal_id = fields.One2many('customize.complete.appraisal', 'customize_appraisal_line_id')

    @api.multi
    @api.onchange('customize_appraisal_id')
    def compute_tatal_and_greate_level(self):
        # Initialize variables
        total, great_level, self.total, self.great_level = 0.0, 0.0, 0.0, 0.0

        for line in self.customize_appraisal_id:
            great_level += line.great_degree_level
            total += line.greed
        self.great_level = great_level
        self.total = total


class CustomizeAppraisal(models.Model):
    _name = 'customize.complete.appraisal'
    _rec_name = 'question'
    _description = 'Customize complete Appraisal'

    question = fields.Char()
    greed = fields.Float(related='degree_id.greed')
    great_degree_level = fields.Float(related='degree_id.great_degree_level')

    # Relational fields
    customize_appraisal_line_id = fields.Many2one('manager.appraisal.complete.line')  # Inverse Field
    degree_id = fields.Many2one('appraisal.degree')
