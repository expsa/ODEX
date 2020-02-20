# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class HrPenaltyDeductionOfEmployee(models.TransientModel):
    _name = "penalty.deduction.wizard"

    _description = "Penalty Deduction of employee"

    date_from = fields.Datetime()
    date_to = fields.Datetime()
    report_type = fields.Selection(selection=[('warning',_('Warning')),
                                       ('penalty',_('Penalty')),
                                       ('termination', _('Termination')),
                                       ('deprivation', _('Deprivation of promotion and promotion')),
                            ], default='warning')


    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'report_type': self.report_type,
            },
        }


        return self.env.ref('hr_base_reports.action_report_penalty').report_action(self, data=data)

    @api.multi
    def get_reportxlsxs(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'report_type': self.report_type,
            },
        }
        return self.env.ref('hr_base_reports.action_report_penalty_xlsx').report_action(self, data=data)

class ReportHrPenaltyDeductionOfEmployee(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.hr_base_reports.report_penalty_template'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        report_type  = data['form']['report_type']


        docs = []

        penalty = self.env['hr.penalty.register'].search([
            ('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT)),
        ])

        for item in penalty:
            for element in item:
                for punishment_type in element.punishment_id:
                    if punishment_type.type == report_type:
                        docs.append({
                            'employee': item.employee_id.name,
                            'department': item.department_id.name,
                            'penalty': item.penalty_id.name,
                            'punishment_type': punishment_type.name,
                        })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start.strftime(DATE_FORMAT),
            'date_end': (date_end - timedelta(days=1)).strftime(DATE_FORMAT),
            'docs': docs,
        }










class HrOvertimeJobParseXlsx(models.AbstractModel):
    _name = "report.hr_base_reports.action_report_penalty_xlsx"
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        report_type  = data['form']['report_type']


        docs = []

        penalty = self.env['hr.penalty.register'].search([
            ('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT)),
        ])

        for item in penalty:
            for element in item:
                for punishment_type in element.punishment_id:
                    if punishment_type.type == report_type:
                        docs.append({
                            'employee': item.employee_id.name,
                            'department': item.department_id.name,
                            'penalty': item.penalty_id.name,
                            'punishment_type': punishment_type.name,
                        })

        sheet = workbook.add_worksheet('Termination of employees')
        format1 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2.set_align('center')
        format2.set_align('vcenter')
        format1.set_font_color('black')
        format1.set_fg_color('#e6e6e6')
        format2.set_font_color('#464dbb')
        format2.set_fg_color('#e6e6ff')

        sheet.write('A3:A3', 'Employee', format2)
        sheet.write('B3:B3', 'Department', format2)
        sheet.write('C3:C3', 'Penalty', format2)
        sheet.write('D3:D3', 'Punishment type', format2)
        # sheet.write('E3:E3', 'Holiday type', format2)
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        # sheet.set_column('E:E', 20)

        row = 3
        col = 0
        for line in docs:
            row += 1
            sheet.write(row, col, line['employee'], format1)
            sheet.write(row, col + 1, line['department'], format1)
            sheet.write(row, col + 2, line['penalty'], format1)
            sheet.write(row, col + 3, line['punishment_type'], format1)
            # sheet.write(row, col + 3, line['holiday_status_id'], format1)










