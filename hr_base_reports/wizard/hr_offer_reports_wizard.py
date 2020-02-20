# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class HrOfferReportsWizard(models.Model):

    _name = 'hr.offer.wizard'
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')

    @api.multi
    def get_report_offer(self):

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



        return self.env.ref('hr_base_reports.action_report_job_offer').report_action(self, data=data)

    @api.multi
    def get_report_offer_xlsx(self):
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
        return self.env.ref('hr_base_reports.action_job_offer_report_xlsx').report_action(self, data=data)


class ReportHrOfferJobOfEmployee(models.AbstractModel):

    _name = 'report.hr_base_reports.report_offer_job_template'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        department = data['form']['department_id']
        job = data['form']['job_id']

        docs = []

        job_offer = self.env['hr.job.offer.signature'].search([('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT))])
        for item in job_offer:
            if department or job:


                if item.department.id == department or item.job_type.id == job:
                    docs.append({
                        'employee': item.employee,
                        'department': item.department.name,
                        'job': item.job_type.name,

                    })
                else:
                    docs.append({
                        'employee': '',
                        'department': '',
                        'job': '',
                    })
            else:
                docs.append({
                    'employee': item.employee,
                    'department': item.department.name,
                    'job': item.job_type.name,

                })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start.strftime(DATE_FORMAT),
            'date_end': (date_end - timedelta(days=1)).strftime(DATE_FORMAT),
            'docs': docs,
        }



class HrJobOfferParseXlsx(models.AbstractModel):
    _name = "report.hr_base_reports.action_job_offer_report_xlsx"
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        department = data['form']['department_id']
        job = data['form']['job_id']

        docs = []

        job_offer = self.env['hr.job.offer.signature'].search([('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT))])


        for item in job_offer:
                if department or job:
                    if item.department.id == department or item.job_type.id == job:
                        docs.append({
                            'employee': item.employee,
                            'department': item.department.name,
                            'job': item.job_type.name,

                        })

                    else:
                        docs.append({
                            'employee':'',
                            'department': '',
                            'job': '',
                        })
                else:
                    docs.append({
                        'employee': item.employee,
                        'department': item.department.name,
                        'job': item.job_type.name,

                    })


        sheet = workbook.add_worksheet('Job Offers of employees')
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
        sheet.merge_range('B5:F5', 'Jobs Offers Of Employees', format2)

        sheet.write(6,2 , 'Employee Name', format2)
        sheet.set_column('C:D', 25)
        sheet.write(6,3, 'Job Title', format2)
        sheet.set_column('E:F', 25)
        sheet.write(6,4, 'Department Name', format2)
        sheet.set_column('G:H', 25)




        row = 6

        for line in docs:
            row += 1
            sheet.write(row, 2, line['employee'], format1)
            sheet.write(row,3 , line['job'], format1)
            sheet.write(row, 4, line['department'], format1)
