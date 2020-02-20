# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api


class PayrollReportView(models.Model):
    _name = 'hr.payroll.report.view'
    _auto = False

    name = fields.Many2one(comodel_name='hr.employee', string='Employee')
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    state = fields.Selection(selection=[('draft', 'Draft'), ('verify', 'Waiting'), ('done', 'Done'), ('cancel', 'Rejected')],
                             string='Status')
    job_id = fields.Many2one(comodel_name='hr.job', string='Job Title')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')
    department_id = fields.Many2one(comodel_name='hr.department', string='Department')
    net = fields.Float(string='Net Salary')

    def _select(self):
        select_str = """
        min(ps.id) as id,emp.id as name,jb.id as job_id,
        dp.id as department_id,cmp.id as company_id,
        ps.date_from, ps.date_to, sum(psl.total) as net, ps.state as state
        """
        return select_str

    def _from(self):
        from_str = """
            hr_payslip_line psl  join hr_payslip ps on (ps.employee_id=psl.employee_id and ps.id=psl.slip_id)
            join hr_employee emp on (ps.employee_id=emp.id) join hr_department dp on (emp.department_id=dp.id)
            join hr_job jb on (emp.department_id=jb.id) join res_company cmp on (cmp.id=ps.company_id) where psl.code='NET'
         """
        return from_str

    def _group_by(self):
        group_by_str = """
            group by emp.id,psl.total,ps.date_from, ps.date_to, ps.state,jb.id,dp.id,cmp.id
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as ( SELECT
               %s
               FROM %s
               %s
               )""" % (self._table, self._select(), self._from(), self._group_by()))

