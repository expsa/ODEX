from odoo import models, fields


class DocumentDirectory(models.Model):
    _name = 'document.directory'
    name = fields.Char(string='Directory')


DocumentDirectory()
