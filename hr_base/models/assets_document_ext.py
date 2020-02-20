# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetsDocumentExt(models.Model):
    _inherit = 'maintenance.equipment'

    documents_id = fields.One2many('document.asset', 'documents_relation', string="Documents")
    make = fields.Char("Make")
    owner_user_id = fields.Many2one(comodel_name='hr.employee')

    model = fields.Char("Model")
    color = fields.Char("Color")
    plate_no = fields.Char("Plate No")
    door_no = fields.Char("Door No")
    chassis_no = fields.Char("Chassis No")
    reg_no = fields.Char("Registration No")
    ownership = fields.Selection(selection=[(
        'own', 'Owned'),
        ('leas', 'Leased')], default='own', string='Ownership')

    sponsor_id = fields.Many2one(comodel_name='res.sponsor', string="Sponsor")
    sponsor = fields.Char(string="Sponsor Name")
    location = fields.Char("Location")
    p_price = fields.Char("Purchase Price")
    i_value = fields.Char("Insured Value")
    sponsor_lease_id = fields.Many2one(comodel_name='res.sponsor', string="Sponsor ID")
    c_name = fields.Many2one(comodel_name='res.company', string="Company Name")
    cr_no = fields.Char("Insured Value")
    lease_expiry = fields.Date(string="Lease Expiry")
    remark = fields.Char("Remarks")

    @api.onchange('sponsor_id')
    def _onchange_s_name(self):
        self.sponsor = self.sponsor_id.name


AssetsDocumentExt()
