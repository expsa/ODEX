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
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class WebsiteMessageWizard(models.TransientModel):

	_name="website.message.wizard"
	_description="Wizard for show message for user."

	message = fields.Text(string="Message")

	@api.multi
	def update_latest_record(self):
		active_model = self.env[self._context.get('active_model')]
		active_id = self._context.get('active_id') or self._context.get('active_ids')[0]
		for current_record in self:
			is_active_record = active_model.search([('is_active','=',True)])
			is_active_record.write({'is_active':False})
			active_record = active_model.browse(active_id)
			active_record.write({'is_active':True})
		return True

	@api.multi
	def cancel(self):
		active_model = self.env[self._context.get('active_model')]
		active_id = self._context.get('active_id') or self._context.get('active_ids')[0]
		active_record = active_model.browse(active_id)
		active_record.write({'is_active':False})