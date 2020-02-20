{
    'name': 'Employee  Requests',
    'category': 'HR-Odex',
    'summary': 'HR Management Employee Requests and self service',
    'version': '1.0',
    'sequence': 4,
    'website': 'http://exp-sa.com',
    'license': 'GPL-3',
    'author': 'Expert Co. Ltd.' ,

    'depends': ['base', 'account', 'hr_loans_salary_advance', 'exp_payroll_custom',
                'attendences'],

    'data': [
        'security/employee_requests_security.xml',
        'security/ir.model.access.csv',

        'views/employee_effective_form.xml',
        'views/employee_overtime_request.xml',
        'views/hr_clearance_form.xml',
        'views/hr_personal_permission.xml',
        'views/customize_hr_employee.xml',
        'views/employee_department_jobs_view.xml',
        'views/attendance_view.xml',

        'report/employee_clearance_report/employee_clearance_form_reports.xml',
        'report/employee_clearance_report/employee_clearance_form_template1.xml',
        'report/employee_clearance_report/employee_clearannce_detailes_template.xml',
        'report/clearance_employee_report_template.xml',

        # data
        'data/data.xml',
        # menu items
        'views/employee_request_menu.xml',
    ],
    # 'qweb': ['static/src/xml/base_template.xml'],
    'installable': True,
    'application': True,
}
