# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    show_in_report = fields.Boolean(default=True)

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        category_name = self.product_id.categ_id.name
        _logger.debug(f'|AccountMoveLine|_onchange_price_unit|{category_name} {self.price_unit}')
        #and category_name in ['Ambrosia', 'Extracto']
        if self.price_unit < 0.01:
            self.show_in_report = False
        else:
            self.show_in_report = True
