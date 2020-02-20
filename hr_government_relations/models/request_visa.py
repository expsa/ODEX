from odoo import models, fields, _ , api,exceptions
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta
from datetime import datetime
from pprint import pprint
from odoo import SUPERUSER_ID

class hr_request_visa(models.Model):
    _name = "hr.request.visa"
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    date = fields.Date()
    state = fields.Selection(selection=[
        ("draft", "Draft"),
        ("send", "Direct Manager"),
        ("confirm", "Government Relations"),
        ("done", "HR Approve"),
        ("refuse", "Refuse")
    ], default='draft',track_visibility='always')
    religion = fields.Selection(selection=[('muslim', 'Muslim'), ('christian', 'Christian'), ('other', 'Other')], default="muslim")
    from_hr = fields.Boolean()
    onece = fields.Boolean()
    multi = fields.Boolean()
    passport = fields.Char()
    passport_date = fields.Date()
    birth_date = fields.Date()
    nationality_id = fields.Many2one(comodel_name='res.country')
    working = fields.Char()
    activity = fields.Char()
    job = fields.Char()
    work_from = fields.Char()
    note = fields.Text()

    employee_id = fields.Many2one('hr.employee', default=lambda item: item.get_user_id())
    department_id = fields.Many2one('hr.department',related='employee_id.department_id')
    one = fields.Boolean(string='15')
    tow = fields.Boolean(string='30')
    three = fields.Boolean(string='90')
    four = fields.Boolean(string='180')
    five = fields.Boolean(string='365')
    sex = fields.Boolean(string='1825')

    
    attach_ids = fields.One2many('ir.attachment', 'attach_ids_exit_return')
    
    cost = fields.Float()
    account_move_id = fields.Many2one(comodel_name='account.move')
    account_journal_id = fields.Many2one(comodel_name='account.journal')
    account_debit_id = fields.Many2one(comodel_name='account.account')
    def send(self):
        self.state = 'send'

    def draft(self):
        # check if the moved journal entry if un posted then delete
        for item in self:
            if item.account_move_id:
                if item.account_move_id.state == 'draft':
                    item.account_move_id.state = 'canceled'
                    item.account_move_id = False
                    self.state = 'draft'
                else:
                    raise exceptions.Warning(_(
                        'You can not re-draft Exit and return because account move with ID "%s" in state Posted') % item.account_move_id.id)
            else:
                self.state = 'draft'


    def hr_manager(self):
        self.state = 'confirm'

    def financial_manager(self):
        for item in self:
            if  item.cost > 0:
                debit_line_vals = {
                    'name': 'debit',
                    'debit': item.cost,
                    'account_id': item.account_debit_id.id,
                    'partner_id': item.employee_id.user_id.partner_id.id
                }
                credit_line_vals = {
                    'name': 'credit',
                    'credit': item.cost,
                    'account_id': item.account_journal_id.default_credit_account_id.id,
                    'partner_id': item.employee_id.user_id.partner_id.id
                }
                move_id = self.env['account.move'].create({
                    'state': 'draft',
                    'journal_id': item.account_journal_id.id,
                    'date': date.today(),
                    'ref': 'Exit and Return',
                    'line_ids': [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
                })
                self.account_move_id = move_id.id

        self.state = 'done'

    def refuse(self):
        self.state = 'refuse'






    # overrite unlink function
    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(hr_exit_return, self).unlink()


    #overrite create function
  
    @api.multi
    def get_user_id(self):
        employee_id=self.env['hr.employee'].search([('user_id','=',self.env.uid)],limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False



class hr_exit_return_attach(models.Model):
    _inherit = "ir.attachment"

    # inverse field to hr.exit.return
    attach_ids_exit_return = fields.Many2one(comodel_name='hr.exit.return')

