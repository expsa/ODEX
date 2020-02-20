from odoo import models, fields, api


class ResLang(models.Model):
    _inherit = 'res.lang'

    hijri_date_format = fields.Char('Hijri Date Format', default='yyyy-mm-dd')


ResLang()


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def get_localisation(self):
        if self.env.user.lang:
            lang_id = self.env['res.lang'].search([('code', '=', self.lang)])
            if lang_id:
                return {
                    'lang': lang_id.hijri_date_format,
                }
            else:
                return {
                    'lang': 'yyyy-mm-dd',
                }
        else:
            return {
                'lang': 'yyyy-mm-dd',
            }
