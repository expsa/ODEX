# -*- coding: utf-8 -*-
##############################################################################
#
#    LCT, Life Connection Technology
#    Copyright (C) 2011-2012 LCT 
#
##############################################################################

from odoo import api, fields, models, _

class ResUsers(models.Model):
	_inherit = 'res.users'

	def _default_groups_custom(self):
		"""
        pervents newly created user from holding all managers groups.
        """
		default_user = self.env.ref('base.group_user', raise_if_not_found=False)
		return default_user

	groups_id = fields.Many2many('res.groups', 'res_groups_users_rel', 'uid', 'gid', string='Groups', default =_default_groups_custom)
