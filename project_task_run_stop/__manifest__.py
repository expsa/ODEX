# -*- coding: utf-8 -*-
{
    'name': "Project Task Start Stop and Pause",
    'version': "1.1.5",
    'author': "BusinessApps",
    'website': "http://business-apps.ru",
    'category': "Project",
    'support': "info@business-apps.ru",
    'summary': "Add Start, Stop and Pause buttons in Kanban and Form view with the preservation of working time in the timesheets",
    'description': "",
    'license':'OPL-1',
    'price': 24.90,
    'currency': 'EUR',
    'images':['static/description/banner.jpg'],
    'data': [
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'depends': ['project','hr_timesheet'],
    'application': True,
}
