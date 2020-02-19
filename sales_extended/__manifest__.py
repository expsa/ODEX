# -*- coding: utf-8 -*-
{
    'name': "Sales Module",
    'summary': "Sales New features",
    'description': """
             This module modify Sales module to fit requested needs
    """,
    'author': "Expert Co. Ltd.",
    'website': 'http://exp-sa.com',
    'category': 'Repair',
    'version': '11.1.0.1',
    'depends': ['base', 'sale', 'stock_landed_costs', 'product_expiry', 'purchase'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/bank_view.xml',
        'views/sale_order_view.xml',
        'views/product_view.xml',
        'views/purchase_order_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml',
        'views/res_partner_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_lot_view.xml',
        'views/scrap_order_view.xml',
        'views/product_brand_view.xml',
        'views/terms_conditions_view.xml',
        'views/report.xml',
        'views/account_invoice.xml',
        'views/report_sale_order_view.xml',
        'wizard/sale_setting_wiz_view.xml',
        'wizard/stock_setting_wiz_view.xml',
        'wizard/update_calibration_wiz_view.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
