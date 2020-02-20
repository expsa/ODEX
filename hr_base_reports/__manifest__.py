{
    'name': 'HR Base Reports',
    'category': 'HR-Odex',
    'summary': 'HR Reports',
    'version': '1.0',
    'sequence': 4,
    'website': 'http://exp-sa.com',
    'license': 'GPL-3',
    'author': 'Expert Co. Ltd.' ,
    'depends': ['base', 'hr','hr_base','hr_disciplinary_tracking','employee_requests','report_xlsx'],
    'data': [

        'views/hr_department_job_wizard_view.xml',
        'views/hr_offer_report_wizard_view.xml',
        'views/hr_employee_reward_wizard.xml',
        'views/hr_termination_view.xml',
        'views/leave_reports_view.xml',
        'views/overtime_report_of_employee_view.xml',
        'views/penalty_deduction_of_employee_view.xml',
        'views/sales_report.xml',

        'views/hr_base_reports_menus.xml',
        'report/hr_department_report.xml',
        'report/hr_department_job_template.xml',
        'report/hr_offer_job_report.xml',
        'report/hr_job_offer_template.xml',
        'report/hr_employee_reward_report.xml',
        'report/hr_employee_reward_template.xml',

    ],
    # 'qweb': ['static/src/xml/base_template.xml'],
    'installable': True,
    'application': True,
}
