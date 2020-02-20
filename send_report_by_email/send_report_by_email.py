# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import models, api, _
import base64

def action_send_report(self, report_id, report_name):
    '''
    This function opens a window to compose an email, with the edi report template message loaded by default
    '''
    self.ensure_one()
    try:
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form')
    except ValueError:
        compose_form_id = False

    pdf = self.env['ir.actions.report'].search(
        [('report_name', '=', report_id),
         ('report_type', '=', 'qweb-pdf')], limit=1).render_qweb_pdf(self.id)
    b64_pdf = base64.b64encode(pdf[0])

    attachment_name = report_name
    attach_id = self.env['ir.attachment'].create({
         'name': attachment_name + '.pdf',
         'type': 'binary',
         'datas': b64_pdf,
         'datas_fname': attachment_name + '.pdf',
         'store_fname': attachment_name + '.pdf',
         'mimetype': 'application/x-pdf'
    })

    user = self.env['res.users'].browse(self._uid)
    ctx = dict(self.env.context or {})
    ctx.update({
        'default_model': self._name,
        'default_res_id': self.id,
        'default_auto_delete': True,
        'default_email_from': user.email,
        'default_subject': attachment_name,
        'default_body': _("""
<p>Dear ,</p>
<p>
Here is, in attachment, a <strong>%s</strong> Report.

</p>

<p>Best regards,</p>

<p style="color:#888888;">
%s
</p>"""%(attachment_name,user.signature)),
        'default_composition_mode': 'comment',
        'force_email': True,
        'default_attachment_ids':[(6, 0, [attach_id.id])]
    })
    return {
        'name': _('Compose Email'),
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(compose_form_id.id, 'form')],
        'view_id': compose_form_id.id,
        'target': 'new',
        'context': ctx,
    }


class MailComposer(models.TransientModel):

    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        result = super(MailComposer, self).default_get(fields)
        result['subject'] = self._context.get('default_subject', result.get('subject'))
        return result
