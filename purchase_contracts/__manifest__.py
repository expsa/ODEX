# -*- coding: utf-8 -*-
{
    'name' : 'Purchase Contract',
    'version' : '1.1',
    'summary': 'creating new purchase contract between vendors and company',
    'sequence': -2,
    'description': """
        creating purchase contracts
    """,
    'data':[
        'views/purchase_contract.xml',
        'security/ir.model.access.csv',
        'security/purchase_contract_groups.xml',
        ],
    'depends' : ['purchase'],
    'installable': True,
    'application': True,
}