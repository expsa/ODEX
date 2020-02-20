# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import ValidationError, UserError


class ProductProduct(models.Model):
    """ Use product as service and ingrate it with initiatives """
    _inherit = 'product.product'

    nature = fields.Selection(selection=[
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('custody', 'Custody')], default='expense', string='Nature',
        help='''the nature of service which identify the type of the required account''')

    initiative_id = fields.Many2one(comodel_name='initiative',
                                    string='Initiative')

    initiative_service = fields.Boolean(string='Initiative Service')

    service_id = fields.Many2one(comodel_name='product.product',
                                 string='Service',
                                 domain=[('type', '=', 'service'), ('initiative_id', '!=', False)])

    sub_products = fields.One2many(comodel_name='product.product',
                                   inverse_name='service_id', string='Products',
                                   domain=[('initiative_id', '=', False)])

    department_id = fields.Many2one(related='initiative_id.department_id',
                                    comodel_name='hr.department', string='Department',
                                    store=True, readonly=True)

    account_restricted_income_id = fields.Many2one(
        'account.account', string="Restricted Income Account",
        domain=[('deprecated', '=', False)])
    account_restricted_expense_id = fields.Many2one(
        'account.account', string="Restricted Expense Account",
        domain=[('deprecated', '=', False)])

    @api.multi
    def unlink(self):
        ''' delete service but they must not be linked with initiative .
        '''
        for rec in self:
            if rec.initiative_id:
                raise UserError(
                    _('You cannot delete a service linked to initiative.'))
        return super(ProductProduct, self).unlink()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        inherit the name search to only show the initiative services
        when the pass it the context
        """
        context = dict(self.env.context)

        if not context.get('initiative_service', False):
            domain = [('initiative_service', '!=', True)]
            args = expression.AND([domain, args])

        if context.get('initiative_service', False):
            domain = [('initiative_service', '=', True)]
            args = expression.AND([domain, args])

        if 'purpose' in context:
            if context['purpose'] in ['custodies']:
                recs = self.env['product.product'].search(
                    [('nature', 'in', ['custody'])])
                recs = [x.id for x in recs]
                services = recs
                domain = [('id', 'in', services)]
                args = expression.AND([domain, args])
            if not context['purpose']:
                domain = [('id', '=', 0)]
                args = expression.AND([domain, args])
        if 'purpose' not in context or context['purpose'] in ['expense', 'income']:
            if 'get_my_services_by_budget' in context:
                get_my_services_by_budget = context.get('get_my_services_by_budget', False)
                if get_my_services_by_budget:
                    if get_my_services_by_budget == 'no_need':  # for income purpose
                        recs = self.env['product.product'].search(
                            [('nature', '=', context['purpose'])])
                        recs = [x.id for x in recs]
                        services = recs
                        domain = [('id', 'in', services)]
                        args = expression.AND([domain, args])
                    if get_my_services_by_budget != 'no_need':  # for expence purpose
                        analytic_obj = self.env['account.analytic.account']
                        analytic_id = analytic_obj.browse(get_my_services_by_budget)
                        services = [x.service_id.id for x in analytic_id.crossovered_budget_line
                                    if x.service_id]

                        domain = [('id', 'in', services)]
                        args = expression.AND([domain, args])
                if not get_my_services_by_budget:
                    domain = [('id', '=', 0)]
                    args = expression.AND([domain, args])
        return super(ProductProduct, self).name_search(name, args,
                                                       operator, limit)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}

        if not context.get('initiative_service', False):
            domain = [('initiative_service', '!=', True)]
            args = expression.AND([domain, args])

        if context.get('initiative_service', False):
            domain = [('initiative_service', '=', True)]
            args = expression.AND([domain, args])

        return super(ProductProduct, self).search(args, offset, limit, order, count=count)
