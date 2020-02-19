from odoo import models, fields, api
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceCustom(models.Model):
    _inherit = 'account.invoice'
    
    purchase_order_id=fields.Char(string='Offer Number')
    order_dated = fields.Date(string='Offer Dated')
    bank_account = fields.Many2one('res.partner.bank' , 'Bank Account')
    arabic_comment = fields.Text(placeholder="Arabic Term and conditions")


class ResCurrencyCustom(models.Model):
    _inherit = 'res.currency'
    
    name=fields.Char(string='Name',translate=True)
    

class CustomInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # name = fields.Html(string="Description",compute='_compute_name')
    name = fields.Html(string="Description")

    def _compute_name(self):
        for line in self:
            return super(CustomInvoiceLine ,line)._onchange_product_id()



