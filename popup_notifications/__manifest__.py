# -*- coding: utf-8 -*-
{
    "name": "Popup notifications",
    "version": "11.0.1.0.1",
    "category": "Extra Tools",
    "author": "Odoo Tools",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/popup_notifications.xml"
    ],
    "qweb": [
        "static/xml/popup_notifications.xml"
    ],

}