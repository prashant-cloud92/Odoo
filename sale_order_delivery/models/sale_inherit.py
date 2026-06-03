from odoo import api, fields, models, tools

class Move_Inherit(models.Model):
    _inherit = "stock.move"

    order_id = fields.Char(string="Order ID",
        compute="_compute_order_id",
        store=True)
    @api.depends('reference')
    def _compute_order_id(self):
       for record in self:
           record.order_id=record.picking_id.origin


