# -*- coding: utf-8 -*-
{
    'name': "account_custom",

    'summary': """
        adding general feauters to account""",

    'description': """
        add any general new feauter to account
        add any general new group to account
        add any general new report to account
    """,

    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",


    'category': 'Accounting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account_invoicing'],

    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
        'security/groups.xml'

    ]
}
