# -*- coding: utf-8 -*-
{
    'name': "Initiative Management",

    'description': """
        Add new featurs of Initiatives which is a set of
        services
    """,

    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",


    'category': '',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'account_custom'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/initiative_goal_view.xml',
        'views/product_view.xml',
    ],
}
