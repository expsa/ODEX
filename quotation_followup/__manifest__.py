# -*- coding: utf-8 -*-
{
    'name': 'Quotation Follow-up Management',
    'version': '11.0',
    'category': 'Sale',
    'summary': 'This module allow you to do followup on your customer Open quotations.',
    'description': """This module allow you to do followup on your customer Open quotations..""",
    'depends': ['sale', 'popup_notifications'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/sale_followup_view.xml',
        'views/sale_order_view.xml',
        'wizard/mail_activity_type_wiz_view.xml',
        'views/template_layout.xml',
    ],
    "qweb": [
        "static/src/xml/quotation_followup.xml"
    ],
    'installable': True,
    'auto_install': False,
}
