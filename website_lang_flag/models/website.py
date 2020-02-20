# -*- coding: utf-8 -*-


from odoo import models, fields
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    def get_languages_flag(self):
        return [(lg.code, lg) for lg in self.language_ids]

    def get_name_lg(self, code):
        lang_obj = self.env['res.lang']
        lang_id = lang_obj.search([('code', '=', code)])
        return lang_obj.browse(int(lang_id)).name

    def get_id_lg(self, code):
        lang_obj = self.env['res.lang']
        lang_id = lang_obj.search([('code', '=', code)])
        return lang_obj.browse(int(lang_id)).id
