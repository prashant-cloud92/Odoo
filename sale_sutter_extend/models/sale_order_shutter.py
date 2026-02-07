from odoo import api,fields,models,exceptions

class ShutterSaleLine(models.Model):
    _inherit = 'sale.order.line'

    shutter_width = fields.Float(string="Shutter Width")
    shutter_height = fields.Float(string="Shutter Height")