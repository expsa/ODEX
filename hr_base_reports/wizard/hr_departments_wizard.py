# -*- coding: utf-8 -*-
from odoo import models, fields, api,_



class HrDepatmentJobWizard(models.TransientModel):
    _name = 'hr.department.job.wizard'
    report_type = fields.Selection([('departments', _('Departments')), ('jobs', _('Jobs'))])

    @api.multi
    def get_reports_departs(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'report_type': self.report_type,

            },
        }
        return self.env.ref('hr_base_reports.action_department_report').report_action(self, data=data)

    @api.multi
    def get_reportxlsxs(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'report_type': self.report_type,

            },
        }
        return self.env.ref('hr_base_reports.action_department_report_xlsx').report_action(self, data=data)


class ReportDepartmentJobParse(models.AbstractModel):
    _name = 'report.hr_base_reports.department_job_report_view'

    @api.model
    def get_report_values(self, docids, data=None):

        docs = []
        departments = self.env['hr.department'].search([], order='name asc')
        jobs = self.env['hr.job'].search([], order='name asc')

        type = data['form']['report_type']
        depart_total = 0
        jobs_total = 0

        if type == 'departments':

            for department in departments:
                depart_total += department.total_employee

                docs.append({
                    'department_name': department.name,
                    'employee_number': department.total_employee,
                })

            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'report_new_type': 'departments',
                'total_amount': depart_total,
                'docs': docs,
            }

        elif type == 'jobs':

            for job in jobs:
                docs.append({
                    'job_name': job.name,
                    'employee_number': job.no_of_employee,
                })
                jobs_total += job.no_of_employee


            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'report_new_type': 'jobs',
                'total_amount': jobs_total,
                'docs': docs,
            }
class HrDepartmentJobParseXlsx(models.AbstractModel):
    _name = "report.hr_base_reports.action_department_report_xlsx"
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):

        docs = []
        departments = self.env['hr.department'].search([], order='name asc')
        jobs = self.env['hr.job'].search([], order='name asc')

        type = data['form']['report_type']
        depart_total = 0
        jobs_total = 0
        if type == 'departments':
            for department in departments:
                depart_total += department.total_employee
                docs.append({
                    'department_name': department.name,
                    'employee_number': department.total_employee,

                })



        elif type == 'jobs':

            for job in jobs:
                docs.append({
                    'job_name': job.name,
                    'employee_number': job.no_of_employee,

                })
                jobs_total += job.no_of_employee


        sheet = workbook.add_worksheet('Res Partner Info')

        format2 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2.set_align('center')
        format2.set_align('vcenter')


        if type == 'departments':
            sheet.merge_range('B5:F5', 'Departments Of Employees', format2)
            sheet.write(6, 2, 'department', format2)
            sheet.set_column('C:C', 25)
            sheet.write(6, 3, u'Total', format2)
            sheet.set_column('D:H', 25)
            row = 6
            for line in docs:
                row += 1
                sheet.write(row, 2, line['department_name'], format2)
                sheet.write(row, 3, line['employee_number'], format2)

            sheet.write(row+1, 3, depart_total, format2)

        elif type == 'jobs':
            sheet.merge_range('B5:F5', 'Jobs Of Employees', format2)
            sheet.write(6, 2, 'jobs', format2)
            sheet.set_column('C:C', 25)
            sheet.write(6, 3, u'Total', format2)
            sheet.set_column('D:H', 25)

            row = 6
            for line in docs:
                row += 1
                sheet.write(row, 2, line['job_name'], format2)
                sheet.write(row, 3, line['employee_number'], format2)

            sheet.write(row+1, 3, jobs_total, format2)



