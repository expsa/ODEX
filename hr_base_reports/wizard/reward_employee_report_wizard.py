# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class HrRewardWizard(models.Model):

    _name = 'hr.reward.wizard'
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')

    @api.multi
    def get_report_reward(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'department_id': self.department_id.id,
                'job_id': self.job_id.id,
            },
        }

        return self.env.ref('hr_base_reports.action_report_employee_rewrad').report_action(self, data=data)



    @api.multi
    def get_reward_report_xlsx(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'department_id': self.department_id.id,
                'job_id': self.job_id.id,

            },
        }
        return self.env.ref('hr_base_reports.action_employee_reward_report_xlsx').report_action(self, data=data)


class ReportHrRewardEmployee(models.AbstractModel):
    _name = 'report.hr_base_reports.report_employee_reward_template'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        department = data['form']['department_id']
        job = data['form']['job_id']

        docs = []

        employee_reward = self.env['hr.employee.reward'].search(
            [('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
             ('create_date', '<', date_end.strftime(DATETIME_FORMAT))])

        for employee in employee_reward:

            for item in employee.line_ids_reward:

                if department or job:

                    if item.employee_id.department_id.id == department or item.employee_id.job_id.id == job:
                        docs.append({
                            'employee_no': item.employee_id.emp_no,
                            'employee_name': item.employee_id.name,
                            'employee_depart': item.employee_id.department_id.name,
                            'employee_job': item.employee_id.job_id.name,
                            'rewrad_reason':employee.allowance_reason,
                            'amount':item.amount,



                        })
                    else:
                        docs.append({
                            'employee_no': '',
                            'employee_name': '',
                            'employee_depart':'',
                            'employee_job': '',
                            'rewrad_reason':'',
                            'amount':'',
                        })
                else:
                    docs.append({
                        'employee_no': item.employee_id.emp_no,
                        'employee_name': item.employee_id.name,
                        'employee_depart': item.employee_id.department_id.name,
                        'employee_job': item.employee_id.job_id.name,
                        'rewrad_reason': employee.allowance_reason,
                        'amount': item.amount,

                    })
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start.strftime(DATE_FORMAT),
            'date_end': (date_end - timedelta(days=1)).strftime(DATE_FORMAT),
            'docs': docs,
        }



class EmployeeRewardParseXlsx(models.AbstractModel):
    _name = "report.hr_base_reports.action_employee_reward_report_xlsx"
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):

        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        department = data['form']['department_id']
        job = data['form']['job_id']

        docs = []

        employee_reward = self.env['hr.employee.reward'].search(
            [('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
             ('create_date', '<', date_end.strftime(DATETIME_FORMAT))])

        for employee in employee_reward:

            for item in employee.line_ids_reward:
                if department or job:

                    if item.employee_id.department_id.id == department or item.employee_id.job_id.id == job:
                        docs.append({
                            'employee_no': item.employee_id.emp_no,
                            'employee_name': item.employee_id.name,
                            'employee_depart': item.employee_id.department_id.name,
                            'employee_job': item.employee_id.job_id.name,
                            'rewrad_reason': employee.allowance_reason,
                            'amount': item.amount,

                        })
                    else:
                        docs.append({
                            'employee_no': '',
                            'employee_name': '',
                            'employee_depart': '',
                            'employee_job': '',
                            'rewrad_reason':'',
                            'amount': '',
                        })

                else:
                    docs.append({
                        'employee_no': item.employee_id.emp_no,
                        'employee_name': item.employee_id.name,
                        'employee_depart': item.employee_id.department_id.name,
                        'employee_job': item.employee_id.job_id.name,
                        'rewrad_reason': employee.allowance_reason,
                        'amount': item.amount,

                    })

        sheet = workbook.add_worksheet('Employee Reward Report')
        format1 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2.set_align('center')
        format2.set_align('vcenter')
        format1.set_font_color('black')
        format2.set_font_color('#464dbb')
        format2.set_fg_color('#e6e6ff')
        sheet.merge_range('B5:F5', 'Employee Reward Report', format2)

        sheet.write(6, 1, 'Employee Number', format2)
        sheet.set_column('A:B', 25)
        sheet.write(6, 2, 'Employee Name', format2)
        sheet.set_column('C:D', 25)
        sheet.write(6, 3, 'Department Name', format2)
        sheet.set_column('E:F', 25)
        sheet.write(6, 4, 'Job Title', format2)
        sheet.set_column('G:H', 25)
        sheet.write(6, 5, 'Reward Reason', format2)
        sheet.set_column('I:J', 25)
        sheet.write(6, 6, 'Amount', format2)
        sheet.set_column('K:L', 25)

        row = 6

        for line in docs:
            row += 1
            sheet.write(row, 1, line['employee_no'], format1)
            sheet.write(row, 2, line['employee_name'], format1)
            sheet.write(row, 3, line['employee_depart'], format1)
            sheet.write(row, 4, line['employee_job'], format1)
            sheet.write(row, 5, line['rewrad_reason'], format1)
            sheet.write(row, 6, line['amount'], format1)

