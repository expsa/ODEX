# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Degreemedical(models.Model):
    _name = "degree.medical.issuance"

    # degree_medical_insurance
    name = fields.Char(translate=True)
    company_insurance = fields.Char()


Degreemedical()


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # unique employee number to employee work information page
    employee_number = fields.Char()

    # passport fields to private information page
    date_issuance_passport = fields.Date()
    expiration_date_passport = fields.Date()
    place_issuance_passport = fields.Char()
    own_license = fields.Boolean()

    # Accommodation and medical insurance page
    ###Residence
    residency_number = fields.Char()
    date_issuance_residence = fields.Date()
    expiration_date_residence = fields.Date()
    place_issuance_residence = fields.Char()
    first_entry_into_saudi_arabia = fields.Date()
    number_of_visa = fields.Integer()
    ###Guaranty
    on_company_guarantee = fields.Boolean(default=True)
    validity_transfer_sponsorship = fields.Date()
    ###Medical Insurance
    medical_insurance = fields.Boolean(default=True)
    degree_medical_insurance = fields.Many2one('degree.medical.issuance')
    # degree_medical_insurance = fields.Selection(
    #    selection=[("vip", _("VIP")), ("a", _("A")), ("b", _("B")), ("c", _("C"))])
    medical_insurance_number = fields.Char()
    date_of_expiry = fields.Date(related='copy_examination_file.expiry_date', readonly=True)
    copy_examination_file = fields.Many2one('hr.employee.document',
                                            domain=[('document_type', '=', 'medical_Examination')])
    filename = fields.Char()
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('complete', 'Complete Data'), ('open', _('Create Contract')),
                   ('out_of_service', _('Out of service'))],
        default="draft")

    # Educational qualification page
    educational_qualification = fields.Char()
    education_country = fields.Many2one(comodel_name='res.country')
    specialization = fields.Char()
    organization = fields.Char()
    education_date = fields.Date()

    # Payment method
    payment_method = fields.Selection(selection=[("cash", _("Cash")), ("bank", _("Bank"))])
    date_of_employment = fields.Date()
    length_of_service = fields.Integer()
    check_nationality = fields.Boolean(compute='_check_nationality_type')

    @api.constrains('employee_number')
    def unique_field_name_constrains(self):
        for item in self:
            items = self.search([('employee_number', '=', item.employee_number)])
            if len(items) > 1:  # return more than one item with the same value
                raise ValidationError(_('You cannot create Employee with the same employee number'))

    @api.depends('country_id')
    def _check_nationality_type(self):
        for item in self:
            if item.country_id.code == 'SA':
                item.check_nationality = True

            else:
                item.check_nationality = False


HrEmployee()
