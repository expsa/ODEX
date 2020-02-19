# -*- coding: utf-8 -*-
from ast import literal_eval

from datetime import datetime
from lxml import etree, html
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    terms_id = fields.Many2one(comodel_name='sale.terms.conditions', string='Terms&Conditions')
    terms_desc = fields.Html(compute='_get_terms_clean')
    quote_print_total = fields.Selection(selection=[('without_total', 'Without Total'),
                                                    ('with_total', 'With Total')], required=True,
                                         default='without_total', string='Quote Print')
    valid_period = fields.Char(string='Valid Period')
    order_dated = fields.Date(string='Order Dated')
    ref_no = fields.Char(string='Ref No.')

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Order Confirmation'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    purchase_order_id=fields.Char(string='Purchase ID')
    our_order_num = fields.Char("Our Offer No")
    our_order_date = fields.Date("Our Offer date")

    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        print('-----------------------------iam copy')
        default = dict(default or {}, revision_no=False,revision_count = 0)
        return super(SaleOrder, self).copy(default=default)

    @api.multi
    def action_confirm(self):
        self.temp_sale_no = self.name
        self.temp_date = self.date_order
        return super(SaleOrder, self).action_confirm()

    @api.multi
    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()
        ctx = res['context']
        template_id = ctx.get('default_template_id')
        if template_id:
            template = self.env['mail.template'].sudo().browse(template_id)
            if self.quote_print_total == 'without_total':
                template.sudo().write(
                    {'report_template': self.env.ref('sales_extended.cepco_action_report_saleorder').id})
            else:
                template.sudo().write(
                    {'report_template': self.env.ref('sale.action_report_saleorder').id})
            ctx.update({
                'default_template_id': template.id
            })
        res.update({'context': ctx})
        return res

    @api.one
    @api.depends('terms_id')
    def _get_terms_clean(self):
        for item in self:
            if item.terms_id and item.terms_id.desc:
                if len(item.terms_id.desc) > 200:
                    item.terms_desc = item.terms_id.desc[:200] + '...........'
                else:
                    item.terms_desc = item.terms_id.desc + '...........'

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        default_term = self.env['sale.terms.conditions'].sudo().search([('default_term', '=', True)], limit=1,
                                                                       order='id desc')
        get_param = self.env['ir.config_parameter'].sudo().get_param
        use_sale_note = get_param('sale.use_sale_note')
        term_id = literal_eval(get_param('default_terms_id', default='False'))
        if use_sale_note:
            res['terms_id'] = term_id
        elif default_term:
            res['terms_id'] = default_term.id
        else:
            res['terms_id'] = False
        return res

    @api.multi
    @api.onchange('validity_date')
    def onchange_validity_date_period(self):
        for item in self:
            if item.validity_date:
                valid_date = datetime.strptime(item.validity_date, DEFAULT_SERVER_DATE_FORMAT).date()
                today = datetime.now().date()
                if valid_date > today:
                    delta = (valid_date - today).days
                    item.valid_period = _("Remain is %s days" % (delta))
                else:
                    item.valid_period = ''
            else:
                item.valid_period = ''

    @api.model
    def _get_sub_levels(self, product_id):
        accessories = product_id.product_accessory_ids
        product_list = []
        depth = [1]

        def inter_levels(product_id):
            deep_create = '.'.join([str(i) for i in depth])
            product_list.append(
                {'level': deep_create, 'products': [product_id]})

            depth.append(1)
            for child in product_id.product_id.product_tmpl_id.product_accessory_ids:
                inter_levels(child)
                depth[-1] += 1
            depth.pop()

        for accessory in accessories:
            inter_levels(accessory)
            depth[0] += 1
        return product_list

    @api.multi
    @api.onchange('order_line', 'order_line.line_no')
    def onchange_sale_order_line(self):
        product_list = []
        line_list = []
        product_level = len(self.order_line.filtered(
            lambda order_record: order_record.product_id and not order_record.parent_product_id))
        for order_item in self.order_line.filtered(
                lambda order_record: order_record.product_id and not order_record.parent_product_id):
            if order_item.product_id and not order_item.parent_product_id:
                if order_item.line_no:
                    product_level = order_item.line_no
                else:
                    product_level = len(self.order_line.filtered(
                        lambda order_record: order_record.product_id and not order_record.parent_product_id))
                product_list = self._get_sub_levels(order_item.product_id.product_tmpl_id)
                current_line = order_item.copy_data()[0]
                if current_line.get('line_no'):
                    product_level = current_line.get('line_no')
                current_line.update({'line_no': product_level})
                line_list.insert(0, current_line)
            else:
                product_level += 1
                new_current_line = order_item.copy_data()[0]
                line_list.append(new_current_line)
            if product_list:
                for item in product_list:
                    for product in item.get('products'):
                        line_season = '{0}.{1}'.format(product_level, item.get('level'))
                        line_list.append({
                            'name': product.product_id.name,
                            'product_id': product.product_id.id,
                            'product_uom_qty': product.qty,
                            'product_uom': product.product_id.uom_id.id,
                            'price_unit': product.product_id.list_price,
                            'line_no': line_season,
                            'parent_product_id': order_item.product_id.id
                        })
        if line_list:
            item_list = [(5, 0, 0)] + [(0, 0, line) for line in line_list]
            self.update({'order_line': item_list})

    @api.multi
    def format_terms(self, text):

        if 'price_value' in text:
            text=text.replace('price_value', str(self.amount_total))
        if 'term_value' in text:
            text=text.replace('term_value', str(self.payment_term_id.name))
        if 'valid_value' in text:
            text=text.replace('valid_value', self.valid_period or '')
        if 'bank_value' in text:
            bank_text = """
            <p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><u><span style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">Our Bank details as follows:</span></u></strong>
    <br><strong><u></u></strong>
    <br>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><span
            style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">%s</span></strong>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><span style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">A/C No. %s&nbsp;</span></strong>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><span style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">%s</span></strong>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><span style="font-size:19px;font-family:&quot;Courier New&quot;;color:blue;">Iban : &nbsp;%s</span></strong>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><u><span style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">SWIFT CODE</span></u></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">&nbsp; &nbsp; &nbsp; : &nbsp; &nbsp; &nbsp;%s</span></strong>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><u><span
            style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">Beneficiary</span></u></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">&nbsp; &nbsp; :</span></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">&nbsp; &nbsp; &nbsp;&nbsp;</span></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">%s</span></strong>
</p>
<p style="margin-top:0cm;margin-right:0cm;margin-bottom:.0001pt;margin-left:0cm;line-height:normal;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">
    <strong><u><span
            style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">Warranty</span></u></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">&nbsp; &nbsp; &nbsp; &nbsp;:</span></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">&nbsp; &nbsp; &nbsp;&nbsp;</span></strong><strong><span
        style="font-size:16px;font-family:&quot;Times New Roman&quot;,serif;color:black;">%s</span></strong>
</p>
            """ % (self.terms_id.bank_id.name or '', self.terms_id.bank_id.account_number or '',
                   self.terms_id.bank_id.street or '', self.terms_id.bank_id.iban or '',
                   self.terms_id.bank_id.bic or '', self.terms_id.bank_id.beneficiary or '',
                   self.terms_id.bank_id.warranty or '')
            text=text.replace('bank_value', bank_text)
        return text

    @api.model
    def text_from_html(self, html_content, max_words=None, max_chars=None,
                       ellipsis=u"…", fail=False):
        try:
            doc = html.fromstring(html_content)
        except (TypeError, etree.XMLSyntaxError, etree.ParserError):
            if fail:
                raise
            else:
                _logger.exception("Failure parsing this HTML:\n%s",
                                  html_content)
                return ""

        # Get words
        words = u"".join(doc.xpath("//text()")).split()

        # Truncate words
        suffix = max_words and len(words) > max_words
        if max_words:
            words = words[:max_words]

        # Get text
        text = u" ".join(words)

        # Truncate text
        suffix = suffix or max_chars and len(text) > max_chars
        if max_chars:
            text = text[:max_chars - (len(ellipsis) if suffix else 0)].strip()

        # Append ellipsis if needed
        if suffix:
            text += ellipsis

        return text


SaleOrder()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _order = 'line_no asc,order_id, layout_category_id, sequence, id'

    line_no = fields.Char(string='No.')
    parent_product_id = fields.Many2one(comodel_name='product.product')
    marked_done = fields.Boolean()
    name = fields.Html(string='Description', required=True)
    warranty_months = fields.Integer(string='Warranty Months', )
    warranty_partner_id = fields.Many2one(comodel_name='res.partner', domain=[('supplier', '=', True)],
                                          string='Warranty Provider')


SaleOrderLine()
