from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError

class ShutterType(models.Model):
    _name = 'shutter.type'
    _description = 'Shutter Type'

    name=fields.Char(string='Shutter Type')
    min_height = fields.Float(string='Min Height')
    max_height=fields.Float(string='Max Height')
    min_width=fields.Float(string='Min Width')
    max_width=fields.Float(string='Max Width')
    lock_product_id = fields.Many2one(comodel_name='product.template',string='Lock Product')
    stopper_product_id = fields.Many2one(comodel_name='product.template',string='Stopper Product')
    blade_product_id=fields.Many2one(comodel_name='product.template',string='Blade Product')

