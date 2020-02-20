# -*- coding: utf-8 -*-
from odoo import models, fields,_


class HrCertification(models.Model):
    _name = 'hr.certification'
    _rec_name = 'car_name'

    car_name = fields.Char('Certification Name', required=True)
    issue_org = fields.Char('Issuing Organization', required=True)
    issue_date = fields.Date('Date of Issue')
    exp_date = fields.Date('Date of Expiry')
    regis_no = fields.Char('Registration No.')
    contact_name = fields.Char()
    contact_phn = fields.Char('Contact Phone No')
    contact_email = fields.Char()
    country_name = fields.Many2one(comodel_name='res.country')
    contract_id = fields.Many2one(comodel_name='hr.contract')

    certification_degree = fields.Selection([('weak', _('Weak')), ('good', _('Good')), ('very_good', _('Very Good')), ('excellent', _('Excellent'))])

    # relation field
    certification_specification_id = fields.Many2one(comodel_name='qualification.specification')
    certification_relation = fields.Many2one(comodel_name='hr.employee', string='Certification Relation')


HrCertification()
