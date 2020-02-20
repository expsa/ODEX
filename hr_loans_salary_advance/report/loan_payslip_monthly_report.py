# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError, UserError

class PayslipMonthlyReport(models.AbstractModel):
    _inherit = 'report.exp_payroll_custom.payslip_monthly_report'

    def get_loan_values(self, data=None):
        docs = []
        loan_line = self.env['loan.installment.line']
        count = 0
        exception = False
        if data['delist'] == 'ff':
            ftotal = 0
            title = _('Loans Totals')
            docs.append({'count': '#', 'rule': _('Name'), 'type': _('Type'), 'amount': _('Amount'), })
            for loan in  self.env[data['loan_model']].browse(data['loan_ids']):
                count += 1
                total = sum(loan_line.browse(data['loan_line_ids']).filtered(\
                    lambda r: r.deduction_line.request_type.id == loan.id).mapped('installment_amount'))
                ftotal += total
                docs.append({'count': count,  'rule': loan.name,'type': _('Loan'), 'amount': total, })
            docs.append({'count': '', 'rule': _('Total'), 'type': '', 'amount': ftotal, })
        elif data['delist'] == 'tt':
            #TODO review bellow raise
            if not data['loan_line_ids'] or not data['loan_ids']: raise ValidationError(_('Sorry No Loan Data To Be Printed'))
            title = _('Employees Loans Paysheet')
            loan_dict = {}
            for line in self.env['loan.request.type'].browse(data['loan_ids']):
                loan_dict.setdefault('loans', [])
                loan_dict['loans'] += line
            tdict = {'count': '#', 'emp': _('Name'),}
            ndict = {'count': '', 'emp': _('Nets'), }
            if self.env.context.get('track_emp', False): tdict['track_id'] = 'track_id'
            for key,value in loan_dict.items():
                for x in value:
                    tdict[x.id], ndict[x.id] = x.name, 0
                #tdict[key], ndict[key] = key, 0
            tdict['net'], ndict['net'] = _('Total'), 0
            docs.append(tdict)
            fnet = 0
            for emp in self.env[data['model']].browse(data['ids']):
                emp_dict = {}
                count += 1
                net = 0
                for key,value in tdict.items():
                    if value == _('#'):
                        emp_dict[key]= count
                        continue
                    elif value == _('Name'):
                        emp_dict[key]= emp.name
                        continue
                    elif value == 'track_id':
                        emp_dict['track_id'] = emp.id
                        continue
                    elif isinstance(key , int):
                        total = sum(loan_line.browse(data['loan_line_ids']).filtered(
                            lambda r: r.deduction_line.employee_id.id == emp.id and\
                                      r.deduction_line.request_type.id == key).mapped('installment_amount'))
                        emp_dict[key] = total
                        net += total
                        fnet += total
                        ndict[key] += total
                    elif isinstance(key , str):
                        emp_dict[key] = net
                        ndict[key] += net
                    if value == _('Net'):
                        emp_dict[key] = net
                        continue
                docs.append(emp_dict)
            ndict['net'] = fnet
            docs.append(ndict)
        else:
            title = _('Specific Loan Report')
            exception = True
            for loan in self.env[data['loan_model']].browse(data['loan_ids']):
                count = 0
                ftotal = 0
                inner_doc = {'rule': loan.name, 'lines': [],}
                inner_doc['lines'].append({'count': '#', 'emp': _('Employee'), 'amount': _('Amount'), })
                for emp in set(loan_line.browse(data['loan_line_ids']).filtered(\
                        lambda r: r.deduction_line.request_type.id == loan.id ).mapped('deduction_line.employee_id')):
                    count += 1
                    total  = sum(loan_line.browse(data['loan_line_ids']).filtered(
                            lambda r: r.deduction_line.employee_id.id == emp.id and\
                                      r.deduction_line.request_type.id == loan.id).mapped('installment_amount'))
                    ftotal += total
                    inner_doc['lines'].append({'count': count,'emp': emp.name,'amount': total,})
                inner_doc['lines'].append({'count': '', 'emp': _('Total'), 'amount': ftotal, })
                docs.append(inner_doc)
        return title, exception, docs

    def get_unified_result(self, docs, docs_rule):
        docs[0].pop('count', )
        docs[0].pop('track_id')
        docs[0].pop('emp')
        docs[0]['net'] = _('Total Loans')
        theader = docs.pop(0)
        docs_rule[0].pop('track_id')
        for kk, vv in theader.items():
            mk = isinstance(kk, int) and 'l' + str(kk) or 'l' + kk
            first = True
            for d in docs_rule:
                if first:
                    d.setdefault(mk, vv)
                else:
                    d.setdefault(mk, 0)
                    if d.get('track_id'):
                        for lk in docs:
                            if lk.get('track_id') and lk['track_id'] == d['track_id'] and lk.get(kk):
                                d[mk] = -1*lk[kk]
                                break
                    else:
                        d[mk] = [-1*lk[kk] for lk in docs if not lk.get('track_id')][0]
                first = False
        final_net = 0
        first = True
        for d in docs_rule:
            if d.get('track_id'):
                d.pop('track_id')
                d['take_home'] = d['net'] + d['lnet']
                final_net += d['net'] + d['lnet']
            else:
                if first:
                    d['take_home'] = _('Final Net')
                else:
                    d['take_home'] = final_net
            first = False
        docs = docs_rule
        return _('Allowances/ Deductions and Loans Total'), docs

    @api.model
    def get_report_values(self, docids, data=None):
        if not data['form']['no_loan'] and not data['form']['no_rule']:
            #TODO: review Param
            rtitle, rexception, docs_rule = self.get_rule_values(data)
            ltitle, exception, docs = self.get_loan_values(data)
            if data['delist'] == 'tt':
                title, docs = self.get_unified_result(docs, docs_rule)
            else:
                docs_rule += docs
                docs = docs_rule
                title = _('Specific Allowances/ Deductions and Loans Report')
        elif data['form']['no_loan']:
            title, exception, docs = self.get_rule_values(data)
        elif data['form']['no_rule']:
            title, exception, docs = self.get_loan_values(data)
        return {
            'exception': exception,
            'title': title,
            'date_from': data['form']['date_from'],
            'date_to' : data['form']['date_to'],
            'docs': docs,
            }

class PayslipMonthlyReportXlsx(models.AbstractModel):
    _inherit = 'report.exp_payroll_custom.payslip_monthly_report_xlsx'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):
        if not data['form']['no_loan'] and not data['form']['no_rule']:
            rtitle, rexception, docs_rule = self.env['report.exp_payroll_custom.payslip_monthly_report'].with_context(track_emp=True).get_rule_values(data)
            ltitle, exception, docs = self.env['report.exp_payroll_custom.payslip_monthly_report'].with_context(track_emp=True).get_loan_values(data)
            if data['delist'] == 'tt':
                title, docs = PayslipMonthlyReport.get_unified_result(self, docs=docs, docs_rule=docs_rule)
            else:
                docs_rule += docs
                docs = docs_rule
                title = _('Specific Allowances/ Deductions and Loans Report')
        elif data['form']['no_loan']:
            return super(PayslipMonthlyReportXlsx, self).generate_xlsx_report(workbook, data, objs)
        elif data['form']['no_rule']:
              title, exception, docs = PayslipMonthlyReport.get_loan_values(self,data)

        sheet = workbook.add_worksheet('Proll Monthly report')
        format1 = workbook.add_format({'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center', })
        format2 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,'align': 'center', 'bold': True})
        format2.set_align('center')
        format2.set_align('vcenter')
        format3 = workbook.add_format({'bottom': True,  'align': 'center', 'bold': True, })
        if data['delist'] != 'tf':
            sheet.merge_range('C5:F5', title, format2)
            sheet.merge_range('C6:F6', data['form']['date_from'] + '  -  ' + data['form']['date_to'], format2)
        else:
            sheet.merge_range('C5:E5', title, format2)
            sheet.merge_range('C6:E6', data['form']['date_from'] + '  -  ' + data['form']['date_to'], format2)
        sheet.set_column('C:C', 10)
        sheet.set_column('D:D', 40)
        #sheet.set_column('E:Z', 20)
        row = 6
        for line in docs:
            if data['delist'] != 'tf':
                row += 1
                clm = 1
                for k,v in line.items():
                    clm += 1
                    sheet.write(row, clm, line[k], format1)
            else:
                row += 1
                clm = 2
                sheet.write(row, clm, line['rule'], format3)
                for ln in line['lines']:
                    row += 1
                    clm = 1
                    for k,v in ln.items():
                        clm += 1
                        sheet.write(row, clm, ln[k], format1)
                row += 1
