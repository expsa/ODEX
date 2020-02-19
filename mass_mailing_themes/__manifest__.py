# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mass Mailing Themes',
    'summary': 'Design gorgeous mails',
    'description': """
Design gorgeous mails
    """,
    'version': '1.0',
    'sequence': 110,
    'website': 'https://www.odoo.com/page/mailing',
    'category': 'Marketing',
    'depends': [
        'mass_mailing',
    ],
    'data': [
        'assets.xml',
        'views/mass_mailing_themes_templates.xml'
    ],
    'qweb': [],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
