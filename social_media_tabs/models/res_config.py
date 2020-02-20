# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _
# from openerp.osv import fields, osv
from odoo.exceptions import Warning
from odoo import SUPERUSER_ID
class SocialTabConfigSettings(models.TransientModel):
	_name = 'social.tab.config.settings'
	_inherit = 'webkul.website.addons'
	


 ###### These functions set the defaults values in the configuration  they have predefined  syntax...get_default_(field name )#####

	website_id =  fields.Many2one('website', string="website", required=True ,default=lambda self: self.env['website'].search([])[0])
	tab_ids = fields.One2many(related='website_id.tab_ids', string='Social Tabs', relation="social.media.tabs")
	tabs_position = fields.Selection(related='website_id.tabs_position', string='Tabs Position')
	tab_event = fields.Selection(related='website_id.tab_event_website', string='Tab Event' ,required=True)

	@api.multi
	def set_values(self):
		super(SocialTabConfigSettings, self).set_values()
		IrDefault = self.env['ir.default'].sudo()
		IrDefault.set('social.tab.config.settings','tab_ids', self.tab_ids.ids)
		IrDefault.set('social.tab.config.settings','tabs_position', self.tabs_position)
		IrDefault.set('social.tab.config.settings','tab_event', self.tab_event)
		return True



	@api.multi
	def get_values(self):
		res = super(SocialTabConfigSettings, self).get_values()
		IrDefault = self.env['ir.default'].sudo()
		res.update({
			'tab_ids':IrDefault.get('social.tab.config.settings','tab_ids'),
			'tabs_position':IrDefault.get('social.tab.config.settings','tabs_position'),
			'tab_event':IrDefault.get('social.tab.config.settings','tab_event'),
			
		})
		return res
