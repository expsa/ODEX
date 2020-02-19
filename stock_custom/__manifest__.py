# -*- coding: utf-8 -*-
{
    'name' : 'Stock Custom',
    'version' : '1.1',
    'summary': 'Adding new Functionality on the stock',
    'sequence': -2,
    'description': """
            This module is made to add new functionalities on the Stock and create new 
            object called Stock Journal to classify the requests depend on it..
    """,
    'data':[
        'security/stock_groups.xml',
        # 'security/ir.model.access.csv',
        'views/stock_custom.xml',
        # 'sequence/exchange_sequence.xml',
        ],
    'depends' : ['stock','hr'],
    'installable': True,
    'application': True,
}
