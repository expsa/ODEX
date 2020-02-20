# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)

class SocialTabs(http.Controller):

	@http.route('/socialTabs/url', type='json', auth='public', website=True)
	def social_tabs_url(self, tab_id=False):
		
		tab_obj = request.env['social.media.tabs'].sudo().browse(int(tab_id))
		values = {}
		if tab_obj:
			values['type'] = tab_obj.media_type,
			if tab_obj.media_type == 'social_tab':
				values['limit']=tab_obj.limit
				if tab_obj.social_tab:

					if  tab_obj.social_tab in  ['facebook','fblike']:
						values['url'] = 'https://graph.facebook.com/' + tab_obj.facebook_id,
						values['fb_token'] = tab_obj.fb_token,
						values['fb_id'] = tab_obj.facebook_id,
						values['social_tab'] = tab_obj.social_tab,
					if tab_obj.social_tab == 'youtube':
						values['api_key'] = tab_obj.yt_api_key,
						values['channel_id'] = tab_obj.yt_channel_id,
						values['user_id'] = tab_obj.yt_user_id,
						values['subscribe'] = tab_obj.yt_show_subscribe,
					if tab_obj.social_tab == 'flickr':
						values['flickr_id'] = tab_obj.flickr_id,
					if tab_obj.social_tab == 'pinterest':
						values['pinterest_id'] = tab_obj.pinterest_id,
					if tab_obj.social_tab == 'vimeo':
						values['vimeo_id'] = tab_obj.vimeo_id,
					if tab_obj.social_tab == 'tumblr':
						values['tumblr_id'] = tab_obj.tumblr_id,
					if tab_obj.social_tab == 'stumbleupon':
						values['stumbleupon_id'] = tab_obj.stumbleupon_id,
					if tab_obj.social_tab == 'google':
						values['google_id'] = tab_obj.google_id,
						values['google_api_key'] = tab_obj.google_api_key,
			else:
				values['custom_html'] =  tab_obj.custom_html
		return values