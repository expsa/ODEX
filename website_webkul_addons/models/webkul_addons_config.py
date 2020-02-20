# -*- coding: utf-8 -*-
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

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class WebkulWebsiteAddons(models.TransientModel):
    _name = 'webkul.website.addons'
    _inherit = 'res.config.settings'

    # Social Network

    # Product Management
    module_dynamic_bundle_products = fields.Boolean(string="Website Customize Bundle Products")
    module_wk_review = fields.Boolean(string="Website: Product Review")

    #Delivery Method
    module_website_store_pickup = fields.Boolean(string="Website: Store Pickup")

    # Stock Management
    module_website_stock = fields.Boolean(string = "Website: Product Stock")
    module_website_stock_notifiy = fields.Boolean(string = "Website: Stock Notify")
    module_website_hide_out_of_stock = fields.Boolean(string="Website : Hide out of stock products")
    module_website_giftwrap = fields.Boolean(string = "Website: Gift Wrap")

    # web Page
    module_website_product_quickview = fields.Boolean(string = "Website: Product Quickview")
    module_website_onepage_checkout = fields.Boolean(string = "Website: Onepage Checkout")
    module_website_recently_viewed_products = fields.Boolean(string="Website: Recently Viewed Products")
    module_website_360degree_view = fields.Boolean(string="Website: Product 360° VIEW")
    module_email_verification = fields.Boolean(string = "Email Verification")
    module_website_seo = fields.Boolean(string = "Website SEO")
    module_website_country_restriction = fields.Boolean(string="Website Country Restriction")
    module_website_estimated_delivery = fields.Boolean(string = "Website Estimated Delivery")
    module_website_store_locator = fields.Boolean(string="Website: Store Locator")
    module_website_block_content_copy = fields.Boolean(string="Website: Website Stop/Block Content Copy")
    module_website_banner_slider = fields.Boolean(string = "Website Banner Slider")
    
    # Sales Promotion
    module_website_daily_deals = fields.Boolean(string = "Website Daily Deals")
    module_website_first_order_discount = fields.Boolean(string="Website: First Purchase Discount")
    module_website_terms_conditions = fields.Boolean(string = "Website: Terms and Conditions")
    module_social_network_tabs = fields.Boolean(string="Social Network Tabs")
    module_website_sales_count = fields.Boolean(string="Website Sales Count")
    module_website_product_vote = fields.Boolean(string = "Website: Product Vote")
    module_website_cart_settings = fields.Boolean(string = "Website Cart Settings")
    module_website_order_notes = fields.Boolean(string = "Website: Internal Notes on Order")
    module_website_product_tags = fields.Boolean(string="Website: Product Tags")
    module_website_product_price_range = fields.Boolean(string="Website: Product  Price Range")
    module_hidden_products = fields.Boolean(string = "Website: Hidden Product")
    module_website_mega_menus = fields.Boolean(string = "Website Mega Menu")
    module_products_az_list = fields.Boolean(string = "Website: Product A-Z List")
    module_products_az_filter = fields.Boolean(string = "Website: Product A-Z Filter")
    module_website_facebook_wallfeed = fields.Boolean(string="Website Facebook Wall Feed")
    module_website_newsletter = fields.Boolean(string="Website Newsletter")
    module_share_the_love = fields.Boolean(string="Share The Love")
    module_website_also_bought_products = fields.Boolean(string="Website Also bought Products")
    module_frequently_bought_together_products = fields.Boolean(string="Frequently bought Togther Products")
    module_website_quote_system = fields.Boolean(string = "Website: Quote System")
    module_google_rich_snippets = fields.Boolean(string = "Google Rich Snippets")
    module_review_after_purchase = fields.Boolean(string="Website: Product Review After Purchase")
    module_website_auction = fields.Boolean(string="Website Auction")
