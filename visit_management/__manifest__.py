# -*- coding: utf-8 -*-
{
    "name": "Customer Visit Management",
    "version": "1.0",
    "description": """
        Customer Visit module
    """,
    "depends": ['sale', 'calendar'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/area_view.xml',
        'views/report_visit_targets.xml',
        'views/report.xml',
        'views/visit_view.xml',
        'wizard/cancel_visit_wiz_view.xml',
    ],
    'installable': True,
    'application': True,
}
