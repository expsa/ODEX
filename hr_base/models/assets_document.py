# -*- coding: utf-8 -*-

from odoo import models, fields


class AssetsDocument(models.Model):
    _name = 'document.asset'

    name = fields.Char(string="Doc Name", required=True)
    doc_no = fields.Char(string="Doc No")
    doc_type = fields.Many2one(comodel_name='documents.typed', string="Doc Type")
    renew_date = fields.Date(string="Renewed Date")
    expire_date = fields.Date(string="Expiry Date", required=True)
    no_of_days = fields.Integer(string="No Of Days", required=True)
    due_renew_days = fields.Integer(string="Due for Renewal", required=True)
    alert_to = fields.Char(string="Alert To")
    attach_file = fields.Binary(string="Attach File")
    remark = fields.Char(string="Remarks")
    documents_relation = fields.Many2one(comodel_name='maintenance.equipment', string='Equipment')


AssetsDocument()


class DocumentType(models.Model):
    _name = 'documents.typed'
    _rec_name = 'name'
    name = fields.Char(string='Type Name', required=True)
