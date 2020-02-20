# -*- coding: utf-8 -*-
{
    'name': 'Report RTL Custom',
    'version': '1.0',
    'summary': 'Report RTL (Right to Left) layout',
    'description':
        """
Adding RTL (Right to Left) Support for Reports.
===============================================

This module provides a propper RTL support for Odoo 11  reports , inhiriting the html_container and minimal_layout to add rtl direction.
Adding Arbic fonts to reports 
        """,
    'depends': ['report_rtl_v11',],
    'auto_install': True,
    'data': [
        'views/layout.xml',
    ],
}
