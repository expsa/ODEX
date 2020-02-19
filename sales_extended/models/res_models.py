
from datetime import datetime
from lxml import etree, html
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class ResBank(models.Model):
    _inherit = 'res.bank'
    arabic_address = fields.Char(string="Arabic Address")
    name = fields.Char(string="Name",translate=True)
    # street  = fields.Char(translate=True)
    # city  = fields.Char(translate=True)
    # street2  = fields.Char(translate=True)


class productCustom(models.Model):
    _inherit = 'product.template'
    description_sale = fields.Html(string="Sale Description" , translate=True )
    # street  = fields.Char(translate=True)
    # city  = fields.Char(translate=True)
    # street2  = fields.Char(translate=True)