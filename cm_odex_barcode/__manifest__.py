# -*- coding: utf-8 -*-
##############################################################################
#
#    Odex - Communications Management System.
#    Copyright (C) 2018 Expert Co. Ltd. (<http://exp-sa.com>).
#
##############################################################################
{
    'name': 'Communications Management Barcodes Reports',
    'version': '0.1',
    'sequence': 4,
    'author': 'Expert Co. Ltd.',
    'category': 'Communications',
    'summary': 'Correspondence Management System',
    'description': """
Odex - Communications Management Reports
========================================
    """,
    'website': 'http://www.exp-sa.com',
    'depends': ['exp_transaction_documents'],
    'data': [
        'reports/barcodes.xml',
        'views/transactions_views.xml',
        'views/assets.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
