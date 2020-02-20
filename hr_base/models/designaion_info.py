# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DesignationInfo(models.Model):
    _name = 'designation.info'
    _rec_name = 'job'

    company_name = fields.Many2one(comodel_name='res.company', string="Company Name", required=True)
    branch_name = fields.Many2one(comodel_name='res.company', string="Branch Name")
    division = fields.Many2one(comodel_name='division.info', string="Division")
    department = fields.Many2one(comodel_name='department.info', string="Department")
    category_id = fields.Many2one(comodel_name='category.info', string="Category Info")
    job = fields.Char("Job Title", required=True)
    profession = fields.Char("ID Profession", required=True)
