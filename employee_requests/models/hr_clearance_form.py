from odoo import models, fields, api, _, exceptions
from odoo import SUPERUSER_ID


class HrClearanceForm(models.Model):
    _name = 'hr.clearance.form'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    from_hr_department = fields.Boolean()
    # employee_id = fields.Many2one(comodel_name='hr.employee')
    date = fields.Date()
    date_deliver_work = fields.Date()
    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    employee_id = fields.Many2one('hr.employee', 'Employee Id', default=lambda item: item.get_user_id())

    clearance_type = fields.Selection(selection=[("vacation", _("Vacation Clearance")),
                                                 ("final", _("Final Clearance"))])
    work_delivered = fields.Text()
    super_mg = fields.Selection(selection=[("approve", _("Approve")),
                                           ("refuse", _("Refuse"))], default='approve')
    super_refuse_cause = fields.Text(default='/')
    direct_mg = fields.Selection(selection=[("approve", _("Approve")),
                                            ("refuse", _("Refuse"))], default='approve')
    direct_refuse_cause = fields.Text(default='/')
    hr_mg = fields.Selection(selection=[("approve", _("Approve")),
                                        ("refuse", _("Refuse"))], default='approve')
    hr_refuse_cause = fields.Text(default='/')
    state = fields.Selection(selection=[("draft", _("Draft")),
                                        ("submit", _("Submitted")),
                                        ('info_system', _('IT Department')),
                                        ('admin_manager', _('Admin Affairs')),
                                        ("wait", _("Finance Approvals")),
                                        ("done", _("HR Manager")),
                                        ("refuse", _("Refuse"))], default='draft',track_visibility='always')

    @api.multi
    def draft(self):
        
        self.state = "draft"

    @api.multi
    def submit(self):
        # Check if exp_custody_petty_cash module is installed
        Module = self.env['ir.module.module'].sudo()
        modules = Module.search([('state', '=', 'installed'), ('name', '=', 'exp_custody_petty_cash')])

        if modules:
            # Check if employee has Employee Custody not in state Return done
            employee_custody = self.env['custom.employee.custody'].search(
                [('employee_id', '=', self.employee_id.id), ('state', 'in', ['submit', 'direct', 'admin', 'approve'])])
            if len(employee_custody) > 0:
                raise exceptions.Warning(
                    _(
                        'You can not Employee Clearance "%s" employee custody not in state Return Done for "%s" please reconcile it') % (
                        len(employee_custody), self.employee_id.name))

            # Check if employee has Employee Petty Cash Payment not in state Return done
            employee_petty_cash_payment = self.env['petty.cash.payment'].search(
                [('employee_id', '=', self.employee_id.id),('state', 'in', ['submit', 'direct', 'fm', 'ceo', 'accepted', 'validate'])])
            if len(employee_petty_cash_payment) > 0:
                raise exceptions.Warning(
                 _('You can not Employee Clearance "%s" employee petty cash payment not in state Return Done for "%s" please reconcile it') % (
                        len(employee_petty_cash_payment), self.employee_id.name))

        for item in self:
            mail_content = "Hello I'm", item.employee_id.name, " request to Clearance Of ", item.clearance_type,"Please approved thanks."
            main_content = {
                   'subject': _('Request clearance-%s Employee %s') % (item.clearance_type, item.employee_id.name),
                   'author_id': self.env.user.partner_id.id,
                   'body_html': mail_content,
                   'email_to': item.department_id.email_manager,
                }
            self.env['mail.mail'].create(main_content).send()
        self.state = "submit"

    @api.multi
    def info_system(self):
        self.state = "info_system"

    @api.multi
    def admin_manager(self):
        self.state = "admin_manager"

    @api.multi
    def wait(self):

        for item in self:
            termination_ids = self.env['hr.termination'].search(
                [('employee_id', '=', item.employee_id.id), ('state', 'not in', ('draft','submit','direct_manager','hr_manager'))])
            if termination_ids or item.clearance_type == 'vacation':
                self.state = "wait"
            else:
                raise exceptions.Warning(
                    _('The Clearance to be completed after the end of service of the employee approve'))

    @api.multi
    def done(self):
        self.employee_id.write({'is_calender': True})
        self.state = "done"

    @api.multi
    def refuse(self):
        self.state = "refuse"

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
        return super(HrClearanceForm, self).unlink()


HrClearanceForm()
