# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BaseAutomation(models.Model):
    _inherit = 'base.automation'

    notify_to_groups_ids = fields.Many2many(
        comodel_name='res.groups', relation='automation_notifications_to_groups_rel',
        string='TO Notify Groups')

    notify_cc_groups_ids = fields.Many2many(
        comodel_name='res.groups', relation='automation_notifications_cc_groups_rel',
        string='CC Notify Groups')

    def has_access(self, user_id, record, mode='read'):
        try:
            record.sudo(user_id).check_access_rule(mode)
            return True
        except:
            return False
        return False

    def access_users(self, groups, record):
        users = []
        for group in groups:
            for user in group.users:
                if self.has_access(user_id = user.id, record=record, mode='read'):
                    users.append(user.partner_id.email)
        return ",".join(users)

    def get_mail_to(self, record):
        users = self.access_users(self.notify_to_groups_ids, record)
        return users

    def get_mail_cc(self, record):
        users = self.access_users(self.notify_cc_groups_ids, record)
        return users


class ServerActions(models.Model):
    """ Add email option in server actions. """
    _inherit = 'ir.actions.server'

    @api.model
    def run_action_email(self, action, eval_context=None):
        # add automated actions users from groups

        if not action.template_id or not self._context.get('active_id'):
            return False

        if self._context.get('__action_done'):
            automations = self._context.get('__action_done')
            automation = list(automations.keys())[0]
            record = automations[automation]
            
            old_email_to = action.template_id.email_to
            old_email_cc = action.template_id.email_cc

            template_values = {
                'email_to': automation.get_mail_to(record),
                'email_cc': automation.get_mail_cc(record),
            }

            action.template_id.write(template_values)

            super(ServerActions, self).run_action_email(action=action, eval_context=eval_context)

            old_template_values = {
                'email_to': old_email_to,
                'email_cc': old_email_cc,
            }

            action.template_id.write(old_template_values)

            return False


        return super(ServerActions, self).run_action_email(action=action, eval_context=eval_context)


