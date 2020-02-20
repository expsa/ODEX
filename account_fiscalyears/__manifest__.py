# -*- coding: utf-8 -*-
{
    'name': "Account Fiscal Years",

    'summary': """
        this module is adding accounting main models to fiscalyear
        """,

    'description': """
    """,

    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",

    'category': 'Accounting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['fiscalyears', 'account_custom', 'account_voucher', 'account_budget',
                'custom_tools'],

    # always loaded
    'data': [
        'security/account_fiscalyear_security.xml',
        'views/account_fiscalyears_views.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/account_voucher_views.xml',
        'views/account_view.xml',
        'views/account_budget_views.xml',
    ],

}
