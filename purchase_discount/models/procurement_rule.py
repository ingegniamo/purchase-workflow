# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProcurementRule(models.Model):
    _inherit = 'stock.rule'

    @api.multi
    def _prepare_purchase_order_line(self, product_id, product_qty,
                                     product_uom, values, po, partner):
        """Apply the discount to the created purchase order"""
        res = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, values, po, partner)
        date = None
        if po.date_order:
            date = fields.Date.to_string(
                fields.Date.from_string(po.date_order))
        seller = product_id._select_seller(
            partner_id=partner,
            quantity=product_qty,
            date=date, uom_id=product_uom)
        res.update(self._prepare_purchase_order_line_from_seller(seller))
        return res

    @api.model
    def _prepare_purchase_order_line_from_seller(self, seller):
        """Overload this function to prepare other data from seller,
        like in purchase_triple_discount module"""
        if not seller:
            return {}
        return {
            'discount': seller.discount,
        }
