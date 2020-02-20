# -*- coding: utf-8 -*-
###################################################################################
#    A part of OpenHRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Anusha P P (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Loans',
    'version': '1.0',
    'summary': 'Manage Loan Requests',
    'description': """
        Helps you to manage Loan Requests of your company's staff.
        """,
    'category': 'HR-Odex',
    'author': 'Expert Co. Ltd.' ,
    'company': 'Exp-co-ltd',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'http://exp-sa.com',
    'depends': ['base','hr','account','hr_payroll','mail','hr_appraisal‏','exp_payroll_custom',
    ],
    'data': [

        'security/hr_loans_salary_advance.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/hr_loan_salary_advance.xml',
        'views/loan_request_type_view.xml',
        'views/loan_installment_line_view.xml',
        'wizard/loan_payslip_monthly_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
