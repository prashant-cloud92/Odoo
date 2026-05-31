from odoo import fields, models

class BillboardBoard(models.Model):
    _name = 'billboard.board'
    _description = 'Billboard'

    name = fields.Char(string='Billboard Name', required=True)
    type_id = fields.Many2one('billboard.type', string='Billboard Type', required=True)
    properties = fields.Properties(string='Properties', definition='type_id.property_definitions', copy=True)
    
    location = fields.Char(string='Location')
    price = fields.Float(string='Price')
    active = fields.Boolean(string='Active', default=True)
