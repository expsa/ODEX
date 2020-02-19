# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

# Incoming Outgoing Report wizard
class IncomingOutgoingReportWizard(models.TransientModel):
    _name = 'incoming.outgoing.report'

    date_from = fields.Date(string='From',required=True)
    date_to = fields.Date(string='To',required=True)
    location_id = fields.Many2one('stock.location' , string='Location', domain=[('usage','=','internal')])
    category_id = fields.Many2one('product.category',string="Category")
    product_ids = fields.Many2many('product.product','incoming_outgoing_products_rel','wizard_id','product_id' ,string='Products',)
    with_prices = fields.Boolean('With Prices')
    
    
    @api.multi
    def print_report(self, data):
        form_values = self.read()
        if self.date_to < self.date_from :
            raise exceptions.ValidationError(_("Date From Must Be Greater Than Date To"))
       
        
        datas = {
            'ids': [],
            'model': 'stock.move.line',
            'data':form_values
            }
        if self.with_prices:
           return self.env.ref('stock_custom_reports.action_incoming_outgoing_with_price_report').report_action(self, data=datas)
        return self.env.ref('stock_custom_reports.action_incoming_outgoing_report').report_action(self, data=datas)
