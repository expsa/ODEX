## -*- coding: utf-8 -*-
##############################################################################
#
#    LCT, Life Connection Technology
#    Copyright (C) 2019-2020 LCT 
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class PayslipMonthlyReport(models.TransientModel):
    _inherit = 'payslip.monthly.report'
    _name = 'payslip.monthly.report'
    _description = "Payslips Monthly Report With Loans"

    loan_ids = fields.Many2many('loan.request.type', string='Loans')
    no_loan = fields.Boolean('No Loans',)

    def get_loan_lines(self):
        dom = []
        if self.salary_ids: dom += [('salary_scale', 'in', self.salary_ids.ids)]
        if self.level_ids: dom += [('salary_level', 'in', self.level_ids.ids)]
        if self.group_ids: dom += [('salary_group', 'in', self.group_ids.ids)]
        if self.degree_ids: dom += [('salary_degree', 'in', self.degree_ids.ids)]
        if self.employee_ids: dom += [('employee_id', 'in', self.employee_ids.ids)]
        emp_ids = [ r.employee_id.id for r in self.env['hr.contract'].search(dom)]
        domain = [('paid', '=', True), ('payment_date', '>=', self.date_from), ('payment_date', '<=', self.date_to),
                  ('deduction_line.employee_id', 'in', emp_ids)]
        if self.loan_ids: domain += [('deduction_line.request_type.id', 'in', self.loan_ids.ids)]
        return self.env['loan.installment.line'].search(domain)

    def check_data(self):
        if self.no_loan and self.no_rule:
            raise ValidationError(_('Please consider selecting loans and/or rules to print '))
        elif self.no_loan and not self.no_rule:
            datas, ctx, landscape = super(PayslipMonthlyReport, self).check_data()
        elif not self.no_loan and self.no_rule:
            landscape = False
            loan_lines = self.get_loan_lines()
            if not loan_lines: raise ValidationError(_('Sorry No Loans Data To Be Printed'))
            loan_ids = self.loan_ids and self.loan_ids.ids or self.env['loan.request.type'].search([]).ids
            loan_ids = list(set(loan_ids) and set([r.id for r in loan_lines.mapped('deduction_line.request_type')]))
            datas = {
                'loan_ids': loan_ids,
                'loan_model': 'loan.request.type',
                'loan_line_ids': [l.id for l in loan_lines],
                'form': (self.read()[0]),
            }
            ctx = self.env.context.copy()
            ctx.update({'active_model': 'loan.request.type', 'active_ids': loan_ids, })
            if self.detailed and self.listed:
                delist = 'tt'
                emp_ids = self.employee_ids and self.employee_ids.ids or \
                          list(set(r.deduction_line.employee_id.id for r in self.env['loan.installment.line'].browse().search([
                              ('payment_date', '>=', self.date_from), ('payment_date', '<=', self.date_to),('paid', '=', True)])))
                emp_ids = list(set(emp_ids) and set([r.id for r in loan_lines.mapped('deduction_line.employee_id')]))
                datas['ids'] = emp_ids
                datas['model'] = 'hr.employee'
                landscape = True
            elif self.detailed and not self.listed:
                delist = 'tf'
            else:
                delist = 'ff'
            datas['delist'] = delist
            return datas, ctx, landscape
        else:
            self = self.with_context({'track_emp': True, })
            datas, ctx, landscape = super(PayslipMonthlyReport, self).check_data()
            loan_lines = self.get_loan_lines()
            loan_ids = self.loan_ids and self.loan_ids.ids or self.env['loan.request.type'].search([]).ids
            loan_ids = list(set(loan_ids) and set([r.id for r in loan_lines.mapped('deduction_line.request_type')]))
            datas.update({
                'loan_ids': loan_ids,
                'loan_model': 'loan.request.type',
                'loan_line_ids': [l.id for l in loan_lines],
                'form': (self.read()[0]),})
        return datas,ctx, landscape

