
from odoo import models, fields, api




class HRDep(models.Model):
    _inherit = 'hr.department'

    dep_link = fields.Many2one(comodel_name='department.info')

    @api.model
    def create(self, vals):
        new_record = super(HRDep, self).create(vals)
        data = self.env['department.info'].create({
            'department': new_record.name,
            'parent_dep': new_record.parent_id.id,
            'manager': new_record.manager_id.id,

        })
        new_record.dep_link = data.id

        return new_record

    @api.multi
    def write(self, vals):
        super(HRDep, self).write(vals)
        if self.dep_link:
            self.dep_link.department = self.name
            self.dep_link.parent_dep = self.parent_id.id
            self.dep_link.manager = self.manager_id.id

        return True

    @api.multi
    def unlink(self):
        self.dep_link.unlink()
        super(HRDep, self).unlink()
        return True
