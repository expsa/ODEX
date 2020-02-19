# -*- coding: utf-8 -*-
{
    'name' : 'Exchange Request',
    'version' : '1.1',
    'summary': 'Adding new Functionality on the inventory',
    'sequence': -2,
    'description': """
            This module is made to add new functionalities on the Stock and create new 
            object called Exchange Request to classify the requests depend on it..
    """,
    'data':[
        # 'security/stock_groups.xml',
        'security/ir.model.access.csv',
        'sequence/exchange_sequence.xml',
        'views/exchange_request.xml',
        'views/stock_journal.xml',
        'wizard/exchange_wizard.xml'
    ],
    'depends' : ['purchase_requisition', 'stock'],
    'installable': True,
    'application': True,
}
