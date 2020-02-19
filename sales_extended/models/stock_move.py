# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import float_is_zero
from collections import defaultdict

class StockMove(models.Model):
    _inherit = 'stock.move'

    line_no = fields.Char(string='No.')
    desc = fields.Html(string='Description')
    average = fields.Float(string="Average")

    @api.multi
    def product_price_update_before_done(self, forced_qty=None):
        tmpl_dict = defaultdict(lambda: 0.0)
        # adapt standard price on incomming moves if the product cost_method is 'average'
        std_price_update = {}
        for move in self.filtered(lambda move: move.location_id.usage in (
                'supplier', 'production', 'internal', 'customer') and move.product_id.cost_method == 'average'):
            product_tot_qty_available = move.product_id.qty_available + tmpl_dict[move.product_id.id]
            rounding = move.product_id.uom_id.rounding

            qty_done = 0.0
            if float_is_zero(product_tot_qty_available, precision_rounding=rounding):
                new_std_price = move._get_price_unit()

            elif float_is_zero(product_tot_qty_available + move.product_qty, precision_rounding=rounding):
                new_std_price = move._get_price_unit()

            else:
                # Get the standard price
                amount_unit = std_price_update.get(
                    (move.company_id.id, move.product_id.id)) or move.product_id.standard_price
                qty_done = move.product_uom._compute_quantity(move.quantity_done, move.product_id.uom_id)
                qty = forced_qty or qty_done
                new_std_price = ((amount_unit * product_tot_qty_available) + (move._get_price_unit() * qty)) / (
                        product_tot_qty_available + qty_done)

            tmpl_dict[move.product_id.id] += qty_done
            print("standard price", new_std_price)
            # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
            move.product_id.with_context(force_company=move.company_id.id).sudo().write(
                {'standard_price': new_std_price})
            std_price_update[move.company_id.id, move.product_id.id] = new_std_price

            move.average = new_std_price
            """ here move.average is our field created to use in report """

        for move in self.filtered(lambda move: move.location_id.usage in (
                'supplier', 'production', 'internal', 'customer') and move.product_id.cost_method == 'standard'):
            new_std_price = move._get_price_unit()
            move.average = new_std_price

    def _run_valuation(self, quantity=None):
        super(StockMove, self)._run_valuation(quantity=None)

        for move in self.filtered(lambda move: move.location_id.usage in (
                'supplier', 'production', 'internal', 'customer') and move.product_id.cost_method == 'fifo'):
            move.average = abs(self.price_unit)


StockMove()
