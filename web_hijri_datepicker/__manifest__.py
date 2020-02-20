# -*- encoding: utf-8 -*-
{
    "name": "Hijri(Islamic) Datepicker",
    'version': '11.0',
	'author': '', 
    'summary': """Odoo Web (Hijri)Islamic Datepicker. The Hijri(Islamic) calendar is the official calendar in countries around the Gulf, especially Saudi Arabia.""",
    "description":
        """
        Odoo Web (Hijri)Islamic Datepicker.
        """,
    "depends": ['base','web'],
    'category': 'web',
    'data': [
        "views/res_language_view.xml",
        "views/web_hijri.xml"
    ],

    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'auto_install': False,

}
