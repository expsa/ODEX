from odoo import models, fields, api, _, exceptions
from datetime import datetime as dt


class EmployeeIqamaRenew(models.Model):
    _name = 'employee.iqama.renewal'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(readonly=True)
    date = fields.Date()
    line_ids = fields.One2many('employee.iqama.renewal.line', 'line_id')
    x_description = fields.Char()


    @api.model
    def create(self, vals):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        seq = self.env['ir.sequence'].get('employee.iqama.renewal')
        vals['name'] = seq + "/" + employee_id.name
        return super(EmployeeIqamaRenew, self).create(vals)

    state = fields.Selection(
        [('draft', _('Draft')), ('submit', _('Submit')), ('hr_depart', _('Hr')),
         ('effective_department', _('Effective_Department')), ('chief_accountant', _('Chief Accountant')),('refused', _('Refused'))],
        default="draft",track_visibility='always')


    @api.multi
    def draft_state(self):
        for item in self:
            for record in item.line_ids:
               if self.state == 'chief_accountant':
                 if record.move_id :
                   if record.move_id.state == 'draft':
                      #record.move_id.state ='canceled'
                      record.move_id.unlink()
                      item.state = "draft"
                      item.line_ids.state = "draft"
                      record.employee_id.iqama_number.write({
                          'expiry_date':record.iqama_expir_date
                      })
                   else:
                      raise exceptions.Warning(_('You can not cancel account move "%s" in state not draft') % record.move_id.name)
                 if record.move_id2 :
                   if record.move_id2.state == 'draft':
                      #record.move_id2.state ='canceled'
                      record.move_id2.unlink()
                      item.state = "draft"
                      item.line_ids.state = "draft"
                      record.employee_id.iqama_number.write({
                          'expiry_date':record.iqama_expir_date
                      })
                   else:
                      raise exceptions.Warning(_('You can not cancel account move "%s" in state not draft') % record.move_id.name)
               else:
                  item.state = 'draft'
                  record.state = "draft"


    @api.multi
    def submit(self):

        for item in self:
           for record in item.line_ids:
               if record.iqama_new_expiry == False:
                   raise exceptions.Warning( _('Sorry You must enter New Iqama expiry'))
               item.state = "submit"
               record.state = "submit"

    @api.multi
    def hr_depart(self):
        for item in self:
           for record in item.line_ids:
              item.state = "hr_depart"
              record.state = "hr_depart"

    @api.multi
    def effective_department(self):
        for item in self:
           for record in item.line_ids:
             item.state = "effective_department"
             record.state = "effective_department"


    @api.multi
    def chief_accountant(self):

        for item in self:

           for record in item.line_ids:
             if record.state == 'effective_department':
                if record.account_id.id == False or record.journal_id.id == False:
                   raise exceptions.Warning( _('To Transfer the entry you must enter the account and journal'))
                
                #### journal renewal_fees
                debit_line_vals = {
                    'name': record.employee_id.name,
                    'debit': record.renewal_fees,
                    'account_id': record.account_id.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }
                credit_line_vals = {
                    'name': record.employee_id.name,
                    'credit': record.renewal_fees,
                    'account_id': record.journal_id.default_credit_account_id.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }

                move = record.env['account.move'].create({
                    'state': 'draft',
                    'journal_id': record.journal_id.id,
                    'date': item.date,
                    'ref': record.employee_id.name,
                    'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                })

                record.move_id = move.id

                #### journal work_premint_fees
                debit_line_vals = {
                    'name': record.employee_id.name,
                    'debit': record.work_premint_fees,
                    'account_id': record.account_id2.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }
                credit_line_vals = {
                    'name': record.employee_id.name,
                    'credit': record.work_premint_fees,
                    'account_id': record.journal_id.default_credit_account_id.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }

                move = record.env['account.move'].create({
                    'state': 'draft',
                    'journal_id': record.journal_id.id,
                    'date': item.date,
                    'ref': record.employee_id.name,
                    'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                })
                record.move_id2 = move.id

                record.employee_id.iqama_number.write({'expiry_date': record.iqama_new_expiry})

           record.state = "chief_accountant"
           item.state = "chief_accountant"

    '''@api.multi
    def general_manager(self):
        for item in self:
            for record in item.line_ids:
                #### journal renewal_fees
                debit_line_vals = {
                    'name': record.employee_id.name,
                    'debit': record.renewal_fees,
                    'account_id': record.account_id.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }
                credit_line_vals = {
                    'name': record.employee_id.name,
                    'credit': record.renewal_fees,
                    'account_id': record.journal_id.default_credit_account_id.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }

                move = record.env['account.move'].create({
                    'state': 'draft',
                    'journal_id': record.journal_id.id,
                    'date': item.date,
                    'ref': record.employee_id.name,
                    'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                })

                record.move_id = move.id

                #### journal work_premint_fees
                debit_line_vals = {
                    'name': record.employee_id.name,
                    'debit': record.work_premint_fees,
                    'account_id': record.account_id2.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }
                credit_line_vals = {
                    'name': record.employee_id.name,
                    'credit': record.work_premint_fees,
                    'account_id': record.journal_id.default_credit_account_id.id,
                    'partner_id': record.employee_id.user_id.partner_id.id
                }

                move = record.env['account.move'].create({
                    'state': 'draft',
                    'journal_id': record.journal_id.id,
                    'date': item.date,
                    'ref': record.employee_id.name,
                    'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                })
                record.move_id2 = move.id

                record.employee_id.iqama_number.write({'expiry_date': record.iqama_new_expiry})

            item.state = "general_manager"
            item.line_ids.state = "general_manager"  '''
            

    @api.multi
    def refused(self):
        for item in self:
           for record in item.line_ids:
              item.state = "refused"
              record.state = "refused"

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(EmployeeIqamaRenew, self).unlink()

    def b_search(self):

        emp_obj = self.env['hr.employee'].search([('iqama_expiy_date', '<=', self.date),('state','=','open')])

        self.line_ids.unlink()
        vals = []
        for emp in emp_obj:
            vals.append((0, False, {'employee_id': emp.id}))

        self.write({'line_ids': vals})


class EmployeeIqamaRenewLine(models.Model):
    _name = 'employee.iqama.renewal.line'

    document_id = fields.Many2one('hr.employee.document', domain=[('document_type', '=', 'Iqama')])

    employee_id = fields.Many2one(comodel_name='hr.employee',required=True)
    iqama_no = fields.Many2one(related='employee_id.iqama_number', readonly=True)
    iqama_expir_date = fields.Date(related='employee_id.iqama_expiy_date',force_save=True, readonly=True)
    #iqama_expir_date = fields.Date(force_save=True, readonly=True, compute='get_iqama_expir_date')
    work_premit_sedad_no = fields.Char()
    renewal_fees = fields.Float(required=True, default=0)
    work_premint_fees = fields.Float(required=True, default=0)
    total = fields.Float(readonly=True, compute='get_total_fees')
    line_id = fields.Many2one(comodel_name='employee.iqama.renewal')

    iqama_new_expiry = fields.Date()
    account_id = fields.Many2one('account.account')
    account_id2 = fields.Many2one('account.account')
    journal_id = fields.Many2one('account.journal')
    move_id = fields.Many2one('account.move', string='Move Renewal')
    move_id2 = fields.Many2one('account.move', string='Move Work')

    state = fields.Selection(
        [('draft', _('Draft')), ('submit', _('Submit')), ('hr_depart', _('HR Department')),
         ('effective_department', _('Effective_Department')), ('chief_accountant', _('Chief Accountant')),
         ('refused', _('Refused'))],
        default="draft",readonly=True)


    @api.onchange('employee_id')
    def _get_iqama_expiry(self):
        for item in self:
            item.iqama_expir_date = item.employee_id.iqama_expiy_date

    @api.depends('work_premint_fees', 'renewal_fees')
    @api.multi
    def get_total_fees(self):
        for rec in self:
            rec.total_fees = rec.renewal_fees + rec.work_premint_fees
            rec.total = rec.total_fees

    @api.onchange('iqama_expir_date', 'iqama_new_expiry')
    def onchange_dates(self):
        if self.iqama_new_expiry:
            if self.iqama_expir_date:
                expiry_date_1 = dt.strptime(self.iqama_expir_date, "%Y-%m-%d")
                new_expiry_date_1 = dt.strptime(self.iqama_new_expiry, "%Y-%m-%d")
                if expiry_date_1 > new_expiry_date_1:
                    raise exceptions.Warning(
                        _('New Iqama Expiry Date  must be greater than old expiry Date'))

EmployeeIqamaRenewLine()
