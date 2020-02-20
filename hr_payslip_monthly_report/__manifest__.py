# -*- coding: utf-8 -*-
{
    'name': 'Payroll-Payslip Reporting',
    'version': '1.0',
    'summary': """Payslip Pivot View Report.""",
    'description': """Payslip monthly report.
    This module gives a pivot view for the HR managers. they can see all the 'NET' amount of payslips in all states""",
    'category': 'HR-Odex',
    'author': 'Expert Co. Ltd.' ,
    'website': 'http://exp-sa.com',
    'depends': ['hr_payroll'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/menu_payslip_report.xml'
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
