# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################


from odoo import api, fields, models


class BudgetConfirmation(models.Model):
    _inherit = 'budget.confirmation'

    type = fields.Selection(selection_add=[("requisition.request", "Requisition Requests")])

    @api.multi
    def done(self):
        """
        change state to done and do set requisition request state to budget confirmed
        and create the voucher
        """
        self.ensure_one()

        if self.type == 'requisition.request':
            requisition_request_obj = self.env['requisition.request']
            requisition_request = requisition_request_obj.browse(self.res_id)
            requisition_request.budget_confirmed()

        return super(BudgetConfirmation, self).done()

    @api.multi
    def cancel(self):
        """
        change state to cancel and do set requisition request state to budget not confirmed
        """
        self.ensure_one()

        if self.type == 'requisition.request':
            requisition_request_obj = self.env['requisition.request']
            requisition_request = requisition_request_obj.browse(self.res_id)
            requisition_request.state = 'budget_not_confirmed'

        return super(BudgetConfirmation, self).cancel()
