# -*- coding: utf-8 -*-
from odoo import http

# class ExpContractCustom(http.Controller):
#     @http.route('/exp_contract_custom/exp_contract_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exp_contract_custom/exp_contract_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exp_contract_custom.listing', {
#             'root': '/exp_contract_custom/exp_contract_custom',
#             'objects': http.request.env['exp_contract_custom.exp_contract_custom'].search([]),
#         })

#     @http.route('/exp_contract_custom/exp_contract_custom/objects/<model("exp_contract_custom.exp_contract_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exp_contract_custom.object', {
#             'object': obj
#         })