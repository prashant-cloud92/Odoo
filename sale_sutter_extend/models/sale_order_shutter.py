from odoo import api,fields,models,exceptions
from odoo.exceptions import UserError

class ShutterSaleLine(models.Model):
    _inherit = 'sale.order.line'

    shutter_width = fields.Float(string="Shutter Width")
    shutter_height = fields.Float(string="Shutter Height")

    def create(self, vals):
        rec = super(ShutterSaleLine, self).create(vals)
        # product_id = vals.get('', False)
        if rec.product_template_id:
            # product_id=self.env['product.template'].browse(product_id)
            if rec.shutter_width<rec.product_template_id.min_width or rec.shutter_width>rec.product_template_id.max_width:
                raise UserError(f"Shutter Width set Between {rec.product_template_id.min_width} and {rec.product_template_id.max_width} ")
            elif rec.shutter_height<rec.product_template_id.min_height or rec.shutter_height>rec.product_template_id.max_height:
                raise UserError(f"Shutter Height set Between {rec.product_template_id.min_height} and {rec.product_template_id.max_height} ")
        return rec
    
    def create(self,val):
        product_id=val.get('product_id')
        product_id=self.env['product.template'].browse(product_id)
        if product_id.product_template_id:
