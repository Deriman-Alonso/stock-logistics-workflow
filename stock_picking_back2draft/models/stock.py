# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_back_to_draft(self):
        if self.filtered(lambda m: m.state != 'cancel'):
            raise UserError(_("You can set to draft cancelled moves only"))
        if self.filtered(lambda m: m.procure_method == 'make_to_order'):
            raise UserError(_(
                "You can set to draft only move without chained picking"))
        self.write({'state': 'draft'})


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_back_to_draft(self):
        moves = self.mapped('move_lines')
        moves.action_back_to_draft()
