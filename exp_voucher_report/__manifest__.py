# -*- coding: utf-8 -*-

{
    'name': 'voucher Print',
    'version': '11.0.0.0',
    'category': 'Accounting',
    'sequence': 1,
    'summary': "Print of payments",
    'description':"Print of payments",
    'author': 'Expert Co. Ltd.',
    'website': 'http://www.exp-sa.com',
    'website': '',
    'depends': ['account_voucher'],
    'data': [
        'report/print_receipt_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}


