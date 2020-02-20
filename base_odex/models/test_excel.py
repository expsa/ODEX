# -*- coding: utf-8 -*-

import xlsxwriter
from StringIO import StringIO
import datetime
import base64

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning



def unwrap(val):
    if isinstance(val, (tuple, list)) and not len(val):
        return 0.0
    elif isinstance(val, (tuple, list)):
        val = val[0]
    if isinstance(val, bool):
        return bool(val)
    if isinstance(val, (int, long, float)):
        val = val
    return val



class BalanceSummaryWiz(models.TransientModel):
    _name = 'balance.summary'

    before = fields.Date(string='To Date', default=lambda *x, **xx: fields.Date.today())

    def build_excel(self, **data):
        row, col = 0, 0
        book = data['book']
        sheet = data['sheet']
        # Set styles and cell size
        bold = book.add_format({'bold': True})
        money = book.add_format({'num_format': '#,###.##'})
        sheet.set_column('A:A', 25)
        sheet.set_column('B:B', 35)
        sheet.set_column('C:H', 13)

        # write excel headers
        for i, header in enumerate([
            _(u'Code'),
            _(u'Name'),
            _(u'Debit'),
            _(u'Credit'),
            _(u'Balance'),
        ]):
            sheet.write(row, i, header, bold)
        row, col = 2, 0
        docs = data['docs']
        for doc in docs:
            sheet.write(row, col, doc.code, bold)
            # examine the record before writing
            if unwrap(doc.name):
                sheet.write(row, 1, unwrap(doc.name))
                sheet.write_number(row, 2, unwrap(doc.debit), money)
                sheet.write_number(row, 3, unwrap(doc.credit), money)
                sheet.write_number(row, 4, unwrap(doc.balance), money)
            else:
                sheet.write(row, 1, u'---')
                sheet.write(row, 2, u'---')
                sheet.write(row, 3, 0.0)
                sheet.write(row, 4, 0.0)
                sheet.write(row, 5, 0.0)
            row += 1
        sheet.write('A%s'%(row+2), _(u'Total : '), bold)
        sheet.write_formula('C%s'%(row+2), u'=SUM(C3:C%s)'%row, money)
        sheet.write_formula('D%s'%(row+2), u'=SUM(D3:D%s)'%row, money)
        sheet.write_formula('E%s'%(row+2), u'=SUM(E3:E%s)'%row, money)
        return sheet

    @api.multi
    def print_(self):
        selected = []
        contracts = []
        to_date = self.before
        before = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        accounts = self.env['account.account'].search([], order='code,name')
        
        
        docargs = {
            'doc_ids': accounts.ids,
            'docs': accounts,
            'unwrap': unwrap,
        }

        output = StringIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet(u'{} {}'.format(_(u'Balance'), before.strftime('%Y-%m-%d')))
        docargs['book'] = workbook
        docargs['sheet'] = worksheet
        res = self.build_excel(**docargs)
        workbook.close()
        output.seek(0)
        o = base64.encodestring(output.read())
        return {
            "type": "ir.actions.client",
            "tag": "export_excel",
            "context": {
                'workbook': o,
            },
        }
        return res
