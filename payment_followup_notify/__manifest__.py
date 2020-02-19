# -*- coding: utf-8 -*-
{
    "name": "Follow up Notify",
    "version": "11.0.1.0.1",
    "category": "Extra Tools",
    "author": "Odoo Tools",
    "license": "AGPL-3",
    "depends": ["account","ce_accounting_followup", "popup_notifications"],
    "data": [
        "data/data.xml",
        "views/account_followup_view.xml"
    ],
    "application": True,
    "installable": True,
    "auto_install": False,

}
