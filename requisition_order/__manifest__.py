{
    'name': 'Requisition Order',
    'summary': '''
    Adding the feature of requisition order allowing users to request
    for services
     ''',
    'category': 'Accounting',
    'author': 'Alfadil',
    'depends': [
        'initiative_management',
        'account_fiscalyears',
        'account_budget_custom',
        'analytic_account',
        'account_voucher',

    ],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/requisition_data.xml',
        'data/donation_data.xml',
        'views/account_payment_view.xml',
        'views/requisition_request_view.xml',
        'views/account_invoice_view.xml',
        'views/account_view.xml',
        'views/donation_request_view.xml',
        'views/account_voucher_view.xml',
    ],
    'installable': True,
}
