# -*- coding: utf-8 -*-
import datetime
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class renew_official_paper_line(models.Model):
    _name = 'hr.official.paper.line'

    official_paper_line = fields.Many2one(comodel_name='hr.renew.official.paper')

    employee_id = fields.Many2one(comodel_name='hr.employee')
    department = fields.Many2one(comodel_name='hr.department')
    job_id = fields.Many2one(comodel_name='hr.job')
    job_no = fields.Integer()
    nationality = fields.Many2one(comodel_name='res.country')
    document_type = fields.Selection(
        [('passport', _('Passport')), ('license', _('License')), ('Iqama', _('Iqama')), ('saudi', _('Saudi ID')),
         ('medical_Examination', _('medical Examination')), ('other', _('Other'))])
    expire_date = fields.Date()
