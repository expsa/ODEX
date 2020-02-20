from odoo import models, fields, api


class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    # branch = fields.Char("Branch" ,required=True)
    # branch_t = fields.Char("Branch Tagline")
    flip = fields.Boolean("/ ")
    # sponsor_id = fields.Char(string="SponsorID",required=True)
    po_no = fields.Char(string="P.O Box No", )
    location = fields.Char(string="Location Code")

    company_link = fields.One2many('res.company.tree', 'company_id', string="License Documents")
    sponsor_link = fields.One2many('res.sponsor', 'sponsor_tree', string="Sponsors")
    hr_email = fields.Char(string='HR Email')


class ResCompanyExtTree(models.Model):
    _name = 'res.company.tree'

    doc_type = fields.Many2one(comodel_name='documents.typed', string="Doc Type")
    issue_date = fields.Date("Issue Date", required=True)
    latest_renewal_date = fields.Date("Latest Renewal Date")
    expiry_date = fields.Date("Expiry Date", required=True)
    renewal = fields.Date("Due for Renewal", required=True)

    company_id = fields.Many2one(comodel_name='res.company')


class Sponsor(models.Model):
    _name = 'res.sponsor'

    name = fields.Char(string='Sponsor Name', required=True, store=True)
    sponsor_id = fields.Integer(string='Sponsor ID', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact Person', required=True)
    cr_no = fields.Char(string='CR No')
    street = fields.Char()
    street2 = fields.Char()
    zip_code = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one(comodel_name='res.country.state', string="Fed. State")
    country_id = fields.Many2one(comodel_name='res.country', string="Country")
    pob = fields.Char(string='P.O Box No')
    email = fields.Char(related='partner_id.email', store=True ,readonly=True)
    phone = fields.Char(related='partner_id.phone', store=True)
    website = fields.Char(related='partner_id.website',readonly=True)
    fax = fields.Char(string="Fax")
    mobile = fields.Char(string='Mobile No')

    sponsor_tree = fields.Many2one(comodel_name='res.company')

    @api.onchange('state_id')
    def _onchange_state(self):
        self.country_id = self.state_id.country_id
