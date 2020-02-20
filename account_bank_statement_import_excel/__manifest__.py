{
    'name': 'Import Excel Bank Statement',
    'category': 'Banking addons',
    'license': 'AGPL-3',
    'author': 'Alfadil',
    'depends': [
        'account_bank_statement_import',
    ],
    'data': [
        'views/view_account_bank_statement_import.xml',
        'views/excel_dimensions_views.xml',
    ],
    'external_dependencies': {
        'python': ['xlrd'],
    },
    'installable': True,
}
