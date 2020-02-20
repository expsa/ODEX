# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from datetime import datetime as dt

from odoo import models, fields, api, exceptions
from odoo.tools.translate import _


class CompanyDocument(models.Model):
    _name = "company.document"
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',track_visibility='always')
    datas = fields.Binary(string='Attachment')
    document_issue_date = fields.Date(sting='Issue Date', default=fields.Date.today,track_visibility='always')
    document_expire_date = fields.Date(sting='Expire Date',track_visibility='always')
    reminder_before = fields.Integer(default=0)
    active = fields.Boolean(default=True)
    attachment_filename = fields.Char()


    @api.onchange('document_issue_date', 'document_expire_date')
    def onchange_dates(self):
        if self.document_issue_date:
            if self.document_expire_date:
                document_issue_date_1 = dt.strptime(self.document_issue_date, "%Y-%m-%d")
                document_expire_date_1 = dt.strptime(self.document_expire_date, "%Y-%m-%d")
                if document_expire_date_1 < document_issue_date_1:
                    raise exceptions.Warning(
                        _('Document Expiry Date  must be greater than document Issue date'))

    @api.model
    def company_doc_mail_reminder(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.document_expire_date:
                exp_date = fields.Date.from_string(i.document_expire_date) - timedelta(days=i.reminder_before)
                if date_now >= exp_date:
                    mail_content = "  Hello ,<br>The Document ", i.name, "is going to expire on ", \
                                   str(i.document_expire_date), ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('Document-%s Expired On %s') % (i.name, i.document_expire_date),
                        'author_id': self.env.user.company_id.partner_id.id,
                        'body_html': mail_content,
                        'email_to': self.env.user.company_id.email,
                        'email_cc': self.env.user.company_id.hr_email,
                    }
                    self.env['mail.mail'].create(main_content).send()


CompanyDocument()
