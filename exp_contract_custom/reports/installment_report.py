# -*- coding: utf-8 -*-
from odoo import models, api

class InstallmentsReport(models.AbstractModel):
    _name = 'report.exp_contract_custom.installments_report'

    @api.multi
    def get_report_values(self, docids, data=None):
        return {
            'data': data,
            'docs': self.env['contract.contract'].browse(docids),
            'doc_model': self.env['contract.contract'],
        }
