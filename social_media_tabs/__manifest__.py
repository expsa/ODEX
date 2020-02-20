#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Website Social Network Tabs",
  "summary"              :  "Embed your social network profiles into your ecommerce.",
  "category"             :  "Website",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/Odoo-Website-Social-Network-Tabs.html",
  "description"          :  "http://webkul.com/blog/odoo-website-social-network-tabs/",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=social_media_tabs&version=11.0&custom_url=/",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'views/webkul_addons_config_inherit_view.xml',
                             'views/res_config_view.xml',
                             'views/social_media_tabs_view.xml',
                             'views/templates.xml',
                             'security/ir.model.access.csv',
                            ],
   "demo":['data/demo.xml'],
  "images"               :  ['static/description/banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}