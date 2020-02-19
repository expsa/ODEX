# -*- coding: utf-8 -*-

from odoo import api,fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    name = fields.Char(index=True,translate=True)
    fax_no=fields.Char(string='Fax No')
    arabic_address = fields.Char(string="Arabic Address")
    @api.multi
    @api.constrains('email', 'zip')
    def _check_email(self):
        for partner in self:
            if partner.is_company:
                domain = [
                    ('id', '!=', partner.id),
                    ('email', '=', partner.email),
                    ('email', '!=', False),
                    ('zip', '!=', False),
                    ('zip', '=', partner.zip),
                ]
            else:
                domain = [
                    ('id', '!=', partner.id),
                    ('email', '=', partner.email),
                    ('email', '!=', False),
                ]
            other_partners = self.search(domain)
            if other_partners:
                if not partner.is_company:
                    raise ValidationError(
                        _("This email is already set to partner '%s'")
                        % other_partners[0].display_name)
                else:
                    raise ValidationError(
                        _("Please check the combo of zip and email it is already set for '%s'")
                        % other_partners[0].display_name)


ResPartner()




class ResCompany(models.Model):
    _inherit = 'res.company'
    
    
    other_phone = fields.Char('Phone')
    other_fax = fields.Char('Fax')
    other_city = fields.Char('City')
    other_country = fields.Many2one('res.country' , 'Country')
    other_zip = fields.Char('ZIP')
    other_state = fields.Many2one('res.country.state' ,'State')
    other_street = fields.Char('Street')
    vat = fields.Char(related='partner_id.vat', string="VAT")
    
