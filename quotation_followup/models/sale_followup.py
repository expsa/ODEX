# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import Warning


class MailFollowUpType(models.Model):
    _inherit = 'mail.activity.type'

    un_remove_able = fields.Boolean(string='System Valid', default=False)

    @api.multi
    def unlink(self):
        if self.un_remove_able:
            raise Warning(_('Can not remove server property'))
        return super(MailFollowUpType, self).unlink()

    @api.multi
    def write(self, vals):
        if vals.get('un_remove_able'):
            vals.pop('un_remove_able')
        return super(MailFollowUpType, self).write(vals)


MailFollowUpType()


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    un_remove_able = fields.Boolean(string='System Valid', default=False, related='activity_type_id.un_remove_able')

    @api.multi
    def write(self, vals):
        if vals.get('un_remove_able'):
            vals.pop('un_remove_able')
        return super(MailActivity, self).write(vals)

    @api.multi
    def close_and_create_new(self):
        activity_type = self.env.ref('quotation_followup.mail_activity_follow_quota')
        note = self.note
        order = self.env[self.res_model].browse(self.res_id)
        new_activity = self.env['mail.activity'].create({
            'summary': 'Snoozing Follow up the quota',
            'date_deadline': self.date_deadline,
            'un_remove_able': True,
            'activity_type_id': activity_type.id,
            'user_id': self.env.user.id,
            'res_model_id': self.env.ref('sale.model_sale_order').id,
            'res_id': order.id,
        })
        new_activity.action_feedback(feedback=note)
        activity_type.sudo().write({'un_remove_able': True})


MailActivity()


class Followup(models.Model):
    _name = 'sale.quote.followup'
    _description = 'Sale Follow-up'
    _rec_name = 'name'

    followup_line = fields.One2many(
        'sale.followup.line',
        'followup_id',
        'Follow-up',
        copy=True
    )
    name = fields.Char(
        string="Name",
        readonly=True
    )


Followup()


class FollowupLine(models.Model):
    _name = 'sale.followup.line'
    name = fields.Char(
        string='Follow-Up Action',
        required=True
    )
    sequence = fields.Integer(
        string='Sequence',
        help="Gives the sequence order when displaying a list of follow-up lines."
    )
    delay = fields.Integer(
        string='Due Days',
        help="The number of days after the create of the \
           quotation to wait before sending the reminder. \
           Could be negative if you want to send a polite alert beforehand.",
        required=True
    )
    followup_id = fields.Many2one(
        'account_followup.followup',
        string='Follow Ups',
        required=True,
    )
    send_activity = fields.Boolean()
    send_popup = fields.Boolean()

    sale_followup_type = fields.Selection(selection=[('budget', 'Budget'),
                                                     ('undirected_tender', 'Undirected Tender'),
                                                     ('directed_tender', 'Directed Tender'),
                                                     ('project', 'Project')], string='Sale Followup', required=True)


FollowupLine()
