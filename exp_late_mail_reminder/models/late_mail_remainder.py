# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE
from odoo import models, fields, api, _


class LateEmailReminder(models.Model):
    _name = 'late.email.reminder'
    _order = 'create_date desc'

    number_of_days = fields.Integer(string='Number Of Days')
    line_ids = fields.One2many('late.email.reminder.line', 'late_email_id', string='Lines')

    @api.multi
    def execute(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def send_message(self, template=None, rec=None, model_name='', email=''):
        if not template:
            return
        if not template:
            return
        template.write({'email_to': email,
                        })
        template.with_context(lang=self.env.user.lang).send_mail(
            rec.id, force_send=True, raise_exception=False)

    def get_user_email(self, line):
        # for line in line_ids:
        user_ids = self.env['res.groups'].search([('id', 'in', line.group_ids.ids)])
        user_email = []
        for user in user_ids:
            for rec in user.users:
                user_email.append(rec.partner_id.email)
        user_email = list(set(user_email))
        emails = ''
        for email in user_email:
            emails += email + ','
        return emails

    def action_send_late_email(self):
        late_record = self.env['late.email.reminder'].search([], limit=1)
        if late_record.line_ids:
            states = ['cancel']
            for line in late_record.line_ids:
                user_email = self.get_user_email(line)
                for state in line.record_state_ids:
                    states.append(state.name)
                model_name = line.model_id.model
                record = self.env[model_name].search([('state', 'not in', states)])
                for rec in record:
                    order_date = rec.mapped(line.order_date.name)
                    last_date = ''
                    if order_date[0] != False:
                        if len(order_date[0]) > 10:
                            last_date = datetime.strptime(order_date[0], DATE_FORMAT).date()
                        else:
                            last_date = datetime.strptime(order_date[0], DATE).date()
                        end_date = last_date + timedelta(days=self.number_of_days)
                        date_now = date.today()
                        if end_date < date_now:
                            self.send_message(line.template_id, rec, model_name, user_email)


class LateEmailReminderLine(models.Model):
    _name = "late.email.reminder.line"

    model_id = fields.Many2one('ir.model', string='Model')
    order_date = fields.Many2one('ir.model.fields', string='Order Date')
    record_state_ids = fields.Many2many('late.email.state', string='States')
    template_id = fields.Many2one('mail.template', string='Template')
    late_email_id = fields.Many2one('late.email.reminder', string='Late Email')
    group_ids = fields.Many2many('res.groups', string='Groups')

    @api.onchange('model_id')
    def onchange_model_id(self):
        domain = {}
        self.order_date = False
        domain = {'order_date': [('id', 'in', self.env['ir.model.fields'].search([('model_id', '=', self.model_id.id),
                                                                                  '|', ('ttype', '=', 'date'),
                                                                                  ('ttype', '=', 'datetime')]).ids)],
                  'template_id': [('id', 'in', self.env['mail.template'].search([('model_id', '=', self.model_id.id)]).ids)]
                  }
        return {'domain': domain}


class LateEmailState(models.Model):
    _name = 'late.email.state'

    name = fields.Char(string='name of state')
