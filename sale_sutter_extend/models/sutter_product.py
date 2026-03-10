from odoo import api, fields, models, tools
from odoo.exceptions import UserError

class ShutterProduct(models.Model):
    _inherit = 'product.template'

    is_apron=fields.Boolean(default=False)
    min_width=fields.Float(default=0.0)
    max_width=fields.Float(default=0.0)
    min_height=fields.Float(default=0.0)
    max_height=fields.Float(default=0.0)
    shutter_type_id=fields.Many2one('shutter.type')

    def create(self, vals):
        if vals.get('is_apron',False):
            if vals.get('min_width',0)<=0:
                raise UserError("Please enter a Value More Than Zero in Min Width")
            elif vals.get('max_width',0)<=0 :
                raise UserError("Please enter a Value More Than Zero in Max Width")
            elif vals.get('min_height',0)<=0:
                raise UserError("Please enter a Value More Than Zero in Min Height")
            elif vals.get('max_height',0)<=0:
                raise UserError("Please enter a value between 0 and 1000 in MAX HEIGHT")

        return super(ShutterProduct, self).create(vals)