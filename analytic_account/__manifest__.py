# -*- coding: utf-8 -*-
{
    'name': "Analytic Accounting Custom",

    'description': """
    Module for extending analytic accounting object.
===============================================

Adding new features in odoo analytic account :
-hierarchy structure and view.

    """,

    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",


    'category': 'Hidden/Dependency',

    # any module necessary for this one to work correctly
    'depends': ['analytic', 'account_custom', 'hierarchical_chart'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/hr_department_view.xml',
    ]
}
