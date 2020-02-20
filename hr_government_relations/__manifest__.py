# -*- coding: utf-8 -*-

{
    'name': 'Employee Government',
    'version': '1.0',
    'category': 'HR-Odex',
    'author': 'Expert Co. Ltd.' ,
    'website': 'http://exp-sa.com',
    'summary': 'Create Contract Termination Requests for Employees',
    'depends': ['base', 'hr','account','hr_base'],
    'demo': [],
    'data': [

        'security/hr_government_relations_security.xml',
        'security/ir.model.access.csv',
        'views/exit_and_return.xml',
        'views/request_visa.xml',
        'views/renew_official_paper.xml',
        'report/renew_official_paper_report.xml',
        'report/renew_official_paper_template.xml',

        # menu items
        'views/government_relations_menus.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
