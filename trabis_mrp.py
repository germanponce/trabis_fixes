# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError

#PARA FECHAS
from datetime import datetime, timedelta

##### SOLUCIONA CUALQUIER ERROR DE ENCODING (CARACTERES ESPECIALES)
import sys
reload(sys)  
sys.setdefaultencoding('utf8')


class mrp_production(models.Model):
    _inherit = 'mrp.production'


    @api.multi
    def action_cancel(self):
        res = super(mrp_production, self).action_cancel()
        for rec in self:
            try:
                group_id = rec.move_finished_ids[0].group_id.id if rec.move_finished_ids[0] else False
                if group_id:
                    self.env.cr.execute("""
                        select id from stock_move 
                            where group_id=%s 
                                and product_id=%s 
                                and production_id is null;
                        """, (group_id,rec.product_id.id))
                cr_res = self.env.cr.fetchall()
                move_ids = [x[0] for x in cr_res]
                for move in self.env['stock.move'].browse(move_ids):
                    if move.state not in ('done','cancel'):
                        move.action_cancel()
            except:
                continue
        return res