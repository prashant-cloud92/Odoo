from odoo import api,fields,models,exceptions
from odoo.exceptions import UserError

class ShutterSaleLine(models.Model):
    _inherit = 'sale.order.line'

    shutter_width = fields.Float(string="Shutter Width")
    shutter_height = fields.Float(string="Shutter Height")
    lock_product_id = fields.Many2one('product.template',string="Lock Type")
    stopper_product_id=fields.Many2one('product.template',string="Stopper Type")
    blade_product_id=fields.Many2one('product.template',string="Blade Type")


    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(ShutterSaleLine, self)._onchange_product_id()

        if self.product_id:
            self.lock_product_id = self.product_id.product_tmpl_id.shutter_type_id.lock_product_id.id
            self.stopper_product_id = self.product_id.product_tmpl_id.shutter_type_id.stopper_product_id.id
            self.blade_product_id = self.product_id.product_tmpl_id.shutter_type_id.blade_product_id.id
        return res
    @api.model_create_multi
    def create(self, vals):


        for val in vals:
            product_template_id=val.get('product_template_id')
            shutter_width = val.get('shutter_width')
            shutter_height = val.get('shutter_height')

            product_id= self.env['product.template'].browse(product_template_id)

            if product_id:
                if product_id.is_apron:
                    # product_id=self.env['product.template'].browse(product_id)
                    if shutter_width<product_id.min_width or shutter_width>product_id.max_width:
                        raise UserError(f"Shutter Width set Between {product_id.min_width} and {product_id.max_width} ")
                    elif shutter_height<product_id.min_height or shutter_height>product_id.max_height:
                        raise UserError(f"Shutter Height set Between {product_id.min_height} and {product_id.max_height} ")

        return super(ShutterSaleLine, self).create(vals)

    def write(self,vals):


        for rec in self:
            shutter_width = vals.get('shutter_width', 0)
            shutter_height = vals.get('shutter_height', 0)
            product_id = vals.get('product_template_id', 0)



            if shutter_width:
                if rec.product_id.is_apron:
                    if shutter_width < rec.product_template_id.min_width or shutter_width >rec.product_template_id.max_width:
                        raise UserError(
                            f"Shutter Width set Between {rec.product_template_id.min_width} and {rec.product_template_id.max_width} ")
            if shutter_height:
                if rec.product_id.is_apron:
                    if shutter_height < rec.product_template_id.min_height or shutter_height > rec.product_template_id.max_height:
                        raise UserError(
                            f"Shutter Height set Between {rec.product_template_id.min_height} and {rec.product_template_id.max_height} ")

            if product_id:
                new_product_id=self.env['product.template'].browse(product_id)
                if new_product_id.is_apron:
                    if shutter_width < new_product_id.min_width or shutter_width >new_product_id.max_width:
                        raise UserError(
                            f"Shutter Width set Between {new_product_id.min_width} and {new_product_id.max_width} ")
                    if shutter_height < new_product_id.min_height or shutter_height > new_product_id.max_height:
                        raise UserError(
                            f"Shutter Height set Between {new_product_id.min_height} and {new_product_id.max_height} ")

        return super(ShutterSaleLine, self).write(vals)

'''
       for val in vals:
           product_template_id=val.get('product_template_id',[])
            rec = super(ShutterSaleLine, self).create(vals)
            
            if rec.product_template_id:
                if rec.product_template_id.is_apron:
                    # product_id=self.env['product.template'].browse(product_id)
                    if rec.shutter_width<rec.product_template_id.min_width or rec.shutter_width>rec.product_template_id.max_width:
                        raise UserError(f"Shutter Width set Between {rec.product_template_id.min_width} and {rec.product_template_id.max_width} ")
                    elif rec.shutter_height<rec.product_template_id.min_height or rec.shutter_height>rec.product_template_id.max_height:
                        raise UserError(f"Shutter Height set Between {rec.product_template_id.min_height} and {rec.product_template_id.max_height} ")
            return rec 



def write(self,val):
if val['shutter_height'] or val['shutter_width']:
if self.product_template_id.min_width < val['shutter_width'] or val['shutter_width']<self.product_template_id.min_width:
raise UserError(f"Shutter Width set Between {self.product_template_id.min_width} and {self.product_template_id.max_width} ")
elif self.shutter_height < self.product_template_id.min_height or self.shutter_height > self.product_template_id.max_height:
raise UserError(f"Shutter Height set Between {self.product_template_id.min_height} and {self.product_template_id.max_height} ") 
'''
