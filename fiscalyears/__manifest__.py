# -*- coding: utf-8 -*-
{
    'name': "Fiscal Years",

    'summary': """
        this module is adding the feature of fiscalyear
        """,

    'description': """
    """,

    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",

    'category': '',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [],

    # always loaded
    'data': [
        'security/fiscalyear_security.xml',
        'security/ir.model.access.csv',
        'views/fiscalyears_views.xml',
    ],

}
