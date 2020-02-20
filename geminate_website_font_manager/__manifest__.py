# -*- coding: utf-8 -*-
###############################################################################
#
#   geminate_website_font_manager for Odoo
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Geminate Website Font Manager',
    'version': '10.0.0.1.0',
    'category': 'Website',
    'license': 'AGPL-3',
    'summary': 'Website font manager',
    'description': """
This module will introduce a new control of font manager in form editor bar on the website editor.
On website editor, there will be an option available to manage font faces and font size.

It will load most commonly used google font faces and default font size from 8 to 72.
""",
    'author': "Geminate Consultancy Services",
    'website': 'http://www.geminatecs.com/',
    'depends': [
        'website'
    ],
    'data': [
        'views/website_font_manager.xml',
    ],
    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
