# -*- coding: utf-8 -*-
from odoo import models, fields, api

import datetime


class EmployeeDependent(models.Model):
    _name = 'hr.employee.dependent'

    name = fields.Char()
    age = fields.Integer(string='Age', force_save=1,compute='_compute_age')
    birthday = fields.Date(string='Birthday')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], default="male")
    relation = fields.Selection(selection=[('wife', 'Wife'), ('child', 'child')])
    nationality = fields.Many2one(comodel_name='res.country')
    passport_no = fields.Char()
    passport_issue_date = fields.Date(string='Passport Issue Date')
    passport_expire_date = fields.Date(string='Passport Expire Date')
    remarks = fields.Text(string='Remarks')
    contract_id = fields.Many2one(comodel_name='hr.contract')
    degree_medical_insu = fields.Char(string='Degree Medical Insurance')
    medical_insurance_num = fields.Char(string='Medical Insurance Number')
    identity_num = fields.Char(string='Identity Number')

    @api.onchange('birthday')
    def _compute_age(self):
        today = datetime.date.today()
        format_str = '%Y-%m-%d'  # The format
        for item in self:
          if item.birthday:
              birthday = datetime.datetime.strptime(item.birthday, format_str)
              age = today.year - birthday.year
              if today.month < birthday.month or today.month == birthday.month and today.day < birthday.day:
                 age -= 1
              item.age = age

# EmployeeDependent()
