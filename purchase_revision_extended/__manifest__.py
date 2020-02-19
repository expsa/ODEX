# -*- coding: utf-8 -*-

{
    'name': 'Purchase Revision',
    'version': '11.1',
    'summary': 'Create Revision and Apply Revision',

    'category': 'Purchase',

    'description': """ This module adds a functionality to manage different revisions and can be rolled 
    back to any revision at anytime in Purchase order.""",
    'depends': ['purchase'],
    'data': [
        'views/purchase_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
