# -*- coding: utf-8 -*-
##############################################################################
#
#    (Odex - Extending the base module).
#    Copyright (C) 2017 Expert Co. Ltd. (<http://exp-sa.com>).
#
##############################################################################
{
    'name' : 'Odex - Base Module',
    'version' : '1.0',
    'author' : 'Expert Co. Ltd.',
    'category' : 'base',
    'description' : """
Odex - Extending the base module
=================================
Extending the Odoo's base module by adding a cross-apps models e.g. `res.country.city`.
any new module should depend in this module so that developer can reuse it.
    """,
    'website': 'http://www.exp-sa.com',
    'depends' : 

#Some App + old theme
['base','access_apps','web_login_background','access_restricted','access_settings_menu','backend_theme_v11','base_user_role','comceptplus_message_readers','document_url_fork','google_recaptcha','ir_rule_protected','mss_whatsapp_redirect','report_rtl_v11','sync_drag_drop_attach','web_export_view','web_hijri_datepicker','web_responsive','web_rtl_v11','website_rtl_v11','wk_show_password'],

#All Apps+New Theme
#['base','access_apps','uppercrust_backend_theme','uppercrust_backend_theme_rtl','web_rtl','web_rtl_v11','access_restricted','access_settings_menu','base_user_role','comceptplus_message_readers','document_url_fork','google_recaptcha','ir_rule_protected','mss_whatsapp_redirect','muk_account_bank_statement_import_sheet','muk_attachment_lobject','muk_automation_extension','muk_autovacuum','muk_converter','muk_dms','muk_dms_access','muk_dms_attachment','muk_dms_export','muk_dms_field','muk_dms_file','muk_dms_lobject','muk_dms_share','muk_dms_thumbnails','muk_fields_lobject','muk_models_groupby_hour','muk_quality_docs','muk_quality_docs_dms','muk_security','muk_thumbnails','muk_utils','muk_web_client','muk_web_client_notification','muk_web_client_refresh','muk_web_export','muk_web_export_attachment','muk_web_fields_lobject','muk_web_preview','muk_web_preview_attachment','muk_web_preview_audio','muk_web_preview_csv','muk_web_preview_image','muk_web_preview_lobject','muk_web_preview_mail','muk_web_preview_markdown','muk_web_preview_msoffice','muk_web_preview_rst','muk_web_preview_text','muk_web_preview_vector','muk_web_preview_video','muk_web_security','muk_web_share','muk_website_customize_gradient','muk_website_navbar_transparent','muk_website_scroll_up','muk_website_snippet_grid','muk_web_utils','partner_external_map','report_rtl_v11','sync_drag_drop_attach','user_login_alert','web_debranding','web_export_view','web_hijri_datepicker','wk_show_password'],

#All Apps 
#['base','access_apps','backend_user_decoration','web_login_background','web_widget_color','access_restricted','access_settings_menu','backend_theme_v11','base_user_role','comceptplus_message_readers','document_url_fork','google_recaptcha','ir_rule_protected','mss_whatsapp_redirect','muk_account_bank_statement_import_sheet','muk_attachment_lobject','muk_automation_extension','muk_autovacuum','muk_converter','muk_dms','muk_dms_access','muk_dms_attachment','muk_dms_export','muk_dms_field','muk_dms_file','muk_dms_lobject','muk_dms_share','muk_dms_thumbnails','muk_fields_lobject','muk_models_groupby_hour','muk_quality_docs','muk_quality_docs_dms','muk_security','muk_thumbnails','muk_utils','muk_web_client','muk_web_client_notification','muk_web_client_refresh','muk_web_export','muk_web_export_attachment','muk_web_fields_lobject','muk_web_preview','muk_web_preview_attachment','muk_web_preview_audio','muk_web_preview_csv','muk_web_preview_image','muk_web_preview_lobject','muk_web_preview_mail','muk_web_preview_markdown','muk_web_preview_msoffice','muk_web_preview_rst','muk_web_preview_text','muk_web_preview_vector','muk_web_preview_video','muk_web_security','muk_web_share','muk_website_customize_gradient','muk_website_navbar_transparent','muk_website_scroll_up','muk_website_snippet_grid','muk_web_utils','partner_external_map','report_rtl_v11','sync_drag_drop_attach','user_login_alert','web_debranding','web_export_view','web_hijri_datepicker','web_responsive','web_rtl_v11','website_rtl_v11','wk_show_password'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_city_view.xml',
        'views/menus_and_actions.xml',
    ],
    'qweb' : [
    ],
    'installable': True,
    'auto_install': False,
}
