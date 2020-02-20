from odoo import models, fields, api, _, exceptions
from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
from odoo import SUPERUSER_ID


class HouseAllowanceAdvance(models.Model):
    _name = 'house.allowance.advance'
    _rec_name = 'employee_id'

    from_hr_department = fields.Boolean()
    amount = fields.Float()
    date = fields.Date()
    start_date = fields.Date()
    duration = fields.Float(compute='get_Days_no')
    state = fields.Selection(
        [('draft', _('Draft')), ('send', _('Send')), ('hr_special_Approval', _('HR Specialist Approval')),
         ('hr_manager_approved', _('HR Manager Approved')),
         ('financial_manager', _('Financial Manager Approval')),
         ('approve_manager', _('Approve Manager')), ('refused', _('Refused'))],
        default="draft")

    @api.multi
    @api.depends('start_date', 'date')
    def get_Days_no(self):
        for item in self:
            if item.start_date and item.date:
                start_date_value = datetime.strptime(item.start_date, "%Y-%m-%d")
                end_date = datetime.strptime(item.date, "%Y-%m-%d")
                if start_date_value > end_date:
                    raise exceptions.Warning(_('End Date must be greater than Start Date'))
                elif start_date_value < end_date:
                    days = (end_date - start_date_value).days
                    item.duration = days
                else:
                    item.duration = 0.0

    # relational fields
    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    contract_id = fields.Many2one(comodel_name='hr.contract')
    account_move_id = fields.Many2one(comodel_name='hr.account.moves', string='Move')
    house_allowance_advance_line_ids = fields.One2many('house.allowance.advance.line', 'amount_id')
    employee_id = fields.Many2one('hr.employee', 'Employee Id', default=lambda item: item.get_user_id())

    @api.multi
    def draft_state(self):
        self.state = "draft"

    @api.multi
    def send(self):
        self.state = "send"

    @api.multi
    def hr_special_Approval(self):
        self.state = "hr_special_Approval"

    @api.multi
    def financial_manager(self):
        self.state = "financial_manager"

    @api.multi
    def hr_manager_approved(self):
        self.state = "hr_manager_approved"

    @api.multi
    def approve_manager(self):
        self.state = "approve_manager"

    @api.multi
    def refused(self):
        self.state = "refused"

    @api.multi
    def get_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False

   

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(HouseAllowanceAdvance, self).unlink()


class HouseAllowanceAdvanceLine(models.Model):
    _name = 'house.allowance.advance.line'

    date = fields.Date()

    # relational fields
    amount_id = fields.Many2one(comodel_name='house.allowance.advance', string='Amount')
