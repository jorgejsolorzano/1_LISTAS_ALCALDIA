# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import UserError
import logging
import datetime

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        #buscar PLAN
        plan = ''
        c_mutropico = 0
        cant_secundaria = 0
        cant_principal = 0
        for l1 in self.order_line:
            product_name = l1.product_id.name
            category_name = l1.product_id.categ_id.name
            product_price = l1.price_unit
            if 'Plan' in category_name:
                plan = product_name
                _logger.debug(f'|SaleOrder|action_confirm|Plan encontrado|{plan}')
            if 'Embrionaria' in category_name and product_price == 0:
                cant_secundaria += l1.product_uom_qty
            if 'Mutropico' in category_name and product_price == 0:
                c_mutropico += l1.product_uom_qty
            if 'Ambrosia' in category_name and product_price == 0:
                cant_principal += l1.product_uom_qty

        if len(plan) > 0:
            if 'BASICO' in plan and not(cant_principal == 1 and cant_secundaria == 1):
                msg = f'ERROR en los productos del {plan} debe tener 1 Ambrosia y 1 Embrionaria con precio CERO'
                raise UserError(msg)
            if 'ESTANDAR' in plan and not(cant_principal == 1 and cant_secundaria == 2):
                msg = f'ERROR en los productos del {plan} debe tener 1 Ambrosia y 2 Embrionaria con precio CERO'
                raise UserError(msg)
            if 'PREMIUM' in plan and not(cant_principal == 1 and cant_secundaria == 3):
                msg = f'ERROR en los productos del {plan} debe tener 1 Ambrosia y 3 Embrionaria con precio CERO'
                raise UserError(msg)
        return super(SaleOrder, self).action_confirm()


