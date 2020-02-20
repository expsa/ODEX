# -*- coding: utf-8 -*-
{
    'name': 'Website Language Flag',
    'category': 'Website',
    'summary': 'Website language flag',
    'version': '1.0',
    'description': """
    Adds language flag to the menu .
    You can define language flag in settings/languages
        """,
    'author': 'DevTalents',
    'website': 'www.templates-odoo.com',
    'depends': [
        'website'
    ],
    'data': [
        'views/template_flag.xml',
        'views/res_flag.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'price': '8',
    'currency':'EUR',
    'live_test_url':'http://paybox.dev-talents.com/',
    'installable': True,
    'application': True,
}
